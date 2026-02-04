from flask import Blueprint, render_template

module = Blueprint("site", __name__, url_prefix="/")


@module.route("/")
def index():
    return render_template("/site/index.html")

@module.route("/home")
def home():
    return render_template("/site/home.html")