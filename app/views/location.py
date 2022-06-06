from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import BuildingForm, LevelForm, LocationForm
from app.logger import log
from app.models import User, Building, Level, Location
from app.controllers import role_required

location_blueprint = Blueprint("location", __name__)


@location_blueprint.route("/building_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def building_add():
    log(log.INFO, "User [%s] on building_add", current_user.id)
    form = BuildingForm(request.form)
    if form.validate_on_submit():
        building = Building(
            name=form.name.data,
            project_id=form.project_id.data,
        )
        building.save()
        flash("Building Registration  is successful.", "success")
        return redirect(url_for("main.define_locations"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("building_add.html", form=form)


@location_blueprint.route("/level_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def level_add():
    log(log.INFO, "User [%s] on level_add", current_user.id)
    form = LevelForm(request.form)
    if form.validate_on_submit():
        level = Level(
            name=form.name.data,
            building_id=form.building_id.data,
        )
        level.save()
        flash("Level Registration  is successful.", "success")
        return redirect(url_for("main.define_locations"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("level_add.html", form=form)


@location_blueprint.route("/location_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def location_add():
    log(log.INFO, "User [%s] on location_add", current_user.id)
    form = LocationForm(request.form)
    if form.validate_on_submit():
        location = Location(
            name=form.name.data,
            description=form.description.data,
            level_id=form.level_id.data,
        )
        location.save()
        flash("Location Registration  is successful.", "success")
        return redirect(url_for("main.define_locations"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("location_add.html", form=form)
