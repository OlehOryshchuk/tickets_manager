from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    url_for,
    flash
)
from flask_login import login_user, logout_user

from app.models import User
from . import login_manager, db

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def user_loader(user_id: str):
    return User.query.get(id=int(user_id))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User()

        # hash password
        user.set_password(password)
        user.username = username

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth:login"))
    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.get(username=username)

        if user.check_password(password):
            login_user(user)
            return redirect(url_for("main:index"))
        else:
            flash("Invalid credentials")
    return render_template("auth/login.html")


@auth.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth:logout"))
