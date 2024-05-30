from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import (
    QuerySelectMultipleField,
    QuerySelectField
)
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectField,
)
from wtforms.validators import (
    Length,
)

from apps.models import Roles, User, Group, Status


class UpdateUser(FlaskForm):
    username = StringField("Username", validators=[Length(max=250)])
    submit = SubmitField("Update")


class AdminUpdateUser(UpdateUser):
    role = SelectField(
        "Roles",
        choices=[(role.name, role.value) for role in Roles]
    )


class UpdateGroup(FlaskForm):
    name = StringField("Name", validators=[Length(max=250)])
    description = TextAreaField("Description")
    users = QuerySelectMultipleField(
        "Users", query_factory=lambda: User.query, get_label="username"
    )
    submit = SubmitField("Update")


class CreateGroup(UpdateGroup):
    pass


class UpdateTicket(FlaskForm):
    status = SelectField(
        "Status",
        choices=[(role.name, role.value) for role in Status],
    )
    note = TextAreaField("Note")
    assigned_groups = QuerySelectMultipleField(
        "Assigned to Groups",
        query_factory=lambda: Group.query,
        get_label="name"
    )
    assigned_user = QuerySelectField(
        "Assigned to User",
        query_factory=lambda: User.query,
        get_label="username"
    )
    submit = SubmitField("Update")


class CreateTicket(UpdateTicket):
    pass
