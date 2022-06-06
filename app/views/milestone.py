from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import MilestoneFrom
from app.logger import log
from app.models import User, ProjectMilestone
from app.controllers import role_required

milestone_blueprint = Blueprint("milestone", __name__)


@milestone_blueprint.route("/milestone_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def milestone_add():
    log(log.INFO, "User [%s] on milestone_add", current_user.id)
    form = MilestoneFrom(request.form)
    if form.validate_on_submit():
        milestones = ProjectMilestone(
            name=form.name.data,
            description=form.description.data,
            baseline_date=form.baseline_date.data,
            project_id=form.project_id.data,
        )
        milestones.save()
        flash("Milestone Registration  is successful.", "success")
        return redirect(url_for("main.define_milestones"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("milestone_add.html", form=form)
