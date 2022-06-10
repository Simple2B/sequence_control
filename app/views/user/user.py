from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required
from app.logger import log
from app.forms import EditUserForm
from app.models import User

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/user_edit", methods=["GET", "POST"])
@login_required
def user_edit():
    log(log.INFO, "User [%d] user_edit", current_user.id)
    user: User = current_user
    form = EditUserForm()
    form.user_name.data = user.username
    if form.validate_on_submit():
        user.password = form.password.data
        user.save()
        log(log.INFO, "User [%d] edited password", current_user.id)
        flash("Password changed.", "success")
        return redirect(url_for("define.define"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("user_edit.html", form=form)
