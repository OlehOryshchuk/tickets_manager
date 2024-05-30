from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    current_app,
    request
)

from flask_login import current_user, login_required

from apps.models import Ticket, Roles, Group
from apps.forms import UpdateTicket, CreateTicket
from apps.utils import role_required, user_in_ticket_group
from apps import db


ticket_bl = Blueprint("ticket", __name__)


@ticket_bl.get("/tickets/")
@login_required
@role_required([Roles.admin, Roles.manager, Roles.analyst])
def list_ticket():
    """
    Get tickets from current user assigned groups
    or if you admin see all
    """
    page = request.args.get("page", 1, type=int)

    tickets = Ticket.query

    if current_user.role != Roles.admin:
        # admin can view everything
        # Get all groups the current user is assigned to
        user_groups = current_user.groups

        # Collect all tickets associated with these groups
        tickets = Ticket.query.join(Ticket.assigned_groups).filter(
            Group.id.in_([group.id for group in user_groups])
        )

    # paginate
    tickets = tickets.paginate(
        page=page,
        max_per_page=current_app.config.get("PAGINATION_MAX_PER_PAGE"),
        error_out=False,
    )
    return render_template(
        "tickets/ticket_list.html",
        tickets=tickets,
        pagination=tickets,
    )


@ticket_bl.get("/tickets/<int:ticket_id>")
@login_required
@role_required([Roles.admin, Roles.analyst, Roles.manager])
@user_in_ticket_group
def detail_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("tickets/ticket_detail.html", ticket=ticket)


@ticket_bl.route("/tickets/create", methods=["GET", "POST"])
@login_required
@role_required([Roles.admin])
def create_ticket():
    form = CreateTicket()

    if form.validate_on_submit():
        status = form.status.data
        note = form.note.data
        assigned_groups = form.assigned_groups.data
        assigned_user = form.assigned_user.data

        ticket = Ticket(status=status, note=note, assigned_user=assigned_user)
        ticket.assigned_groups.extend(assigned_groups)

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("ticket.list_ticket"))

    return render_template("tickets/ticket_form.html", form=form)


@ticket_bl.route("/tickets/<int:ticket_id>/update", methods=["GET", "POST"])
@login_required
@role_required([Roles.admin, Roles.analyst, Roles.manager])
@user_in_ticket_group
def update_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateTicket(obj=ticket)

    if form.validate_on_submit():
        ticket.status = form.status.data
        ticket.assigned_groups = form.assigned_groups.data
        ticket.assigned_user = form.assigned_user.data

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("ticket.detail_ticket", ticket_id=ticket_id))

    return render_template(
        "tickets/ticket_form.html",
        ticket=ticket,
        form=form
    )


@ticket_bl.delete("/tickets/<int:ticket_id>")
@login_required
@role_required([Roles.admin, Roles.analyst, Roles.manager])
@user_in_ticket_group
def delete_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()

    return redirect(url_for("ticket.list_ticket"))
