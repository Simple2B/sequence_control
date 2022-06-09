from flask import render_template, url_for, redirect, Blueprint, request, flash, session
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
    log(log.INFO, "[building_add] User [%s] ", current_user.id)
    form = BuildingForm(request.form)
    if form.validate_on_submit():
        log(
            log.INFO,
            "[building_add.validate_on_submit] User [%s] name [%s], project[%s]",
            current_user.id,
            form.name.data,
            session["project_id"],
        )

        building = Building(
            name=form.name.data,
            project_id=session["project_id"],
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
    log(log.INFO, "[level_add] User [%s]", current_user.id)
    form = LevelForm(request.form)
    form.building_id.choices = [
        (building.id, building.name)
        for building in Building.query.filter_by(
            deleted=False, project_id=session["project_id"]
        ).all()
    ]
    if form.validate_on_submit():
        log(
            log.INFO,
            "[level_add.validate_on_submit] User [%s] submitted name[%s] building[%s]",
            current_user.id,
            form.name.data,
            form.building_id.data,
        )

        level = Level(
            name=form.name.data,
            building_id=form.building_id.data,
        )
        level.save()
        flash("Level Registration  is successful.", "success")
        return redirect(url_for("main.define_locations"))
    elif form.is_submitted():
        log(
            log.INFO,
            "[level_add.is_submitted] User [%s] submitted failed with name[%s] building[%s]",
            current_user.id,
            form.name.data,
            form.building_id.data,
        )

        flash("The given data was invalid.", "danger")
    return render_template("level_add.html", form=form)


@location_blueprint.route("/location_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def location_add():
    log(log.INFO, "[location_add] User [%s]", current_user.id)
    form = LocationForm(request.form)
    form.level_id.choices = [
        (level.id, level.name + " - " + level.building.name)
        for level in Level.query.filter_by(
            deleted=False,
        ).all()
        if level.building.project_id == session["project_id"]
    ]
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
