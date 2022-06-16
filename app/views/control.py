from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from app.controllers import role_required, get_works_for_project
from app.logger import log
from app.models import User, Work
from app.forms import WorkChangeReasonForm

control_blueprint = Blueprint("control", __name__)


@control_blueprint.route("/control")
@login_required
@role_required(
    roles=[User.Role.project_manager, User.Role.viewer, User.Role.wp_manager]
)
def control():
    log(log.INFO, "[control] User [%d]", current_user.id)
    type_query = request.args.get("type", "", type=str)
    page = request.args.get("page", 1, type=int)
    type_query = type_query.split("?") if type_query else ["", ""]

    search_result = get_works_for_project()

    works = search_result.paginate(page=page, per_page=15)
    return render_template("control.html", works=works)


@control_blueprint.route("/work_select_reason/", methods=["POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def work_select_reason():
    form = WorkChangeReasonForm()
    log(log.INFO, "[work_select_reason] User[%d]", current_user.id)

    if form.is_submitted():
        work: Work = Work.query.get(form.work_id.data)
        work.reason_id = form.reason_id.data
        work.save()
        log(
            log.INFO,
            "[work_select_reason] User[%d] changed work [%d] milestone ",
            current_user.id,
            work.id,
        )
    return {}
