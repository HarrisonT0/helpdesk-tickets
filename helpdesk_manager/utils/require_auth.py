from functools import wraps
from flask import session, redirect, flash


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("You must be logged in to access this page.", "error")
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
