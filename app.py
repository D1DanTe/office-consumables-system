from flask import Flask, render_template

from flask_login import (
    LoginManager,
    login_required,
    current_user
)

from config import Config
from models import db
from models.user import User
from models.product import Product
from models.request import Request
from models.supplier import Supplier

from routes.auth import auth_bp
from routes.products import products_bp
from routes.purchase import purchase_bp
from routes.requests import requests_bp
from routes.receipts import receipts_bp
from routes.suppliers import suppliers_bp
from routes.users import users_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"

app.register_blueprint(auth_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(products_bp)
app.register_blueprint(requests_bp)
app.register_blueprint(receipts_bp)
app.register_blueprint(suppliers_bp)
app.register_blueprint(users_bp)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_new_requests():

    if current_user.is_authenticated:

        new_requests_count = Request.query.filter_by(
            status="Новая"
        ).count()

        return dict(
            new_requests_count=new_requests_count
        )

    return dict(
        new_requests_count=0
    )


@app.route("/dashboard")
@login_required
def dashboard():

    total_products = Product.query.count()

    total_requests = Request.query.count()

    new_requests = Request.query.filter_by(
        status="Новая"
    ).count()

    latest_requests = Request.query.filter_by(
        status="Новая"
    ).order_by(
        Request.id.desc()
    ).limit(5).all()

    purchase_needed = Product.query.filter(
        Product.current_stock <= Product.min_stock
    ).count()

    total_suppliers = Supplier.query.count()

    return render_template(
        "dashboard/index.html",
        user_name=current_user.get_full_name(),
        role=current_user.role,
        total_products=total_products,
        total_requests=total_requests,
        new_requests=new_requests,
        purchase_needed=purchase_needed,
        total_suppliers=total_suppliers,
        latest_requests=latest_requests
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )