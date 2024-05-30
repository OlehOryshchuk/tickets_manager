from apps.models import User, Roles
from apps.utils import hash_pass
from apps.extensions import db

ADMIN_USERNAME = "Admin1_"
ADMIN_PASSWORD = "afspo982_&(_"


def create_admin(app):
    with app.app_context():

        # check if user admin exist
        user = User.query.filter_by(
            username=ADMIN_USERNAME,
            role=Roles.admin
        ).first()

        if not user:
            admin = User(
                username=ADMIN_USERNAME,
                password=hash_pass(ADMIN_PASSWORD),
                role=Roles.admin
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")

        else:
            print("Admin user already exists.")
