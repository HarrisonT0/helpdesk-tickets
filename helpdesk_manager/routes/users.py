from flask import render_template, redirect, flash, g, Blueprint
from helpdesk_manager.models.user import User
from ..database import db
from ..utils.require_auth import require_auth

users_bp = Blueprint("users", __name__, url_prefix="/users")


# List users
@users_bp.route("/")
@require_auth
def list_users():
    if not g.user.admin:
        flash("You do not have permission to view users.", "error")
        return redirect("/")

    users = User.query.with_entities(
        User.id, User.email, User.created_at, User.admin
    ).all()
    return render_template("/users/list.html", users=users)


# Delete user
@users_bp.route("/<user_id>/delete", methods=["POST"])
@require_auth
def delete_user(user_id):
    if not g.user.admin:
        flash("You do not have permission to delete this user.", "error")
        return redirect("/users")

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "success")

    # Force logout if user deleted their own account
    if user == g.user:
        return redirect("/logout")
    return redirect("/users")


# Promote user to admin
@users_bp.route("/<user_id>/promote", methods=["POST"])
@require_auth
def promote_user(user_id):
    if not g.user.admin:
        flash("You do not have permission to promote this user.", "error")
        return redirect("/users")

    user = User.query.get_or_404(user_id)

    user.admin = True
    db.session.commit()
    flash("User promoted.", "success")

    return redirect("/users")


# Demote (admin) user to regular
@users_bp.route("/<user_id>/demote", methods=["POST"])
@require_auth
def demote_user(user_id):
    if not g.user.admin:
        flash("You do not have permission to demote this user.", "error")
        return redirect("/users")

    user = User.query.get_or_404(user_id)

    user.admin = False
    db.session.commit()
    flash("User demoted.", "success")

    return redirect("/users")
