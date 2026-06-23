from datetime import datetime

from models import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_name = db.Column(
        db.String(255),
        nullable=False
    )

    contact_person = db.Column(
        db.String(255)
    )

    phone = db.Column(
        db.String(50)
    )

    email = db.Column(
        db.String(255)
    )

    comment = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )