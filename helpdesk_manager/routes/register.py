from flask import current_app as app, request, session, render_template, redirect
from ..models.user import User
from werkzeug.security import generate_password_hash
from ..database import db


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        # Get form inputs
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if password != confirm_password:
            error = "Passwords do not match."
        elif User.query.filter_by(email=email).first():
            error = "User with this email already exists. Please Log in."

        # If all checks pass
        else:
            hashed_password = generate_password_hash(password)
            user = User(email=email, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id
            redirect("/")

    return render_template("register.html", error=error)
