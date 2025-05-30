from flask import current_app as app, request, session, render_template, redirect, g
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User
from ..database import db
import re


# RegEx pattern matching strings of at least 6 characters with at least 1 number and 1 special character
PASSWORD_REGEX = re.compile(r"^(?=.*[0-9])(?=.*[\W_]).{6,}$")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        # Get form inputs
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if not email or not password or not confirm_password:
            error = "All fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif not PASSWORD_REGEX.match(password):
            error = "Stronger password required. Must be at least 6 characters, contain at least one number, and contain at least one special character."
        elif User.query.filter_by(email=email).first():
            error = "User with this email already exists. Please Log in."

        # If all checks pass
        else:
            hashed_password = generate_password_hash(password)
            user = User(email=email, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id
            return redirect("/")

    return render_template("auth/register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        # Get form inputs
        email = request.form.get("email")
        password = request.form.get("password")

        # Find user with existing username
        user = User.query.filter_by(email=email).first()

        # Validation
        if user is None:
            error = "Invalid email."
        elif not check_password_hash(user.password_hash, password):
            error = "Invalid password."

        # If all checks pass
        else:
            session["user_id"] = user.id
            return redirect("/")

    return render_template("auth/login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Inject user object into template for fine-grain ACG handling
@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = None
    if user_id is not None:
        g.user = User.query.get(user_id)


@app.context_processor
def inject_user():
    return dict(user=g.get("user", None))
