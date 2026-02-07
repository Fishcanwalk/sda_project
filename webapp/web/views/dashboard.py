from flask import Blueprint, render_template

from webapp.web.utils.acl import roles_required

module = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@module.route("/")
@roles_required("user", "admin")
def index():
    return render_template("/dashboard/index.html")
