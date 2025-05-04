from flask import Blueprint, abort, render_template, request, redirect, url_for, flash, session
from models.Order import Order
from models.User import User
from extensions import db

user_bp = Blueprint('user', __name__, url_prefix='/dashboard/users')

@user_bp.route('/', methods=['GET', 'POST'])
def manage_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Only admins can access this page.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if 'delete_user' in request.form:
            delete_id = int(request.form['delete_user'])
            user = User.query.get(delete_id)
            if user:
                db.session.delete(user)
                db.session.commit()
            flash('User deleted successfully.', 'success')
            return redirect(url_for('user.manage_users'))

        if 'add_user' in request.form:
            # Add new user
            new_user = User(
                username=request.form['new_username'],
                email=request.form['new_email'],
                phone=request.form['new_phone'],
                role=request.form['new_role']
            )
            new_user.set_password(request.form['new_password'])
            db.session.add(new_user)
            db.session.commit()
            flash('New user added successfully.', 'success')
            return redirect(url_for('user.manage_users'))

        if 'user_id' in request.form:
            # Update existing user
            user = User.query.get(int(request.form['user_id']))
            if user:
                user.username = request.form['username']
                user.email = request.form['email']
                user.phone = request.form['phone']
                user.role = request.form['role']
                
                if request.form.get('password'):  # Yeni şifre yazılmışsa
                    user.set_password(request.form['password'])

                db.session.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('user.manage_users'))

    users = User.query.all()
    return render_template('dashboard/manage_user.html', users=users)

@user_bp.route('/info')
def user_info():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.ordered_at.desc()).all()
    return render_template("user_info.html", user=user, orders=orders)