from flask import current_app as app, render_template
from ..utils.require_auth import require_auth


@app.route("/")
@require_auth
def home():
    return render_template("home.html")
