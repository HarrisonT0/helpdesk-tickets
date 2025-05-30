from flask import current_app as app


@app.route("/login")
def login():
    return "Login"
