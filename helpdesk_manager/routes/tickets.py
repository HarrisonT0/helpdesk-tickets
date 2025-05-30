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
from helpdesk_manager.models.ticket import Ticket
from ..database import db
from ..utils.require_auth import require_auth


@app.route("/tickets")
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


@app.route("/tickets/<ticket_id>")
@require_auth
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("tickets/view.html", ticket=ticket)


@app.route("/tickets/new", methods=["GET", "POST"])
@require_auth
def new_ticket():
    if "user_id" not in session:
        return redirect(url_for("login"))

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
            return redirect(url_for("list_tickets"))

    return render_template("tickets/new.html", error=error)
