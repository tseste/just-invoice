"""Search routes."""

from flask import Blueprint, render_template

bp = Blueprint("search", __name__)


@bp.route("/search", methods=["GET"])
def search():
    """Search page."""
    return render_template("search.html")
