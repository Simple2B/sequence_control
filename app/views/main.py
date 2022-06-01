from flask import Blueprint, redirect, render_template
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
    # TODO: if current role admin render user to create else render main page
    return redirect(url_for("main.main_page"))
    # return redirect(url_for("main.main_page"))


@main_blueprint.route("/main_page", methods=["GET", "POST"])
def main_page():
    return render_template("main_page.html")
