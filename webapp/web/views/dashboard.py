from flask import Blueprint, render_template

from webapp.web.utils.acl import roles_required

module = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@roles_required("user", "admin")
@module.route("/")
def index():
    return render_template("/dashboard/index.html")
