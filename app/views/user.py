from flask import render_template, Blueprint
from flask_login import login_required
from app.logger import log

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users")
@login_required
# @role_required(roles=[User.Role.admin])
def index():
    log(
        log.INFO,
        "User [] on index page",
    )

    return render_template("users.html")


# @user_blueprint.route("/project_manager_add", methods=["GET", "POST"])
# @login_required
# # @role_required(roles=[User.Role.admin])
# def project_manager_add():
#     log(
#         log.INFO,
#         "User [] on project_manager_add",
#     )
#     form = PmRegistrationForm(request.form)
#     if form.validate_on_submit():
#         user = User(
#             username=form.username.data,
#             email=form.email.data,
#             password=form.password.data,
#             company=form.company_name.data,
#             position=form.position.data,
#             role=User.Role.project_manager,
#         )
#         user.save()
#         flash("Registration successful.", "success")
#         return redirect(url_for("define.define"))
#     elif form.is_submitted():
#         flash("The given data was invalid.", "danger")
#     return render_template("project_manager_add.html", form=form)
