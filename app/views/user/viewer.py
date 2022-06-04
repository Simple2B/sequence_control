from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import WPMRegistrationForm
from app.logger import log
from app.models import User
from app.controllers import role_required


viewer_blueprint = Blueprint("viewer", __name__)


@viewer_blueprint.route("/users")
@login_required
def index():
    log(
        log.INFO,
        "User [] on index page",
    )

    return render_template("users.html")


@viewer_blueprint.route("/viewer_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.admin, User.Role.project_manager])
def viewer_add():
    log(log.INFO, "User [%d] on viewer_add", current_user.id)
    form = WPMRegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            company=form.company_name.data,
            position=form.position.data,
            wp_responsible=form.wp_responsible.data,
            role=User.Role.viewer,
            subordinate_id=current_user.id,
        )
        user.save()
        flash("Registration successful.", "success")
        return redirect(url_for("define.define"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("viewer_add.html", form=form)
