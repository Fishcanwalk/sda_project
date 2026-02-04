from flask import Blueprint, render_template

module = Blueprint("dashboard", __name__)


@module.route("/")
def index():
    return render_template("/dashboard/index.html")
