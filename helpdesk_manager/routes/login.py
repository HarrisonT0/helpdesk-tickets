from flask import current_app as app, request, session, render_template, redirect
from werkzeug.security import check_password_hash
from ..models.user import User


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None:
            error = "Invalid email."
        elif not check_password_hash(user.password_hash, password):
            error = "Invalid password."
        else:
            session["user_id"] = user.id
            return redirect("/")

    return render_template("login.html", error=error)
