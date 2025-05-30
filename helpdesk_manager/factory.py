from flask import Flask
from .database import db


def create_app():
    app = Flask(__name__)

    # Database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdesk.db"
    db.init_app(app)

    # App context
    with app.app_context():
        db.create_all()

        # Routes
        import helpdesk_manager.routes.login

    return app
