import os
import dotenv

dotenv.load_dotenv()


class Config:
    ASSETS_ROOT = "app/static"
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # database configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
