import dotenv
import os
from flask_migrate import Migrate

from app import init_app, db
from app.config import config_dict

dotenv.load_dotenv()

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv("DEBUG", "False") == "True")

# The configuration
config_mode = "debug" if DEBUG else "production"

# create app and all of it dependencies
app = init_app(config_dict[config_mode])
Migrate(app, db)

if __name__ == "__main__":
    app.run()
