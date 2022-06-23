from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from flask_login import current_user, login_required
from sqlalchemy import desc
from app.controllers import role_required, get_works_for_project
from app.logger import log
from app.models import User, Work, PlanDate, WorkPackage
from app.forms import (
    WorkChangeReasonForm,
    WorkEditDateForm,
    WorkEditNoteForm,
    WorkSelectCompleteForm,
    SearchForm,
    WorkReforecastForm,
)

control_blueprint = Blueprint("control", __name__)


@control_blueprint.route("/control", methods=["GET", "POST"])
@login_required
@role_required(
    roles=[User.Role.project_manager, User.Role.viewer, User.Role.wp_manager]
)
def control():
    user: User = current_user
    log(log.INFO, "[control] User [%d]", current_user.id)
    project_id = session.get("project_id")
    wp_id = session.get("wp_id")
    if user.role in [User.Role.project_manager, User.Role.viewer]:
        if not project_id:
            return redirect(url_for("project.project_choose"))
    if user.role == User.Role.wp_manager:
        if not wp_id:
            return redirect(url_for("work_package.work_package_choose"))
    search_form = SearchForm()
    query = ""
    if search_form.validate_on_submit():
        query = search_form.search_field.data
    page = request.args.get("page", 1, type=int)
    search_result = get_works_for_project().filter_by(is_completed=False)
    if query:
        wp_ids = [
            wp.id
            for wp in WorkPackage.query.filter(WorkPackage.number.ilike(f"%{query}%"))
        ]
        search_result = search_result.filter(Work.wp_id.in_(wp_ids))

    works = search_result.order_by(desc(Work.id)).paginate(page=page, per_page=15)
    return render_template("control.html", works=works, search_form=search_form)


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


@control_blueprint.route("/reforecast/<work_id>", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager, User.Role.wp_manager])
def reforecast(work_id: int):
    log(log.INFO, "User [%d] reforecast", current_user.id)
    user: User = current_user
    work: Work = Work.query.get(work_id)
    if not work:
        log(log.ERROR, "User [%d] can't find work id[%d]", user.id, work_id)
        flash("Can't find PPC", "danger")
        return redirect(url_for("control.control"))
    if (
        user.role == User.Role.project_manager
        and work.work_package.project.manager_id != user.id
    ) or (user.role == User.Role.wp_manager and work.wp_manager_id != user.id):
        log(
            log.WARNING,
            "User [%d] try to change work id[%d] from other project",
            user.id,
            work_id,
        )
        flash("You can't change  PPC from other project", "danger")
        return redirect(url_for("control.control"))

    form = WorkReforecastForm()
    form.deliverable.data = work.deliverable
    form.reference.data = work.reference
    form.old_plan_date.data = work.latest_date
    form.responsible.choices = [
        (wp.contractor_name, wp.contractor_name)
        for wp in WorkPackage.query.filter_by(
            deleted=False, project_id=work.work_package.project_id
        ).all()
    ]
    if form.validate_on_submit():
        PlanDate(
            date=form.new_plan_date.data,
            work_id=work.id,
            version=(work.latest_date_version + 1),
            note=form.note.data,
            responsible=form.responsible.data,
            reason=form.reason.data,
            user_id=user.id,
        ).save()
        log(
            log.INFO,
            "User [%d] edited reforecast for work [%d]",
            current_user.id,
            work.id,
        )
        return redirect(url_for("control.control"))
    elif form.is_submitted():
        log(
            log.WARNING,
            "User [%d] cant reforecast work [%d] , error[%s]",
            current_user.id,
            work.id,
            form.form_errors,
        )
        flash("The given data was invalid.", "danger")
    return render_template("reforecast.html", form=form, work_id=work_id)


@control_blueprint.route("/complete/<work_id>", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def complete(work_id: int):
    log(log.INFO, "User [%d] complete", current_user.id)
    user: User = current_user
    work: Work = Work.query.get(work_id)
    if not work or work.work_package.project.manager_id != user.id:
        log(
            log.WARNING,
            "User [%d] try to change work id[%d] from other project",
            user.id,
            work_id,
        )
        flash("You can't change  PPC from other project", "danger")
        return redirect(url_for("control.control"))
    work.is_completed = True
    work.save()
    return redirect(url_for("control.control"))
