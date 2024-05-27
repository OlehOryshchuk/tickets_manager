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

from app.models import Ticket, Roles, Group
from app.forms import UpdateTickets
from app.utils import role_required, user_in_ticket_group
from app import db


ticket_bl = Blueprint("ticket", __name__)


@ticket_bl.get("/tickets/")
@login_required
@role_required([Roles.admin.value, Roles.manager.value, Roles.analyst.value])
def list_ticket():
    # Get all groups the current user is assigned to
    user_groups = current_user.groups

    # Collect all tickets associated with these groups
    ticket_query = Ticket.query.join(Ticket.assigned_groups).filter(
        Group.id.in_([group.id for group in user_groups])
    )

    tickets = ticket_query.paginate(
        max_per_page=current_app.config.get("PAGINATION_MAX_PER_PAGE")
    )

    return render_template("tickets/ticket_list.html", tickets=tickets)


@ticket_bl.get("/tickets/<int:ticket_id>")
@login_required
@role_required([Roles.admin.value, Roles.analyst.value, Roles.manager.value])
@user_in_ticket_group
def detail_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("tickets/ticket_detail.html", ticket=ticket)


@ticket_bl.patch("/tickets/<int:ticket_id>")
@login_required
@role_required([Roles.admin.value, Roles.analyst.value, Roles.manager.value])
@user_in_ticket_group
def update_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateTickets(obj=ticket)

    if form.validate_on_submit():
        ticket.status = form.status.data
        ticket.status = form.status.data
        ticket.assigned_groups = form.assigned_groups.data
        ticket.assigned_users = form.assigned_users.data

        db.session.add(ticket)
        db.session.commit()

        flash("Your changes have been saved.")
        return redirect(url_for("admin:list_ticket", ticket_id=ticket_id))

    return render_template("tickets/ticket_update.html", ticket=ticket)


@ticket_bl.delete("/tickets/<int:ticket_id>")
@login_required
@role_required([Roles.admin.value, Roles.analyst.value, Roles.manager.value])
@user_in_ticket_group
def delete_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()

    flash("Ticket has been deleted successfully", "success")
    return redirect(url_for("ticket:list_ticket"))
