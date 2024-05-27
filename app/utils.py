from typing import Callable
from functools import wraps

from flask_login import (
    current_user
)
from flask import (
    flash,
    abort
)
from werkzeug.exceptions import HTTPException
from sqlalchemy import text

from app import db
from app.models import Roles


def role_required(roles: list[str | Roles]) -> Callable:
    """
    Decorator for implementing RBAC
    :param roles:
    :return:
    """
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def view(*args, **kwargs) -> Callable | HTTPException:
            if current_user.role not in roles:
                flash("You do not have access!")
                abort(403)
            return func(*args, **kwargs)
        return view
    return wrapper


def user_in_ticket_group(func: Callable) -> Callable:
    """
    Verify if current user is assigned to Group to which
    ticket_id belongs to
    :param func:
    :return:
    """
    @wraps(func)
    def view(*args, **kwargs) -> Callable | HTTPException:
        ticket_id = kwargs.get("ticket_id")
        user_groups_id = (group.id for group in current_user.groups)

        query = text("""
            SELECT COUNT(*)
            FROM group_tickets gt
            JOIN group g ON g.id = gt.group_id
            WHERE gt.ticket_id = :ticket_id
            AND g.id IN :user_groups_id
        """)

        result = db.session.execute(
            query,
            {"ticket_id": ticket_id, "user_groups_id": user_groups_id}
        ).scalar()

        if result == 0:
            abort(
                403,
                description=(
                    "You are not assigned to group"
                    " which this ticket belongs to"
                )
            )

        return func(*args, **kwargs)
    return view
