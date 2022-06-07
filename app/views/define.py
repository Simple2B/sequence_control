from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.logger import log


define_blueprint = Blueprint("define", __name__)


@define_blueprint.route("/define")
@login_required
def define():
    log(log.INFO, "User [%d] define", current_user.id)

    return render_template("define.html")
