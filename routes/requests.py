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
from models.request import Request
from models.product import Product


requests_bp = Blueprint(
    "requests",
    __name__
)


@requests_bp.route("/requests")
@login_required
def requests():

    if current_user.role == "user":

        requests_list = Request.query.filter_by(
            created_by=current_user.get_full_name()
        ).order_by(
            Request.id.desc()
        ).all()

    else:

        requests_list = Request.query.order_by(
            Request.id.desc()
        ).all()

    stock_data = {}

    for request_item in requests_list:

        product = Product.query.filter_by(
            name=request_item.product_name
        ).first()

        if product:

            stock_data[request_item.id] = (
                product.current_stock
            )

        else:

            stock_data[request_item.id] = 0

    return render_template(
        "requests/index.html",
        requests=requests_list,
        stock_data=stock_data
    )


@requests_bp.route(
    "/requests/add",
    methods=["GET", "POST"]
)
@login_required
def add_request():

    products = Product.query.order_by(
        Product.name
    ).all()

    if request.method == "POST":

        product_name = request.form.get(
            "product_name"
        )

        custom_product = request.form.get(
            "custom_product"
        )

        custom_unit = request.form.get(
            "custom_unit"
        )

        # если пользователь ввел свой товар
        if custom_product and custom_product.strip():

            product_name = custom_product.strip()
            unit = custom_unit.strip() if custom_unit else ""

        # если выбран товар из каталога
        else:

            product = Product.query.filter_by(
                name=product_name
            ).first()
            unit = product.unit if product else ""

        new_request = Request(
            product_name=product_name,
            quantity=int(
                request.form.get(
                    "quantity"
                )
            ),
            unit=unit,
            comment=request.form.get(
                "comment"
            ),
            created_by=current_user.get_full_name()
        )

        db.session.add(new_request)
        db.session.commit()

        return redirect(
            url_for("requests.requests")
        )

    return render_template(
        "requests/add.html",
        products=products
    )


@requests_bp.route(
    "/requests/status/<int:request_id>/<status>"
)
@login_required
def change_status(
    request_id,
    status
):

    if current_user.role == "user":

        return redirect(
            url_for("requests.requests")
        )

    request_item = Request.query.get_or_404(
        request_id
    )

    if request_item.status == "Выдана":
        return redirect(
            url_for("requests.requests")
        )

    request_item.status = status

    db.session.commit()

    return redirect(
        url_for("requests.requests")
    )


@requests_bp.route(
    "/requests/issue/<int:request_id>"
)
@login_required
def issue_request(request_id):

    if current_user.role == "user":

        return redirect(
            url_for("requests.requests")
        )

    request_item = Request.query.get_or_404(
        request_id
    )

    # защита от повторной выдачи
    if request_item.status == "Выдана":

        return redirect(
            url_for("requests.requests")
        )

    product = Product.query.filter_by(
        name=request_item.product_name
    ).first()

    # товар не найден
    if not product:

        return redirect(
            url_for("requests.requests")
        )

    # недостаточно остатка
    if product.current_stock < request_item.quantity:

        return redirect(
            url_for("requests.requests")
        )

    # списание товара
    product.current_stock -= request_item.quantity

    # изменение статуса
    request_item.status = "Выдана"

    db.session.commit()

    return redirect(
        url_for("requests.requests")
    )

@requests_bp.route(
    "/requests/delete/<int:request_id>"
)
@login_required
def delete_request(request_id):

    if current_user.role != "super_admin":

        return redirect(
            url_for("requests.requests")
        )

    request_item = Request.query.get_or_404(
        request_id
    )

    db.session.delete(request_item)

    db.session.commit()

    return redirect(
        url_for("requests.requests")
    )