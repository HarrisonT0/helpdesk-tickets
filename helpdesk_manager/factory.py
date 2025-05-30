from flask import Flask
from .database import db
from .utils.seed_database import seed_database
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__)

    # Database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdesk.db"
    app.config["SECRET_KEY"] = "SECRET_CHANGE_ME"
    db.init_app(app)

    # App context
    with app.app_context():
        # Register table models
        from helpdesk_manager.models.user import User
        from helpdesk_manager.models.ticket import Ticket

        db.create_all()
        seed_database()

        # Register routes
        import helpdesk_manager.routes.home
        import helpdesk_manager.routes.auth
        import helpdesk_manager.routes.tickets

    return app
