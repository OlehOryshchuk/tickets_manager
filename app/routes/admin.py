from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from app.models import User, Group, Roles, Ticket
from app.utils import role_required
from app.forms import UpdateUser, UpdateGroup
from app import db

admin_bl = Blueprint("user", __name__)

# All routes are available for admin
# so I created this model for this

# Admin Manage Users


@admin_bl.route("admin/users/<int:user_id>", methods=["GET", "PATCH"])
@login_required
@role_required(["Admin"])
def update_user(user_id: int):
    user = User.query.get_or_404(user_id)
    form = UpdateUser(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.role = form.role.data

        db.session.add(current_user)
        db.session.commit()

        flash("Your changes have been saved.")
        return redirect(url_for("user:detail_user", user_id=user_id))

    return render_template("users/user_update.html", form=form)


@admin_bl.delete("admin/users/<int:user_id>")
@login_required
@role_required(["Admin"])
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("User has been deleted successfully", "success")
    return redirect(url_for("user:list_user"))

# Admin Manager Groups


@admin_bl.get("admin/groups/")
@login_required
@role_required([Roles.admin.value])
def list_group():
    groups = Group.query.all()
    return render_template("groups/group_list.html", groups=groups)


@admin_bl.get("admin/groups/<int:group_id>")
@login_required
@role_required([Roles.admin.value])
def detail_group(group_id: int):
    group = Group.query.get_or_404(group_id)
    return render_template("groups/group_detail.html", group=group)


@admin_bl.route("admin/groups/<int:group_id>")
@login_required
@role_required(["Admin"])
def update_group(group_id: int):
    group = Group.query.get_or_404(group_id)
    form = UpdateGroup(obj=group)

    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        group.users = form.users.data

        db.session.add(group)
        db.session.commit()

        flash("Your changes have been saved.")
        return redirect(url_for("admin:list_group", group_id=group_id))

    return render_template("groups/group_update.html", form=form)


@admin_bl.delete("/groups/<int:group_id>")
@login_required
@role_required(["Admin"])
def delete_group(group_id: int):
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()

    flash("Group has been deleted successfully", "success")
    return redirect(url_for("main:list_group"))


# Admin Manage Tickets

@admin_bl.get("admin/tickets/")
@login_required
@role_required([Roles.admin.value])
def list_ticket():
    tickets = Ticket.query.all()
    return render_template("tickets/ticket_list.html", tickets=tickets)
