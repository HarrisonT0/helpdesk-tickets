from flask import (
    current_app as app,
    request,
    session,
    render_template,
    redirect,
    flash,
    g,
)
from helpdesk_manager.models.comment import Comment
from helpdesk_manager.models.ticket import Ticket
from ..database import db
from ..utils.require_auth import require_auth


# Create new comment
@app.route("/tickets/<ticket_id>/comment", methods=["GET", "POST"])
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
