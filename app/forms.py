from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import (
    QuerySelectMultipleField
)
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectField,
)
from wtforms.validators import (
    Length
)

from app.models import Roles, User, Group


class UpdateUser(FlaskForm):
    username = StringField(
        "Username",
        validators=[Length(max=250)]
    )
    submit = SubmitField("Update")

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop("user_role", None)
        super().__init__(*args, **kwargs)

        # only Admin can update user role
        if user_role == Roles.admin.name:
            self.role = SelectField(
                "Roles",
                choices=[(role.name, role.value) for role in Roles]
            )


class UpdateGroup(FlaskForm):
    name = StringField(
        "Name",
        validators=[Length(max=250)]
    )
    description = TextAreaField("Description")
    users = QuerySelectMultipleField(
        "Users",
        query_factory=lambda: User.query,
        get_label="username"
    )
    submit = SubmitField("Update")


class UpdateTickets(FlaskForm):
    status = SelectField(
        "Status",
        choices=[(role.name, role.value) for role in Roles],
    )
    note = TextAreaField("Note")
    assigned_groups = QuerySelectMultipleField(
        "Assigned Groups",
        query_factory=lambda: Group.query,
        get_label="name"
    )
    assigned_users = QuerySelectMultipleField(
        "Assigned Users",
        query_factory=lambda: User.query,
        get_label="username"
    )
    submit = SubmitField("Update")
