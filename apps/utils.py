import os
import binascii
import hashlib

from typing import Callable
from functools import wraps

from flask_login import current_user
from flask import abort
from werkzeug.exceptions import HTTPException

from apps import bcrypt
from apps.models import Roles, Ticket


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
                abort(403)
            return func(*args, **kwargs)

        return view

    return wrapper


def user_in_ticket_group(func: Callable) -> Callable:
    """
    Verify if current user is assigned to Group to which
    ticket_id belongs to
    :param view_func:
    :return:
    """

    @wraps(func)
    def view(*args, **kwargs) -> Callable | HTTPException:
        ticket_id = kwargs.get("ticket_id")
        ticket = Ticket.query.get(ticket_id)

        if current_user.role != Roles.admin and not any(
                group in current_user.groups
                for group in ticket.assigned_groups
        ):
            abort(
                403,
                description=(
                    "You are not assigned to group"
                    " which this ticket belongs to"
                ),
            )

        return func(*args, **kwargs)

    return view


def hash_pass(password):
    """Hash a password for storing."""
    return bcrypt.generate_password_hash(password).decode("utf-8")


def verify_pass(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    return bcrypt.check_password_hash(
        pw_hash=stored_password, password=provided_password
    )
