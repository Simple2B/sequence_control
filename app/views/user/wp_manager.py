from flask import render_template, session, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import WPMRegistrationForm
from app.logger import log
from app.models import User, WorkPackage
from app.controllers import role_required

wp_manager_blueprint = Blueprint("wp_manager", __name__)


@wp_manager_blueprint.route("/wp_manager_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager, User.Role.admin])
def wp_manager_add():
    log(log.INFO, "User [%d] on wp_manager_add", current_user.id)
    form = WPMRegistrationForm(request.form)
    if current_user.role == User.Role.admin:
        form.wp_responsible.choices = [
            (wp.id, wp.number)
            for wp in WorkPackage.query.filter_by(deleted=False).all()
        ]
    else:
        form.wp_responsible.choices = [
            (wp.id, wp.number)
            for wp in WorkPackage.query.filter_by(
                deleted=False,
                manager_id=current_user.id,
                project_id=session["project_id"],
            ).all()
        ]
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            company=form.company_name.data,
            position=form.position.data,
            wp_responsible=form.wp_responsible.data,
            role=User.Role.wp_manager,
            subordinate_id=current_user.id,
        )
        user.save()
        flash("Registration successful.", "success")
        return redirect(url_for("define.define"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("wp_manager_add.html", form=form)
