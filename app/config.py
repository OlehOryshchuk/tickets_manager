import os
import dotenv

dotenv.load_dotenv()


class Config:
    ASSETS_ROOT = "app/static"

    # database configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
