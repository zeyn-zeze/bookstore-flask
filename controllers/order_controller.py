# order.py
from flask import Blueprint, render_template, session
from models.Order import Order
from extensions import db

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/history')
def history():
    user_id = session.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.ordered_at.desc()).all()
    return render_template('order_history.html', orders=orders)

