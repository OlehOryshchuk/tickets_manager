from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.config import Config
from app import models


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth:login"
csrf_protect = CSRFProtect()


def register_blueprints(app: Flask):
    from app.routes import (
        auth,
        admin,
        group,
        ticket,
        user
    )
    app.register_blueprint(auth.auth_bl)
    app.register_blueprint(admin.admin_bl)
    app.register_blueprint(group.group_bl)
    app.register_blueprint(ticket.ticket_bl)
    app.register_blueprint(user.user_bl)


def configure_db(app: Flask):
    with app.app_context():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def register_extensions(app: Flask):
    login_manager.init_app(app)
    csrf_protect.init_app(app)


def init_app(confi: Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    configure_db(app)

    return app
