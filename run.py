import dotenv
import os

from apps import init_app
from apps.config import config_dict
from create_admin_user import create_admin

dotenv.load_dotenv()

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv("DEBUG", "False") == "True")

# The configuration
config_mode = "debug" if DEBUG else "production"

# create apps and all of it dependencies
app = init_app(config_dict[config_mode])

# create default admin user
create_admin(app)

if __name__ == "__main__":
    app.run()
