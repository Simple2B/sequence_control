from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import current_user, login_required
from app.forms import ReasonForm
from app.logger import log
from app.models import User, Reason
from app.controllers import role_required

reason_blueprint = Blueprint("reason", __name__)


@reason_blueprint.route("/reason_add", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.admin])
def reason_add():
    log(log.INFO, "User [%s] on reason_add", current_user.id)
    form = ReasonForm(request.form)
    if form.validate_on_submit():
        reason = Reason(
            name=form.name.data,
        )
        reason.save()
        flash("Reason Registration  is successful.", "success")
        return redirect(url_for("main.define_reasons"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("reason_add.html", form=form)
