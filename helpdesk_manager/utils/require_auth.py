from functools import wraps
from flask import session, redirect, flash

from helpdesk_manager.models.user import User


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")

        # No credentials presented
        if not user_id:
            flash("You must be logged in to access this page.", "error")
            return redirect("/login")

        # Credentials invalid/expired
        user = User.query.get(user_id)
        if not user:
            session.clear()
            flash("Your session expired. Please log in again.", "error")
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function
