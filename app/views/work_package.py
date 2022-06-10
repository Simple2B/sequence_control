from flask import render_template, url_for, redirect, Blueprint, flash, session
from flask_login import current_user, login_required
from app.forms import WorkPackageForm, ProjectChooseForm
from app.logger import log
from app.models import User, WorkPackage
from app.controllers import role_required

work_package_blueprint = Blueprint("work_package", __name__)


@work_package_blueprint.route("/work_package_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def work_package_add():
    form = WorkPackageForm()
    if form.validate_on_submit():
        log(
            log.INFO,
            "[work_package_add.validate_on_submit] User [%s] submit wp # [%s] for project [%s]",
            current_user.id,
            form.number.data,
            session["project_id"],
        )
        work_package = WorkPackage(
            name=form.name.data,
            number=form.number.data,
            contractor_name=form.contractor_name.data,
            project_id=session["project_id"],
            manager_id=form.wp_manager.data,
        )
        work_package.save()
        flash("Work Package Registration  is successful.", "success")
        return redirect(url_for("main.define_work_packages"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("work_package_add.html", form=form)


@work_package_blueprint.route("/work_package_choose", methods=["GET", "POST"])
@login_required
@role_required(
    roles=[
        User.Role.wp_manager,
        User.Role.viewer,
    ]
)
def work_package_choose():
    log(log.INFO, "[work_package_choose] User [%s] in", current_user)
    form = ProjectChooseForm()
    user: User = User.query.filter_by(id=current_user.id).first()
    form.number.choices = [
        (wp.id, wp.number)
        for wp in WorkPackage.query.filter_by(deleted=False, manager_id=user.id).all()
    ]
    if form.validate_on_submit():
        log(
            log.INFO,
            "[work_package_choose.validate_on_submit] User [%s] choose work package [%s]",
            user.id,
            form.number.data,
        )
        session["wp_id"] = form.number.data
        wp: WorkPackage = WorkPackage.query.get(form.number.data)
        session["project_name"] = wp.name
        log(
            log.INFO,
            "[work_package_choose.validate_on_submit] User [%s]  work package [%s]",
            current_user,
            session["wp_id"],
        )
        if user.role == User.Role.wp_manager:
            return redirect(url_for("main.define_wp_milestones"))
        if user.role == User.Role.viewer:
            return redirect(url_for("main.define_for_viewer"))
    return render_template("work_package_choose.html", form=form)
