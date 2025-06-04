from flask import request, session, render_template, redirect, flash, g, Blueprint
from helpdesk_manager.models.comment import Comment
from helpdesk_manager.models.ticket import Ticket
from ..database import db
from ..utils.require_auth import require_auth

comments_bp = Blueprint(
    "comments", __name__, url_prefix="/tickets/<ticket_id>/comments"
)


# Create new comment
@comments_bp.route("/new", methods=["GET", "POST"])
@require_auth
def new_comment(ticket_id):
    error = None
    user_id = session["user_id"]

    ticket = Ticket.query.get_or_404(ticket_id)
    if not (g.user.admin or ticket.author_id == user_id):
        flash("You do not have permission to comment on this ticket.", "error")
        return redirect(f"/tickets/{ticket_id}")

    if request.method == "POST":
        # Get form inputs
        content = request.form.get("content")

        # Validation
        if not content:
            error = "Content is required."

        # If all checks pass
        else:
            comment = Comment(content=content, author_id=user_id, ticket_id=ticket_id)
            db.session.add(comment)
            db.session.commit()

            flash(
                "Comment submitted.",
                "success",
            )
            return redirect(f"/tickets/{ticket_id}")

    return render_template("comments/new.html", ticket=ticket, error=error)


# Delete comment
@comments_bp.route("/<comment_id>/delete", methods=["POST"])
@require_auth
def delete_comment(ticket_id, comment_id):
    if not g.user.admin:
        flash("You do not have permission to delete this comment.", "error")
        return redirect(f"/tickets/{ticket_id}")

    comment = Comment.query.get_or_404(comment_id)

    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "success")
    return redirect(f"/tickets/{ticket_id}")
