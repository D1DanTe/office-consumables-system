from datetime import datetime

from models import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    unit = db.Column(
        db.String(50),
        nullable=False
    )

    current_stock = db.Column(
        db.Integer,
        default=0
    )

    min_stock = db.Column(
        db.Integer,
        default=0
    )

    description = db.Column(
        db.Text
    )

    comment = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )