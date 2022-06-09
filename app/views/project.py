from flask import render_template, url_for, redirect, Blueprint, request, flash, session
from flask_login import current_user, login_required
from app.forms import ProjectForm, ProjectChooseForm
from app.logger import log
from app.models import User, Project
from app.controllers import role_required

project_blueprint = Blueprint("project", __name__)


@project_blueprint.route("/project_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.admin])
def project_add():
    log(log.INFO, "User [%s] on project_add", current_user)
    form = ProjectForm(request.form)
    form.manager_id.choices = [
        (user.id, user.username)
        for user in User.query.filter_by(
            deleted=False, role=User.Role.project_manager
        ).all()
    ]
    if form.validate_on_submit():
        log(
            log.INFO,
            "[project_add.validate_on_submit] User [%s] submit form",
            current_user,
        )

        project = Project(
            name=form.name.data,
            number=form.number.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            manager_id=form.manager_id.data,
        )
        project.save()
        log(
            log.INFO,
            "[project_add.validate_on_submit] Project saved with id [%d], manager_id [%d] by user [%s]",
            project.id,
            project.manager_id,
            current_user,
        )
        flash("Project Registration  is successful.", "success")
        return redirect(url_for("main.define_projects"))
    elif form.is_submitted():
        log(
            log.INFO,
            "[project_add.is_submitted] User [%s] submit form failed",
            current_user,
        )
        flash("The given data was invalid.", "danger")
    return render_template("project_add.html", form=form)


@project_blueprint.route("/project_choose", methods=["GET", "POST"])
@login_required
@role_required(
    roles=[
        User.Role.wp_manager,
        User.Role.project_manager,
        User.Role.viewer,
    ]
)
def project_choose():
    log(log.INFO, "[project_choose] User [%s] in", current_user)
    form = ProjectChooseForm(request.form)
    user: User = User.query.filter_by(id=current_user.id).first()
    if user.role == User.Role.project_manager:
        form.number.choices = [
            (project.id, project.number)
            for project in Project.query.filter_by(
                deleted=False, manager_id=user.id
            ).all()
        ]
    else:
        form.number.choices = []
    if form.validate_on_submit():
        log(
            log.INFO,
            "[project_choose.validate_on_submit] User [%s] choose project [%s]",
            user.id,
            form.number.data,
        )
        session["project_id"] = form.number.data
        project: Project = Project.query.get(form.number.data)
        session["project_name"] = project.name
        log(
            log.INFO,
            "[project_choose.validate_on_submit] User [%s] choose project [%s]",
            current_user,
            session["project_id"],
        )
        return redirect(url_for("main.define_milestones"))
    return render_template("project_choose.html", form=form)
