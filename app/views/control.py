from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user, login_required
from app.controllers import role_required, get_works_for_project
from app.logger import log
from app.models import User, Work, PlanDate
from app.forms import (
    WorkChangeReasonForm,
    WorkEditDateForm,
    WorkEditNoteForm,
    WorkSelectCompleteForm,
)

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
            "[work_select_reason] User[%d] changed work [%d] reason ",
            current_user.id,
            work.id,
        )
    return {}


@control_blueprint.route("/edit_work_date/<work_id>", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def edit_work_date(work_id: int):
    log(log.INFO, "User [%d] edit_work_date", current_user.id)
    user: User = current_user
    work: Work = Work.query.get(work_id)
    if not work or work.work_package.project.manager_id != user.id:
        flash("You can't change date for others PPC", "danger")
        return redirect(url_for("control.control"))
    form = WorkEditDateForm()
    form.reference.data = work.reference
    form.old_plan_date.data = work.latest_date
    if form.validate_on_submit():
        PlanDate(
            date=form.new_plan_date.data,
            work_id=work.id,
            version=(work.latest_date_version + 1),
        ).save()
        log(log.INFO, "User [%d] edited date at work [%d]", current_user.id, work.id)
        return redirect(url_for("control.control"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("edit_work_date.html", form=form, work_id=work_id)


@control_blueprint.route("/edit_work_note/<work_id>", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def edit_work_note(work_id: int):
    log(log.INFO, "User [%d] edit_work_note", current_user.id)
    user: User = current_user
    work: Work = Work.query.get(work_id)
    if not work or work.work_package.project.manager_id != user.id:
        flash("You can't change note for others PPC", "danger")
        return redirect(url_for("control.control"))
    form = WorkEditNoteForm()
    form.reference.data = work.reference
    if form.validate_on_submit():
        work.note = form.note.data if form.note.data else "None"
        work.save()
        log(log.INFO, "User [%d] edited note for work [%d]", current_user.id, work.id)
        return redirect(url_for("control.control"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    form.note.data = work.note if work.note != "None" else ""
    return render_template("edit_work_note.html", form=form, work_id=work_id)


@control_blueprint.route("/work_select_complete/", methods=["POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def work_select_complete():
    form = WorkSelectCompleteForm()
    log(log.INFO, "[work_select_complete] User[%d]", current_user.id)

    if form.is_submitted():
        work: Work = Work.query.get(form.work_id.data)
        work.complete = form.complete.data
        work.save()
        log(
            log.INFO,
            "[work_select_complete] User[%d] changed work [%d] completed ",
            current_user.id,
            work.id,
        )
    return {}
