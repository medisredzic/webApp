from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from webApp.auth import login_required, is_manager
from webApp.db import get_db
from webApp.items import get_item

bp = Blueprint('cashregister', __name__, url_prefix='/cregister')


@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT * FROM items ORDER BY id ASC'
    ).fetchall()

    return render_template('cashregister/add.html', items=items)


@bp.route('/register', methods=('GET', 'POST'))
@login_required
def add():

    addList = {}

    if request.method == 'POST':
        itemid = request.form['itemid']
        stock = request.form['stock']
        error = None

        if not itemid:
            error = "You need to enter id or barcode"

        if not stock:
            stock = 1

        if error is not None:
            flash(error)
        else:
            addList[itemid] = stock

    return render_template('cashregister/add.html', addList=addList)
