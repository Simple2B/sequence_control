from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms.auth import RegistrationForm
from app.logger import log
from app.models import User

admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/admin_add", methods=["GET", "POST"])
@login_required
# @role_required(roles=[User.Role.admin])
def admin_add():
    log(log.INFO, "User [%s] on admin_blueprint", current_user.id)
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            company=form.company_name.data,
            role=User.Role.admin,
        )
        user.save()
        flash("Registration successful.", "success")
        return redirect(url_for("define.define"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("admin_add.html", form=form)
