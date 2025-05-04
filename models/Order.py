# models/order.py
from extensions import db
from datetime import datetime

from models.OrderItem import OrderItem

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ordered_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(lambda: OrderItem, backref="order", cascade="all, delete-orphan")

