from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import ProjectForm
from app.logger import log
from app.models import User, Project
from app.controllers import role_required

project_blueprint = Blueprint("project", __name__)


@project_blueprint.route("/project_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.admin])
def project_add():
    log(log.INFO, "User [%s] on project_add", current_user.id)
    form = ProjectForm(request.form)
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            number=form.number.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
        )
        project.save()
        flash("Project Registration  is successful.", "success")
        return redirect(url_for("main.define_projects"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("project_add.html", form=form)
