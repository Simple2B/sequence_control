import tempfile
from flask import Blueprint, render_template, request, session, redirect
from flask.helpers import url_for
from flask_login import current_user, login_required
from app.controllers import role_required, import_data_file, get_works_for_project
from app.logger import log
from app.models import User, Work
from app.forms import ImportFileForm

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
    type = request.args.get("type", "", type=str)
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
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
