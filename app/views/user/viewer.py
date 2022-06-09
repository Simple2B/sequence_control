from flask import render_template, url_for, redirect, Blueprint, flash, session
from flask_login import current_user, login_required
from app.forms import PmRegistrationForm
from app.logger import log
from app.models import User, ProjectViewer
from app.controllers import role_required

viewer_blueprint = Blueprint("viewer", __name__)


@viewer_blueprint.route("/viewer_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.admin, User.Role.project_manager])
def viewer_add():
    log(log.INFO, "[viewer_add]User [%d] on ", current_user.id)
    form = PmRegistrationForm()
    if form.validate_on_submit():
        project_id = session["project_id"]
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            company=form.company_name.data,
            position=form.position.data,
            role=User.Role.viewer,
            subordinate_id=current_user.id,
        )
        user.save()
        # if project manager creating viewer we can assign him to current project
        if current_user.role == User.Role.project_manager:
            ProjectViewer(project_id=project_id, viewer_id=user.id).save()
            log(
                log.INFO,
                "[viewer_add.validate_on_submit] User [%d] created user [%d] for project[%d]",
                current_user.id,
                user.id,
                project_id,
            )

        flash("Registration successful.", "success")
        return redirect(url_for("define.define"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("viewer_add.html", form=form)
