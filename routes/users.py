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
from models.user import User

from werkzeug.security import (
    generate_password_hash
)


users_bp = Blueprint(
    "users",
    __name__
)


@users_bp.route("/users")
@login_required
def users():

    if current_user.role != "super_admin":

        return redirect(
            url_for("products.products")
        )

    users_list = User.query.order_by(
        User.last_name
    ).all()

    return render_template(
        "users/index.html",
        users=users_list
    )


@users_bp.route(
    "/users/add",
    methods=["GET", "POST"]
)
@login_required
def add_user():

    if current_user.role != "super_admin":

        return redirect(
            url_for("products.products")
        )

    if request.method == "POST":

        user = User(
            first_name=request.form.get(
                "first_name"
            ),
            last_name=request.form.get(
                "last_name"
            ),
            login=request.form.get(
                "login"
            ),
            password_hash=generate_password_hash(
                request.form.get(
                    "password"
                )
            ),
            role=request.form.get(
                "role"
            ),
            status="active"
        )

        db.session.add(user)

        db.session.commit()

        return redirect(
            url_for("users.users")
        )

    return render_template(
        "users/add.html"
    )


@users_bp.route(
    "/users/edit/<int:user_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_user(user_id):

    if current_user.role != "super_admin":

        return redirect(
            url_for("products.products")
        )

    user = User.query.get_or_404(
        user_id
    )

    if request.method == "POST":

        user.first_name = request.form.get(
            "first_name"
        )

        user.last_name = request.form.get(
            "last_name"
        )

        user.login = request.form.get(
            "login"
        )

        user.role = request.form.get(
            "role"
        )

        db.session.commit()

        return redirect(
            url_for("users.users")
        )

    return render_template(
        "users/edit.html",
        user=user
    )


@users_bp.route(
    "/users/status/<int:user_id>/<status>"
)
@login_required
def change_status(
    user_id,
    status
):

    if current_user.role != "super_admin":

        return redirect(
            url_for("products.products")
        )

    user = User.query.get_or_404(
        user_id
    )

    user.status = status

    db.session.commit()

    return redirect(
        url_for("users.users")
    )
@users_bp.route(
    "/users/delete/<int:user_id>"
)
@login_required
def delete_user(user_id):

    if current_user.role != "super_admin":

        return redirect(
            url_for("products.products")
        )

    user = User.query.get_or_404(
        user_id
    )

    # защита от удаления самого себя
    if user.id == current_user.id:

        return redirect(
            url_for("users.users")
        )

    db.session.delete(user)

    db.session.commit()

    return redirect(
        url_for("users.users")
    )