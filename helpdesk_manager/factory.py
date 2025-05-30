from flask import Flask
from .database import db
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

        # Create (upsert) admin account
        if not User.query.filter_by(email="admin@company.com").first():
            admin = User(
                email="admin@company.com",
                password_hash=generate_password_hash("password"),
                admin=True,
            )
            db.session.add(admin)
            db.session.commit()

        # Register routes
        import helpdesk_manager.routes.home
        import helpdesk_manager.routes.auth
        import helpdesk_manager.routes.tickets

    return app
