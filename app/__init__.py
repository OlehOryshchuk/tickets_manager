from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.config import Config
from app import models

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth:login"

csrf_protect = CSRFProtect()


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf_protect.init_app(app)

    with app.app_context():
        db.create_all()

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

    return app
