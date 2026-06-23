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
from models.supplier import Supplier


suppliers_bp = Blueprint(
    "suppliers",
    __name__
)


@suppliers_bp.route("/suppliers")
@login_required
def suppliers():

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    suppliers_list = Supplier.query.order_by(
        Supplier.company_name
    ).all()

    return render_template(
        "suppliers/index.html",
        suppliers=suppliers_list
    )


@suppliers_bp.route(
    "/suppliers/add",
    methods=["GET", "POST"]
)
@login_required
def add_supplier():

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    if request.method == "POST":

        supplier = Supplier(
            company_name=request.form.get(
                "company_name"
            ),
            contact_person=request.form.get(
                "contact_person"
            ),
            phone=request.form.get(
                "phone"
            ),
            email=request.form.get(
                "email"
            ),
            comment=request.form.get(
                "comment"
            )
        )

        db.session.add(supplier)

        db.session.commit()

        return redirect(
            url_for("suppliers.suppliers")
        )

    return render_template(
        "suppliers/add.html"
    )


@suppliers_bp.route(
    "/suppliers/edit/<int:supplier_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_supplier(supplier_id):

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    supplier = Supplier.query.get_or_404(
        supplier_id
    )

    if request.method == "POST":

        supplier.company_name = request.form.get(
            "company_name"
        )

        supplier.contact_person = request.form.get(
            "contact_person"
        )

        supplier.phone = request.form.get(
            "phone"
        )

        supplier.email = request.form.get(
            "email"
        )

        supplier.comment = request.form.get(
            "comment"
        )

        db.session.commit()

        return redirect(
            url_for("suppliers.suppliers")
        )

    return render_template(
        "suppliers/edit.html",
        supplier=supplier
    )


@suppliers_bp.route(
    "/suppliers/delete/<int:supplier_id>"
)
@login_required
def delete_supplier(supplier_id):

    if current_user.role == "user":

        return redirect(
            url_for("products.products")
        )

    supplier = Supplier.query.get_or_404(
        supplier_id
    )

    db.session.delete(supplier)

    db.session.commit()

    return redirect(
        url_for("suppliers.suppliers")
    )