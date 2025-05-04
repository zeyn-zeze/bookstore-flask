import pytest
from models.Book import Book
from extensions import db


@pytest.fixture
def book_factory(app):  # sadece app kullan, client değil!
    def _create(title="Test Book", genre="Fiction", author="Author", price=10.0, stock=5):
        book = Book(
            title=title,
            genre=genre,
            author=author,
            description="Sample",
            price=price,
            stock=stock
        )
        db.session.add(book)
        db.session.commit()
        return book
    return _create



# 1. Ana sayfa yüklüyor mu?
def test_index_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Genres" in response.data


# 2. Arama sonuç döndürüyor mu?
def test_search_book_shows_result(client, book_factory):
    book = book_factory(title="Flask 101")
    response = client.get('/?search=Flask')
    assert book.title.encode() in response.data


# 3. Kitap detayları doğru dönüyor mu?
def test_book_details_page(client, book_factory):
    book = book_factory(title="Detail Book")
    url = f'/book_details/{book.id}'
    response = client.get(url)
    assert response.status_code == 200
    assert b"Detail Book" in response.data



# 4. Geçersiz kitap ID’si 404 dönmeli
def test_book_details_invalid_id(client):
    response = client.get('/book_details/999999')
    assert response.status_code == 404


# 5. Tür filtresi çalışıyor mu?
def test_genre_filter_works(client, book_factory):
    book = book_factory(title="Science Book", genre="Science")
    response = client.get('/?genre=Science')
    assert response.status_code == 200
    assert book.title.encode() in response.data
