"""Index routes."""

from flask import Blueprint, redirect, render_template, request, session, url_for

bp = Blueprint("index", __name__)


@bp.route("/", methods=["GET"])
def index():
    """Landing page."""
    return render_template("index.html")


@bp.route("/lang/<lang_code>", methods=["GET"])
def set_language(lang_code: str):
    """Set active UI language and redirect back."""
    if lang_code in {"el", "en"}:
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("index.index"))
