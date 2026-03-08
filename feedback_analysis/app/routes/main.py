"""
app/routes/main.py
Main web page routes
"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Home / dashboard page."""
    return render_template("index.html")


@main_bp.route("/upload")
def upload():
    """Feedback upload page."""
    return render_template("upload.html")


@main_bp.route("/results")
def results():
    """Analysis results page."""
    return render_template("results.html")


@main_bp.route("/about")
def about():
    """About page."""
    return render_template("about.html")
