from datetime import datetime

from models import db


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_name = db.Column(
        db.String(255),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    unit = db.Column(
        db.String(50),
        nullable=False
    )

    comment = db.Column(
        db.Text
    )

    created_by = db.Column(
    db.String(255),
    nullable=False
)

    status = db.Column(
        db.String(50),
        default="Новая"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )