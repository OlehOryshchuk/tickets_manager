from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class CreateAccountForm(FlaskForm):
    username = StringField(
        "Username", id="username_create", validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        id="pwd_create",
        validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        id="username_login",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        id="pwd_login",
        validators=[DataRequired()]
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")
