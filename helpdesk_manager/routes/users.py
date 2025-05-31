from flask import (
    current_app as app,
    request,
    session,
    render_template,
    redirect,
    url_for,
    flash,
    g,
)
from helpdesk_manager.models.user import User
from ..database import db
from ..utils.require_auth import require_auth


# List users
@app.route("/users")
@require_auth
def list_users():
    if not g.user.admin:
        flash("You do not have permission to view users.", "error")
        return redirect("/")

    users = User.query.with_entities(User.id, User.email, User.created_at).all()
    return render_template("/users/list.html", users=users)
