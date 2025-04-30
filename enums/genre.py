# enums/genre.py
from sqlalchemy.dialects.mysql import ENUM

GENRES = (
    'Fiction',
    'Non-Fiction',
    'Fantasy',
    'Science',
    'Biography',
    'Mystery',
    'Romance',
    'History'
)

genre_enum = ENUM(*GENRES, name='genre_enum')
