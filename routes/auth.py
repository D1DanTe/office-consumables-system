from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    login_user,
    logout_user
)

from models.user import User
from services.auth_service import verify_password

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter_by(
            login=login
        ).first()

        if user and verify_password(
            password,
            user.password_hash
        ):
            login_user(user)

            return redirect(
                url_for("dashboard")
            )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )