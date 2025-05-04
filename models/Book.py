from extensions import db
from enums.genre import genre_enum
from sqlalchemy.dialects.mysql import LONGTEXT

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(genre_enum, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_data = db.Column(LONGTEXT, nullable=True)


    def __repr__(self):
        return f'<Book {self.title}>'
