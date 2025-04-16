from flask import Blueprint, render_template, request, redirect, url_for, session
from app.model.User import User

auth_bp = Blueprint('auth', __name__)


users = {} # draft database

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)

        if user and user.password == password:
            session['user'] = email
            return redirect(url_for('auth.home'))
        return "Login Failed", 401
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            return "Already Registered", 400
        users[email] = User(email, password)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
