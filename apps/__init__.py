from flask import Flask
from flask_migrate import Migrate

from apps.extensions import db, login_manager, csrf_protect, bcrypt
from apps.models import User


def register_blueprints(app: Flask):
    from apps.routes import group, ticket, user
    from apps.auth.route import auth_bl

    app.register_blueprint(auth_bl)
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
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)
    csrf_protect.init_app(app)
    bcrypt.init_app(app)

    @login_manager.user_loader
    def user_loader(user_id: str):
        return User.query.filter_by(id=int(user_id)).first()


def init_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    configure_db(app)

    return app
