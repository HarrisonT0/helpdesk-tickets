from functools import wraps
from flask import session, redirect, flash, current_app as app, request

from helpdesk_manager.models.user import User


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")

        # No credentials presented
        if not user_id:
            app.logger.warning(
                "Unauthenticated access attempt path=%s ip=%s",
                request.path,
                request.remote_addr,
            )
            flash("You must be logged in to access this page.", "error")
            return redirect("/login")

        # Credentials invalid/expired
        user = User.query.get(user_id)
        if not user:
            session.clear()
            app.logger.warning(
                "Invalid or expired credentials provided path=%s ip=%s user_id=%s",
                request.path,
                request.remote_addr,
                user_id,
            )
            flash("Your session expired. Please log in again.", "error")
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function
