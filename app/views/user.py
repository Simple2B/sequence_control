from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import login_required
from app.forms.auth import PmRegistrationForm, WPMRegistrationForm
from app.logger import log
from app.models import User

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users")
@login_required
# @role_required(roles=[User.RoleType.admin])
def index():
    log(
        log.INFO,
        "User [] on index page",
    )

    return render_template("users.html")


@user_blueprint.route("/project_manager_add", methods=["GET", "POST"])
@login_required
# @role_required(roles=[User.RoleType.admin])
def project_manager_add():
    log(
        log.INFO,
        "User [] on project_manager_add",
    )
    form = PmRegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            company=form.company_name.data,
            position=form.position.data,
            sc_role=User.RoleType.project_manager,
        )
        user.save()
        flash("Registration successful.", "success")
        return redirect(url_for("define.define"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("project_manager_add.html", form=form)
