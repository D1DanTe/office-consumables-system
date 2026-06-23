from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.product import Product
from sqlalchemy import func


products_bp = Blueprint(
    "products",
    __name__
)


@products_bp.route("/products")
@login_required
def products():

    search = request.args.get(
        "search",
        ""
    )

    products_list = Product.query.order_by(
        Product.name
    ).all()

    if search:

        search_lower = search.lower()

        products_list = [
            product
            for product in products_list
            if search_lower in product.name.lower()
        ]

    return render_template(
        "products/index.html",
        products=products_list,
        search=search
    )


@products_bp.route(
    "/products/add",
    methods=["GET", "POST"]
)
@login_required
def add_product():

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    if request.method == "POST":

        product = Product(
            name=request.form.get("name"),
            unit=request.form.get("unit"),
            current_stock=int(
                request.form.get("current_stock")
            ),
            min_stock=int(
                request.form.get("min_stock")
            ),
            description=request.form.get(
    "description"
),
comment=request.form.get(
    "comment"
)
        )

        db.session.add(product)

        db.session.commit()

        return redirect(
            url_for("products.products")
        )

    return render_template(
        "products/add.html"
    )


@products_bp.route(
    "/products/edit/<int:product_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_product(product_id):

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    product = Product.query.get_or_404(
        product_id
    )

    if request.method == "POST":

        product.name = request.form.get(
            "name"
        )

        product.unit = request.form.get(
            "unit"
        )

        product.current_stock = int(
            request.form.get(
                "current_stock"
            )
        )

        product.min_stock = int(
            request.form.get(
                "min_stock"
            )
        )

        product.description = request.form.get(
            "description"
        )

        product.comment = request.form.get(
    "comment"
)

        db.session.commit()

        return redirect(
            url_for("products.products")
        )

    return render_template(
        "products/edit.html",
        product=product
    )


@products_bp.route(
    "/products/delete/<int:product_id>"
)

@login_required
def delete_product(product_id):

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    product = Product.query.get_or_404(
        product_id
    )

    product = Product.query.get_or_404(
        product_id
    )

    db.session.delete(product)

    db.session.commit()

    return redirect(
        url_for("products.products")
    )