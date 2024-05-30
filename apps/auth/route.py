from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_user, logout_user

from apps.models import User
from .forms import LoginForm, CreateAccountForm
from apps import db
from apps.utils import verify_pass, hash_pass

auth_bl = Blueprint("auth", __name__)


@auth_bl.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)

    if login_form.validate_on_submit():

        # read form data
        username = login_form.username.data
        password = login_form.password.data
        remember = login_form.remember.data

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(
            stored_password=user.password, provided_password=password
        ):
            login_user(user, remember=remember)

            return redirect(url_for("user.view_me"))

        # Something (user or pass) is not ok
        return render_template(
            "auth/login.html", msg="Wrong user or password", form=login_form
        )

    return render_template("auth/login.html", form=login_form)


@auth_bl.route("/register", methods=["GET", "POST"])
def register():
    create_account_form = CreateAccountForm(request.form)
    if create_account_form.validate_on_submit():

        username = create_account_form.username.data
        password = create_account_form.password.data

        # Check username exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template(
                "auth/register.html",
                msg="Username already registered",
                success=False,
                form=create_account_form,
            )

        # else we can create the user
        user = User(username=username, password=hash_pass(password))

        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template(
            "auth/register.html",
            msg="Account created successfully.",
            success=True,
            form=create_account_form,
        )

    return render_template("auth/register.html", form=create_account_form)


@auth_bl.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
