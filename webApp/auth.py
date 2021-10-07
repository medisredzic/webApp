import os
import functools
import sys

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from webApp.db import get_db

from dotenv import load_dotenv

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['fName']
        lastName = request.form['lName']
        manCode = request.form['manCode']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif not firstName:
            error = 'First name is required'
        elif not lastName:
            error = 'Last name is required'
        elif not manCode:
            error = 'Manager code is required'

        if manCode != os.getenv('MANAGER_KEY'):
            error = 'Manager code is incorrect'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user(username, firstName, lastName, password, level) VALUES (?, ?, ?, ?, 1)",
                    (username, firstName, lastName, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db=get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username, )
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


def is_manager(uid):
    db = get_db()

    user = db.execute('SELECT level FROM user WHERE id = ?', (uid, )).fetchone()

    if user['level'] > 2:
        return user['level']
    else:
        return user['level']
