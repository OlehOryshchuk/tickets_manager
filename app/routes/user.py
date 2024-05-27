from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    current_app
)

from flask_login import (
    current_user,
    login_required
)

from app.models import User
from app.forms import UpdateUser
from app import db


user_bl = Blueprint("user", __name__)

# Endpoints for User model


@user_bl.get("/users/me")
@login_required
def view_me():
    return render_template("users/user_detail.html", user=current_user)


@user_bl.route("/users/me/edit", methods=["GET", "PATCH"])
@login_required
def update_me():
    form = UpdateUser(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user)
        db.session.commit()

        flash("Your changes have been saved.")
        return redirect(url_for("main:view_me"))
    return render_template("users/user_update.html", form=form)


@user_bl.get("/users/")
@login_required
def list_user():
    users = User.query.paginate(
        max_per_page=current_app.config.get("PAGINATION_MAX_PER_PAGE")
    )
    return render_template("users/user_list.html", users=users)


@user_bl.get("/users/<int:user_id>")
@login_required
def detail_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return render_template("users/user_detail.html", user=user)
