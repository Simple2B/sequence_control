from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import WPMilestoneFrom
from app.logger import log
from app.models import User, WPMilestone
from app.controllers import role_required

wp_milestone_blueprint = Blueprint("wp_milestone", __name__)


@wp_milestone_blueprint.route("/wp_milestone_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.wp_manager])
def wp_milestone_add():
    log(log.INFO, "User [%s] on wp_milestone_add", current_user.id)
    form = WPMilestoneFrom()
    if form.validate_on_submit():
        wp_milestone = WPMilestone(
            name=form.name.data,
            description=form.description.data,
            baseline_date=form.baseline_date.data,
            wp_manager_id=current_user.id,
            project_milestone_id=form.project_milestone_id.data,
        )
        wp_milestone.save()
        flash("Milestone Registration  is successful.", "success")
        return redirect(url_for("main.define_wp_milestones"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("wp_milestone_add.html", form=form)
