from flask import Flask
from .database import db
from .utils.seed_database import seed_database
from dotenv import load_dotenv
import os
import logging


def create_app():
    app = Flask(__name__)

    # Database config
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdesk.db"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret-for-dev-only")
    db.init_app(app)

    # App context
    with app.app_context():
        # Register Database
        db.create_all()
        seed_database()

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        )
        app.logger.setLevel(logging.INFO)

        # Register Blueprints
        from helpdesk_manager.routes.tickets import tickets_bp
        from helpdesk_manager.routes.auth import auth_bp
        from helpdesk_manager.routes.comments import comments_bp
        from helpdesk_manager.routes.users import users_bp
        from helpdesk_manager.routes.home import home_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(tickets_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(comments_bp)

    return app
