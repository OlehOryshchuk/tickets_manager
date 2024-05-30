from flask import (
    Blueprint,
    render_template,
    abort,
    current_app,
    redirect,
    url_for,
    request,
)

from flask_login import login_required, current_user

from apps import db
from apps.models import Group, Roles, Ticket
from apps.forms import UpdateGroup, CreateGroup

from apps.utils import role_required


group_bl = Blueprint("group", __name__)

# Endpoints for Group model


@group_bl.get("/groups/")
@login_required
@role_required([Roles.admin])
def list_group():
    page = request.args.get("page", 1, type=int)
    ticket_id = request.args.get("ticket_id", type=int)

    groups = Group.query

    if current_user.role.value != "Admin":
        # only admin can manager all groups,
        # others only to the one they were assigned to
        groups = groups.filter(Group.users.contains(current_user))

    if ticket_id:
        # filter groups who are assign to the ticket_id
        groups = groups.filter(Group.tickets.any(Ticket.id == ticket_id))

    # paginate
    groups = groups.paginate(
        page=page,
        max_per_page=current_app.config.get("PAGINATION_MAX_PER_PAGE"),
        error_out=False,
    )
    return render_template(
        "groups/group_list.html",
        groups=groups,
        # passing groups again for pagination
        pagination=groups,
    )


@group_bl.route("/groups/create", methods=["GET", "POST"])
@login_required
@role_required([Roles.admin])
def create_group():
    form = CreateGroup()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        users = form.users.data

        group = Group(
            name=name,
            description=description,
            users=users,
        )
        db.session.add(group)
        db.session.commit()

        return redirect(url_for("group.list_group"))

    return render_template("groups/group_form.html", form=form)


@group_bl.get("/groups/<int:group_id>")
@login_required
@role_required([Roles.admin, Roles.analyst, Roles.manager])
def detail_group(group_id: int):
    if current_user.role == Roles.admin:
        group = Group.query.filter_by(id=group_id).first()

    else:
        group = Group.query.filter(
            Group.id == group_id, Group.users.any(id=current_user.id)
        ).first()

    if not group:
        abort(
            403,
            description=(
                "You are not assigned for this group"
                " or group does not exist")
        )

    return render_template(
        "groups/group_detail.html",
        group=group
    )


@group_bl.get("/admin/groups/<int:group_id>")
@login_required
@role_required([Roles.admin])
def admin_detail_group(group_id: int):
    group = Group.query.filter_by(id=group_id).first()

    if not group:
        abort(404, description="Does not exist")

    return render_template(
        "groups/group_detail.html",
        group=group
    )


@group_bl.route("/groups/<int:group_id>/update", methods=["GET", "POST"])
@login_required
@role_required([Roles.admin])
def update_group(group_id: int):
    group = Group.query.get_or_404(group_id)
    form = UpdateGroup(obj=group)

    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        group.users = form.users.data

        db.session.add(group)
        db.session.commit()

        return redirect(url_for("admin.detail_group", group_id=group_id))

    return render_template("groups/group_form.html", form=form, group=group)


@group_bl.delete("/groups/<int:group_id>")
@login_required
@role_required([Roles.admin])
def delete_group(group_id: int):
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()

    return redirect(url_for("group.list_group"))
