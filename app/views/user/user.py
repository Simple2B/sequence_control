from flask import render_template, Blueprint
from flask_login import login_required
from app.logger import log

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users")
@login_required
def index():
    log(
        log.INFO,
        "User [] on index page",
    )

    return render_template("users.html")
