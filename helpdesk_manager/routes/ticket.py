from flask import current_app as app, request, session, render_template, redirect
from helpdesk_manager.models.ticket import Ticket
from ..database import db


@app.route("/ticket/new", methods=["GET", "POST"])
def new_ticket():
    if request.method == "POST":
        # Get form inputs
        title = request.form.get("title")
        content = request.form.get("content")
        user_id = session["user_id"]

        # Create ticket
        ticket = Ticket(title=title, content=content, author_id=user_id)
        db.session.add(ticket)
        db.session.commit()

        return redirect("/")

    return render_template("tickets/new.html")
