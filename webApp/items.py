from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from webApp.auth import login_required, is_manager
from webApp.db import get_db

bp = Blueprint('items', __name__, url_prefix='/items')


@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT * FROM items ORDER BY id ASC'
    ).fetchall()

    return render_template('items/index.html', items=items)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        itemname = request.form['itemName']
        wholesaleprice = request.form['wholesalePrice']
        retailprice = request.form['retailPrice']
        stock = request.form['stock']
        barcode = request.form['barcode']

        error = None

        if not itemname:
            error = "Item needs to have a name"
        elif not wholesaleprice:
            error = "Item needs to have wholesale price"
        elif not retailprice:
            error = "Item needs to have retail price"
        elif not stock:
            error = "Item needs to have stock"
        elif not barcode:
            error = "Item needs to have bar code"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO items(itemName, wholesalePrice, retailPrice, stock, barCode)'
                'VALUES (?, ?, ?, ?, ?)',(itemname, wholesaleprice, retailprice, stock, barcode)
            )
            db.commit()
            return redirect(url_for('items.index'))
    return render_template('items/create.html')


def get_item(item_id):
    item = get_db().execute(
        'SELECT id, itemName, wholesalePrice, retailPrice, stock, barCode FROM items WHERE id = ?', (item_id,)
    ).fetchone()

    if item is None:
        abort(404, f"Post id {item_id} doesn't exist.")

    """if not is_manager(g.user['id']):
        abort(403)"""

    return item


@bp.route('/<int:item_id>/update', methods=('GET', 'POST'))
@login_required
def update(item_id):

    item = get_item(item_id)

    if request.method == 'POST':
        itemname = request.form['itemName']
        wholesaleprice = request.form['wholesaleprice']
        retailprice = request.form['retailprice']
        stock = request.form['stock']
        barcode = request.form['barcode']
        error = None

        if not itemname:
            error = "Item name is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE items SET itemName = ?, wholesalePrice = ?, retailPrice = ?, stock = ?, barCode = ?'
                'WHERE id = ?', (itemname, wholesaleprice, retailprice, stock, barcode, item_id)
            )
            db.commit()
            return redirect(url_for('items.index'))

    return render_template('items/update.html', item=item)


@bp.route('/<int:item_id>/delete', methods=('POST',))
@login_required
def delete(item_id):
    get_item(item_id)
    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()
    return redirect(url_for('items.index'))


""""@bp.route('/<int:item_id>/info', methods=('POST', 'GET'))
@login_required
def info(item_id):

    item = get_item(item_id)"""

