from flask import request, session, render_template, redirect, flash, g, Blueprint
from helpdesk_manager.models.ticket import Ticket
from helpdesk_manager.models.comment import Comment
from ..database import db
from ..utils.require_auth import require_auth

tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")


# List tickets
@tickets_bp.route("/")
@require_auth
def list_tickets():
    if g.user.admin:
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = (
            Ticket.query.filter_by(author_id=g.user.id)
            .order_by(Ticket.created_at.desc())
            .all()
        )
    return render_template("tickets/list.html", tickets=tickets)


# View individual ticket (by ID)
@tickets_bp.route("/<ticket_id>")
@require_auth
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if (not g.user.admin) and (g.user.id != ticket.author.id):
        flash("You do not have permission to view this ticket.", "error")
        return redirect("/tickets")
    comments = (
        Comment.query.filter_by(ticket_id=ticket_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return render_template("tickets/view.html", ticket=ticket, comments=comments)


# Create new ticket
@tickets_bp.route("/new", methods=["GET", "POST"])
@require_auth
def new_ticket():
    error = None

    if request.method == "POST":
        # Get form inputs
        title = request.form.get("title")
        content = request.form.get("content")
        user_id = session["user_id"]

        # Validation
        if not title:
            error = "Title is required."
        elif not content:
            error = "Content is required."

        # If all checks pass
        else:
            ticket = Ticket(title=title, content=content, author_id=user_id)
            db.session.add(ticket)
            db.session.commit()

            flash(
                "Ticket created - an admin will be in contact via email shortly.",
                "success",
            )
            return redirect("/tickets")

    return render_template("tickets/new.html", error=error)


# Edit ticket
@tickets_bp.route("/<ticket_id>/edit", methods=["GET", "POST"])
@require_auth
def edit_ticket(ticket_id):
    error = None
    ticket = Ticket.query.get_or_404(ticket_id)

    # Check user is author of ticket
    if ticket.author_id != g.user.id:
        flash("You do not have permission to edit this ticket.", "error")
        return redirect("/tickets")

    if request.method == "POST":
        # Get form inputs
        title = request.form.get("title")
        content = request.form.get("content")

        # Validation
        if not title:
            error = "Title is required."
        elif not content:
            error = "Content is required."

        ticket.title = title
        ticket.content = content
        db.session.commit()
        flash("Ticket updated successfully.", "success")
        return redirect(f"/tickets/{ticket.id}")

    return render_template("tickets/edit.html", ticket=ticket, error=error)


# Delete ticket
@tickets_bp.route("/<ticket_id>/delete", methods=["POST"])
@require_auth
def delete_ticket(ticket_id):
    if not g.user.admin:
        flash("You do not have permission to delete this ticket.", "error")
        return redirect("/tickets")

    ticket = Ticket.query.get_or_404(ticket_id)

    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket resolved and deleted.", "success")
    return redirect("/tickets")
