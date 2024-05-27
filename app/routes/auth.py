from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_user, logout_user

from app.models import User
from app.forms import LoginForm, CreateAccountForm
from app import login_manager, db
from app.utils import verify_pass, hash_pass

auth_bl = Blueprint("auth", __name__)


@login_manager.user_loader
def user_loader(user_id: str):
    return User.query.filter_by(id=id).first()


@auth_bl.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for("user:view_me"))

        # Something (user or pass) is not ok
        return render_template('auth/login.html',
                               msg='Wrong user or password',
                               form=login_form)
    return render_template('auth/login.html',
                           form=login_form)


@auth_bl.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if create_account_form.validate_on_submit():

        username = request.form['username']

        # Check username exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('auth/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = User(
            username=username,
            password=hash_pass(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('auth/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    return render_template('auth/register.html', form=create_account_form)


@auth_bl.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth:login'))
