import base64
from enums.genre import GENRES
from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.Book import Book
from extensions import db

book_bp = Blueprint('book', __name__)


@book_bp.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@book_bp.route('/book_details/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_details.html', book=book)


@book_bp.route('/dashboard/')
def admin_home():
    books = Book.query.all()
    return render_template('dashboard/home.html', books=books)


@book_bp.route('/dashboard/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form.get('description')
        genre = request.form['genre']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        image = request.files.get('image')
        image_data = base64.b64encode(image.read()).decode('utf-8') if image else None

        new_book = Book(
            title=title,
            author=author,
            description=description,
            genre=genre,
            price=price,
            stock=stock,
            image_data=image_data
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('book.admin_home'))  

    return render_template('dashboard/add_book.html', genres=GENRES)  



@book_bp.route('/dashboard/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.description = request.form.get('description')
        book.genre = request.form['genre']
        book.price = float(request.form['price'])
        book.stock = int(request.form['stock'])

        image = request.files.get('image')
        if image and image.filename != '':
            book.image_data = base64.b64encode(image.read()).decode('utf-8')

        db.session.commit()
        return redirect(url_for('book.admin_home'))

    return render_template('dashboard/update_book.html', book=book,genres=GENRES)


@book_bp.route('/dashboard/delete_book/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book.admin_home'))
