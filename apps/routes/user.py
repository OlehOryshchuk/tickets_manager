from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    request,
)

from flask_login import current_user, login_required

from apps.models import User, Group, Roles
from apps.forms import UpdateUser, AdminUpdateUser
from apps import db
from apps.utils import role_required


user_bl = Blueprint("user", __name__)

# Endpoints for User model


@user_bl.get("/")
def index():
    return "Hello"


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
        return redirect(url_for("main.view_me"))
    return render_template("users/user_form.html", form=form)


@user_bl.get("/users/")
@login_required
def list_user():
    page = request.args.get("page", 1, type=int)
    group_id = request.args.get("group_id", type=int)
    users = User.query

    if group_id:
        # filter users by group id
        users = users.filter(User.groups.any(Group.id == group_id))

    users = users.paginate(
        page=page,
        max_per_page=current_app.config.get("PAGINATION_MAX_PER_PAGE"),
        error_out=False,
    )

    return render_template(
        "users/user_list.html",
        users=users,
        # passing users again for pagination
        pagination=users,
    )


@user_bl.get("/users/<int:user_id>")
@login_required
def detail_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return render_template("users/user_detail.html", user=user)


@user_bl.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
@role_required([Roles.admin])
def update_user(user_id: int):
    """ "Admin can fully update user and their role"""
    user = User.query.get_or_404(user_id)
    form = AdminUpdateUser(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.role = form.role.data

        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for("user.detail_user", user_id=user_id))

    return render_template("users/user_form.html", form=form, user=user)


@user_bl.delete("/users/<int:user_id>")
@login_required
@role_required([Roles.admin])
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("user.list_user"))
