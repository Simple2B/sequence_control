from flask import Blueprint, render_template
from app.logger import log


define_blueprint = Blueprint("define", __name__)


@define_blueprint.route("/define")
def define():
    log(
        log.INFO,
        "User [] define",
    )

    return render_template("define.html")
