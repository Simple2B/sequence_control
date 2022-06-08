from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm
from app.logger import log


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    log(log.INFO, "[login] User [%s] try to login", current_user)
    form = LoginForm(request.form)
    if form.validate_on_submit():
        log(
            log.INFO,
            "[login.validate_on_submit] User [%s] submit form with [%s]",
            current_user,
            form.user_id.data,
        )
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            log(
                log.INFO,
                "[login.validate_on_submit] User [%s] logged in with [%s]",
                current_user,
                form.user_id.data,
            )
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        log(
            log.INFO,
            "[login.validate_on_submit] User [%s] entered wrong credentials with [%s]",
            current_user,
            form.user_id.data,
        )
        flash("Wrong user ID or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "info")
    return redirect(url_for("main.index"))
