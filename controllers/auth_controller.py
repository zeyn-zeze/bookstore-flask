from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.User import User
from extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')  

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = request.form['phone']
        address = request.form.get('address')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        user = User.query.filter((User.username == username) | (User.email == email)).first()
        if user:
            flash('Username or email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email, phone=phone,address=address)
        new_user.set_password(password)
        new_user.role = 'user'
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Successful login!', 'success')

            if user.role == 'admin':
                return redirect(url_for('book.admin_home'))
            else:
                return redirect(url_for('book.index'))
        else:
            flash('Incorrect username or password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        flash('Access denied: Admins only!', 'danger')
        return redirect(url_for('book.index'))

    return redirect(url_for('book.admin_home'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('book.index'))

