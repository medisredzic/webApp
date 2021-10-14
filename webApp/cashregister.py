import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, Flask
)

from werkzeug.exceptions import abort

from webApp.auth import login_required, is_manager
from webApp.db import get_db
from webApp.items import get_item

bp = Blueprint('cashregister', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = None

    bill_id = session.get('bill_id')

    if bill_id is None:
        pass
    else:
        #items = db.execute("SELECT * FROM itemsSold WHERE billId = ?", (bill_id,))
        items = db.execute("SELECT items.itemName, itemsSold.id, itemsSold.billId, itemsSold.soldAt, itemsSold.stock"
                           " FROM itemsSold"
                           " INNER JOIN items ON items.id = itemsSold.itemId"
                           " WHERE itemsSold.billId = ?", (bill_id,))
        db.commit()

    return render_template('cashregister/index.html', items=items)


@bp.route('/register', methods=('GET', 'POST'))
@login_required
def add():

    db = get_db()

    bill_id = session.get('bill_id')

    if request.method == 'POST':
        itemid = request.form['itemid']
        stock = request.form['stock']
        error = None

        if not itemid:
            error = "You need to enter id or barcode"

        item = get_item(itemid)

        if item['stock'] > 0:
            if not stock:
                stock = 1
        else:
            error("Item is not in stock, contact your manager")

        if error is not None:
            flash(error)
        else:
            if bill_id is None:
                db.execute("INSERT INTO bills(cashier) VALUES (?)", (g.user['id'],))
                db.commit()
                bill_id = db.execute("SELECT id FROM bills ORDER BY id DESC LIMIT 1").fetchone()

                session['bill_id'] = None
                session['bill_id'] = bill_id[0]

                db.execute("INSERT INTO itemsSold(billId, itemId, soldAt, stock) VALUES (?, ?, ?, ?)",
                           (bill_id[0], itemid, item['retailPrice'], stock))
                db.commit()
            else:
                bill_id = session['bill_id']

                db.execute("INSERT INTO itemsSold(billId, itemId, soldAt, stock) VALUES (?, ?, ?, ?)",
                           (bill_id, itemid, item['retailPrice'], stock))
                db.commit()

    return render_template('cashregister/add.html')


@bp.route('/finish', methods=('GET', 'POST'))
@login_required
def finish():

    finishl = {}  # Used to pass last information to the template
    bill_id = session['bill_id']  # Fetch bill_id session
    calc_price = 0
    error = None

    if bill_id is None:
        error = "You haven't added any items."

    if error is None:
        db = get_db()
        rows = db.execute("SELECT * FROM itemsSold WHERE billId = ?", (bill_id,)).fetchall()

        for n in range(len(rows)):
            item_info = get_item(rows[n]['itemId'])
            stock = item_info['stock']

            stock = stock - rows[n]['stock']

            calc_price = calc_price + (rows[n]['soldAt'] * rows[n]['stock'])

            db.execute("UPDATE items SET stock = ? WHERE id = ?", (stock, rows[n]['itemId']))
            db.commit()

        finishl['lastPrice'] = calc_price

        session['bill_id'] = None

    flash(error)

    return render_template('cashregister/finish.html', finishl=finishl)