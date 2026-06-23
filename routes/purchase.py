from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from models.product import Product


purchase_bp = Blueprint(
    "purchase",
    __name__
)


@purchase_bp.route("/purchase")
@login_required
def purchase():

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    products = Product.query.filter(
        Product.current_stock <= Product.min_stock
    ).all()

    return render_template(
        "purchase/index.html",
        products=products
    )