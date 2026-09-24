from flask import Flask
from config import Config
from app.models.produto import db


def create_app():
    app = Flask(
        __name__,
        template_folder="app/templates",
        static_folder="app/static"
    )

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)