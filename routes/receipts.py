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
from models.receipt import Receipt
from models.product import Product


receipts_bp = Blueprint(
    "receipts",
    __name__
)


@receipts_bp.route("/receipts")
@login_required
def receipts():

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    receipts_list = Receipt.query.order_by(
        Receipt.id.desc()
    ).all()

    return render_template(
        "receipts/index.html",
        receipts=receipts_list
    )


@receipts_bp.route(
    "/receipts/add",
    methods=["GET", "POST"]
)
@login_required
def add_receipt():

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    if request.method == "POST":

        product_name = request.form.get(
            "product_name"
        )

        quantity = int(
            request.form.get(
                "quantity"
            )
        )

        product = Product.query.filter_by(
            name=product_name
        ).first()

        if not product:

            return render_template(
                "receipts/add.html",
                error="Товар не найден в каталоге. Сначала добавьте его в раздел 'Товары'."
            )

        receipt = Receipt(
            product_name=product_name,
            quantity=quantity,
            unit=request.form.get(
                "unit"
            ),
            comment=request.form.get(
                "comment"
            ),
            created_by=current_user.get_full_name()
        )

        product.current_stock += quantity

        db.session.add(receipt)

        db.session.commit()

        return redirect(
            url_for("receipts.receipts")
        )

    return render_template(
        "receipts/add.html"
    )