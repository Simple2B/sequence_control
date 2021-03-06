from flask import render_template, url_for, redirect, Blueprint, flash
from flask_login import current_user, login_required
from app.forms import PmRegistrationForm
from app.logger import log
from app.models import User
from app.controllers import role_required

project_manager_blueprint = Blueprint("project_manager", __name__)


@project_manager_blueprint.route("/project_manager_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.admin])
def project_manager_add():
    log(log.INFO, "User [%d] on project_manager_add", current_user.id)
    form = PmRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            company=form.company_name.data,
            position=form.position.data,
            role=User.Role.project_manager,
            subordinate_id=current_user.id,
        )
        user.save()
        log(log.INFO, "User [%d] added project manager [%d]", current_user.id, user.id)
        flash("Registration successful.", "success")
        return redirect(url_for("define.define"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("project_manager_add.html", form=form)
