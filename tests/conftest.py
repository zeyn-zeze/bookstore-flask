import os
import sys
import pytest

# PYTHONPATH düzenle (test dizininden ana dizine erişim için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app  # ← burası düzeldi
from extensions import db
from config import Config


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI":"mysql+pymysql://root:Zeynep5703?@localhost/book_store_test", 
        "WTF_CSRF_ENABLED": False,  
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        

@pytest.fixture
def client(app):
    return app.test_client()
