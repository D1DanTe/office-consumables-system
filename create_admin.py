from app import app

from models import db
from models.user import User

from services.auth_service import hash_password


with app.app_context():

    admin = User.query.filter_by(
        login="admin"
    ).first()

    if not admin:

        admin = User(
            first_name="Данияр",
            last_name="Курбанов",
            login="admin",
            password_hash=hash_password(
                "admin123"
            ),
            role="super_admin",
            status="active"
        )

        db.session.add(admin)

        db.session.commit()

        print("Супер-админ создан")

    else:
        print("Админ уже существует")