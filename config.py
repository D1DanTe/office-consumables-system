import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "office-supply-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'database', 'office.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False