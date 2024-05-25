import dotenv

from app import init_app

dotenv.load_dotenv()

# create app and all of it dependencies
app = init_app()


if __name__ == "__main__":
    app.run(debug=True)
