import tempfile
from flask import Blueprint, render_template, request, session, redirect, flash
from flask.helpers import url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from app.controllers import role_required, import_data_file, get_works_for_project
from app.logger import log
from app.models import User, Work, PlanDate
from app.forms import (
    ImportFileForm,
    WorkEditForm,
    WorkAddForm,
    WorkDeleteForm,
    WorkChangeMilestoneForm,
    WorkChangeLocationForm,
)

plan_blueprint = Blueprint("plan", __name__)


@plan_blueprint.route("/plan")
@login_required
@role_required(
    roles=[User.Role.wp_manager, User.Role.project_manager, User.Role.viewer]
)
def plan():
    user: User = current_user
    log(log.INFO, "User [%d] plan", user.id)
    project_id = session.get("project_id")
    wp_id = session.get("wp_id")
    if user.role in [User.Role.project_manager, User.Role.viewer]:
        if not project_id:
            return redirect(url_for("project.project_choose"))
    if user.role == User.Role.wp_manager:
        if not wp_id:
            return redirect(url_for("work_package.work_package_choose"))
    return render_template("plan.html")


@plan_blueprint.route("/import_file", methods=["GET", "POST"])
@login_required
@role_required(
    roles=[
        User.Role.wp_manager,
    ]
)
def import_file():
    wp_id = session.get("wp_id")
    if not wp_id:
        log(log.ERROR, "No WP_ID!")
        return redirect(url_for("work_package.work_package_choose"))
    wp_id = int(wp_id)
    form = ImportFileForm()
    if form.validate_on_submit():
        # save data to DB
        in_file = form.file.data
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            # fp.close()
            file_path: str = fp.name
            with open(file_path, "wb") as wf:
                wf.write(in_file.read())
            import_data_file(file_path, wp_id)
        return redirect(url_for("plan.plan"))
    elif form.is_submitted():
        log(log.ERROR, "form submit errors: [%s]", form.errors)
        # flash("The given data was invalid.", "danger")

    return render_template("import_file.html", form=form)


@plan_blueprint.route("/info/<ppc_type>")
@login_required
@role_required(
    roles=[User.Role.wp_manager, User.Role.project_manager, User.Role.viewer]
)
def info(ppc_type):
    ppc_type: Work.PpcType = Work.PpcType[ppc_type]
    type_query = request.args.get("type", "", type=str)
    page = request.args.get("page", 1, type=int)
    type_query = type_query.split("?") if type_query else ["", ""]
    # query = request.args.get("query", "", type=str)
    type = type_query[0]
    query = type_query[1] if len(type_query) == 2 else ""
    links, color = {
        Work.PpcType.info: (
            ["DWG", "TS", "SCH", "MDL", "CPD", "EDA", "TDRG", "TENQ", "CFO", "DSC"],
            "yellow",
        ),
        Work.PpcType.docs: (["PSD", "RAMS", "TWS", "CMS"], "blue"),
        Work.PpcType.quality: (
            ["QS_QBM_P_MU", "Fab_QSO", "Ins_QSO", "QHP"],
            "green",
        ),
        Work.PpcType.atp: (
            ["ATP1", "ATP2", "ATP3"],
            "red",
        ),
        Work.PpcType.hod: (
            ["HOD"],
            "brown",
        ),
    }[ppc_type]

    search_result = get_works_for_project(ppc_type, type)

    query = query.strip()
    if query:
        search_result = search_result.filter(Work.reference.like(f"%{query}%"))

    works = search_result.paginate(page=page, per_page=15)
    return render_template(
        "plan.html",
        context="info",
        works=works,
        links=links,
        color=color,
        ppc_type=ppc_type.name,
    )


@plan_blueprint.route("/edit_work/<work_id>", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.wp_manager, User.Role.project_manager])
def edit_work(work_id: int):
    log(log.INFO, "User [%d] edit_work", current_user.id)
    user: User = current_user
    work: Work = Work.query.get(work_id)
    if not work:
        flash("You can't change date for others PPC", "danger")
        return redirect(url_for("plan.plan"))
    if user.role == User.Role.wp_manager:
        if work.work_package.manager_id != user.id:
            log(
                log.WARNING,
                "[edit_work] User [%d] try to edit work [%d]",
                current_user.id,
                work.id,
            )
            flash("You can't edit PPC from other Work Package", "danger")
            return redirect(url_for("plan.info", ppc_type=work.ppc_type.name))
        form = WorkEditForm()
    else:
        project_id = session.get("project_id")
        if not project_id or work.work_package.project_id != project_id:
            log(
                log.WARNING,
                "[edit_work] User [%d] try to edit work [%d]",
                current_user.id,
                work.id,
            )
            flash("You can't delete PPC from other Project", "danger")
            return redirect(url_for("plan.info", ppc_type=work.ppc_type.name))
        form = WorkDeleteForm()
    if form.validate_on_submit():
        work_type: Work.Type = Work.Type[form.type.data.upper()]
        work.deliverable = form.deliverable.data
        work.ppc_type = Work.ppc_type_by_type(work_type)
        work.type = work_type
        work.save()
        if not work.latest_date or form.new_plan_date.data != work.latest_date.date():
            PlanDate(
                date=form.new_plan_date.data,
                work_id=work.id,
                version=(work.latest_date_version + 1)
                if work.latest_date_version
                else 1,
            ).save()
        log(log.INFO, "User [%d] edited work [%d]", current_user.id, work.id)
        return redirect(url_for("plan.info", ppc_type=work.ppc_type.name))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    form.reference.data = work.reference
    form.deliverable.data = work.deliverable
    form.plan_date.data = work.latest_date
    form.ppc_type.data = work.ppc_type.name
    form.type.data = work.type.name
    if user.role == User.Role.wp_manager:
        form.new_plan_date.data = work.latest_date
    return render_template("edit_work.html", form=form, work_id=work_id)


@plan_blueprint.route("/work_add/<ppc_type>", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.wp_manager])
def work_add(ppc_type: str):
    log(log.INFO, "User [%d] work_add", current_user.id)
    user: User = current_user
    wp_id = session.get("wp_id")
    if not wp_id:
        log(log.ERROR, "[work_add] No WP_ID for user [%d]", user.id)
        return redirect(url_for("work_package.work_package_choose"))
    wp_id = int(wp_id)

    ppc_type = ppc_type
    type_query = request.args.get("type", "", type=str)
    type_query = type_query.split("?") if type_query else ["", ""]
    type = type_query[0]

    form = WorkAddForm()

    form.ppc_type.data = form.ppc_type.data.lower() if form.ppc_type.data else ppc_type
    form.type.data = form.type.data.upper() if form.type.data else type
    if form.validate_on_submit():
        try:
            work_type: Work.Type = Work.Type[form.type.data]
        except KeyError:
            flash("The given data was invalid.", "danger")
            return render_template("work_add.html", form=form, ppc_type=ppc_type)
        work = Work(
            wp_id=wp_id,
            type=work_type,
            ppc_type=Work.ppc_type_by_type(work_type),
            deliverable=form.deliverable.data,
            reference=form.reference.data,
        ).save()
        PlanDate(
            date=form.plan_date.data,
            work_id=work.id,
        ).save()

        log(log.INFO, "User [%d] added work [%d]", user.id, work.id)
        # flash("Date changed.", "success")
        return redirect(url_for("plan.info", form=form, ppc_type=ppc_type))

    elif form.is_submitted():
        log(log.INFO, "User [%d] cannot add work ", user.id)

    return render_template("work_add.html", form=form, ppc_type=ppc_type)


@plan_blueprint.route("/delete_work/<work_id>", methods=["GET", "POST"])
@login_required
@role_required(roles=[User.Role.project_manager])
def delete_work(work_id: int):
    log(log.INFO, "User [%d] delete_work", current_user.id)
    project_id = session.get("project_id")
    if not project_id:
        return redirect(url_for("project.project_choose"))
    project_id = int(project_id)
    work: Work = Work.query.get(work_id)

    if not work or work.work_package.project_id != project_id:
        flash("You can't delete PPC of other Project", "danger")
        return redirect(url_for("plan.plan"))
    work.deleted = True
    work.save()
    log(log.INFO, "[delete_work] User [%d] deleted work [%d]", current_user.id, work.id)

    return redirect(url_for("plan.info", ppc_type=work.ppc_type.name))


@plan_blueprint.route("/work_version/<work_id>")
@login_required
@role_required(
    roles=[User.Role.wp_manager, User.Role.project_manager, User.Role.viewer]
)
def work_version(work_id: int):
    log(log.INFO, "User [%d] work_version", current_user.id)
    work: Work = Work.query.get(work_id)
    page = request.args.get("page", 1, type=int)
    plan_dates = (
        PlanDate.query.filter(PlanDate.work_id == work_id)
        .order_by(desc(PlanDate.version))
        .paginate(page=page, per_page=25)
    )
    return render_template(
        "plan.html", context="version", plan_dates=plan_dates, work=work
    )


@plan_blueprint.route("/work_select_milestone/", methods=["POST"])
@login_required
@role_required(roles=[User.Role.wp_manager])
def work_select_milestone():
    form = WorkChangeMilestoneForm()
    log(log.INFO, "[work_select_milestone] User[%d]", current_user.id)

    if form.is_submitted():
        work: Work = Work.query.get(form.work_id.data)
        work.milestone_id = form.ms_id.data
        work.save()
        log(
            log.INFO,
            "[work_select_milestone] User[%d] changed work [%d] milestone ",
            current_user.id,
            work.id,
        )
    return {}


@plan_blueprint.route("/work_select_location/", methods=["POST"])
@login_required
@role_required(roles=[User.Role.wp_manager])
def work_select_location():
    form = WorkChangeLocationForm()
    log(log.INFO, "[work_select_location] User[%d]", current_user.id)

    if form.is_submitted():
        work: Work = Work.query.get(form.work_id.data)
        work.location_id = form.loc_id.data
        work.save()
        log(
            log.INFO,
            "[work_select_location] User[%d] work [%d] location ",
            current_user.id,
            work.id,
        )
    return {}
