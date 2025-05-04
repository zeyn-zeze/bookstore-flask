from flask import Blueprint, abort, request, redirect, url_for, flash, session, render_template
from models.CartItem import CartItem
from models.Book import Book
from extensions import db
from models.Order import Order
from models.OrderItem import OrderItem

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/add/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    if 'user_id' not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for('auth.login'))

    existing = CartItem.query.filter_by(user_id=session['user_id'], book_id=book_id).first()
    if existing:
        existing.quantity += 1
    else:
        new_item = CartItem(user_id=session['user_id'], book_id=book_id, quantity=1)
        db.session.add(new_item)

    db.session.commit()
    flash("Book added to cart!", "success")
    return redirect(url_for('book.book_details', book_id=book_id))


@cart_bp.route('/view')
def view_cart():
    if 'user_id' not in session:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for('auth.login'))

    items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.book.price * item.quantity for item in items)
    return render_template('cart.html', items=items, total=total)


@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != session.get('user_id'):
        flash("You are not authorized to perform this action.", "danger")
        return redirect(url_for('cart.view_cart'))

    db.session.delete(item)
    db.session.commit()
    flash("Book removed from cart.", "success")
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/increase/<int:item_id>', methods=['POST'])
def increase_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == session.get('user_id'):
        item.quantity += 1
        db.session.commit()
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/decrease/<int:item_id>', methods=['POST'])
def decrease_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == session.get('user_id'):
        if item.quantity > 1:
            item.quantity -= 1
            db.session.commit()
        else:
            flash("Minimum quantity is 1", "warning")
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get('user_id')
    if not user_id:
        abort(403)

    items = CartItem.query.filter_by(user_id=user_id).all()
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart.view_cart'))

    # Yeni siparişi oluştur
    order = Order(user_id=user_id)
    db.session.add(order)
    db.session.flush()  # order.id'ye ulaşmak için

    # Her bir sepet öğesini sipariş öğesine çevir
    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            book_id=item.book_id,
            quantity=item.quantity,
            total_price=item.book.price * item.quantity
        )
        db.session.add(order_item)
        db.session.delete(item)  # Sepetten sil

    db.session.commit()
    flash("Purchase completed successfully!", "success")
    return render_template("cart.html", items=[], total=0, checkout_success=True)



