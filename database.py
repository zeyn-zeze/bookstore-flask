# database.py

from extensions import db
from app import create_app

app = create_app()

def create_tables():
    with app.app_context():
        db.create_all()
        print("✅ Database tables have been created successfully.")

def drop_tables():
    with app.app_context():
        db.drop_all()
        print("🗑️Database tables were deleted successfully.")
