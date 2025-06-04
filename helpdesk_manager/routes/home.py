from flask import render_template, Blueprint
from ..utils.require_auth import require_auth

home_bp = Blueprint("home", __name__, url_prefix="/")


@home_bp.route("/")
@require_auth
def home():
    return render_template("home.html")
