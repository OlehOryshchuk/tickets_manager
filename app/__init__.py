from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.config import Config

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

    from app.auth import auth
    app.register_blueprint(auth)

    from app.route import main
    app.register_blueprint(main)

    return app


from app import models
