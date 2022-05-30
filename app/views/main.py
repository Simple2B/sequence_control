from flask import Blueprint, redirect
from flask.helpers import url_for
from app.logger import log
from flask_login import current_user
from app.models.user import AnonymousUser


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():

    log(
        log.INFO,
        "User [] on index page",
    )

    # return redirect(url_for("auth.login"))
    if isinstance(current_user, AnonymousUser):
        return redirect(url_for("auth.login"))

    return redirect(url_for("user.index"))
