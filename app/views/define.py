from flask import Blueprint, render_template


define_blueprint = Blueprint("define", __name__)


@define_blueprint.route("/define")
def define():
    return render_template("define.html")
