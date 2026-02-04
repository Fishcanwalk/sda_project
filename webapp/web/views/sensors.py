from flask import Blueprint, render_template

module = Blueprint("sensors", __name__, url_prefix="/sensors")


@module.route("/")
def index():
    return render_template("/sensors/index.html")

@module.route("/view")
def view():
    return render_template("/sensors/view.html")