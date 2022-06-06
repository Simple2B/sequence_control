from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import WorkPackageForm
from app.logger import log
from app.models import User, WorkPackage
from app.controllers import role_required

work_package_blueprint = Blueprint("work_package", __name__)


@work_package_blueprint.route("/work_package_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def work_package_add():
    log(log.INFO, "User [%s] on work_package_add", current_user.id)
    form = WorkPackageForm(request.form)
    if form.validate_on_submit():
        work_package = WorkPackage(
            name=form.name.data,
            number=form.number.data,
            contractor_name=form.contractor_name.data,
            project_id=form.project_id.data,
            manager_id=current_user.id,
        )
        work_package.save()
        flash("Work Package Registration  is successful.", "success")
        return redirect(url_for("main.define_work_packages"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("work_package_add.html", form=form)
