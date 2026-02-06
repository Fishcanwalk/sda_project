from flask import Blueprint, render_template

from webapp.web.utils.acl import roles_required

module = Blueprint("site", __name__, url_prefix="/")


@module.route("/")
def index():
    return render_template("/site/index.html")


@roles_required("user", "admin")
@module.route("/home")
def home():
    return render_template("/site/home.html")
