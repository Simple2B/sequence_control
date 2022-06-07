from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from app.controllers import role_required
from app.logger import log


from app.models import User, Work


plan_blueprint = Blueprint("plan", __name__)


@plan_blueprint.route("/plan")
@login_required
def plan():
    log(log.INFO, "User [%d] define", current_user.id)

    return render_template("plan.html")


@plan_blueprint.route("/info/<ppc_type>")
@role_required(
    roles=[User.Role.wp_manager, User.Role.project_manager, User.Role.viewer]
)
@login_required
def info(ppc_type):
    ppc_type
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    if ppc_type == "info":
        links = ["DWG", "TS", "SCH", "MDL", "CPD", "EDA", "TDRG", "TENQ", "CFO", "DSC"]
        color = "yellow"
        search_result = Work.query.filter_by(deleted=False, ppc_type=Work.PpcType.info)
    if ppc_type == "docs":
        links = ["PSD", "RAMS", "TWS", "CMS"]
        color = "blue"
        search_result = Work.query.filter_by(deleted=False, ppc_type=Work.PpcType.docs)
    if ppc_type == "quality":
        links = ["QS_QBM_P_MU", "Fab_QSO", "Ins_QSO", "QHP"]
        color = "green"
        search_result = Work.query.filter_by(
            deleted=False, ppc_type=Work.PpcType.quality
        )
    if ppc_type == "atp":
        links = ["ATP1", "ATP2", "ATP3"]
        color = "red"
        search_result = Work.query.filter_by(deleted=False, ppc_type=Work.PpcType.atp)
    if ppc_type == "hod":
        links = ["HOD"]
        color = "brown"
        search_result = Work.query.filter_by(deleted=False, ppc_type=Work.PpcType.atp)
    query = query.strip()
    if query:
        search_result = search_result.filter(Work.reference.like(f"%{query}%"))
    works = search_result.paginate(page=page, per_page=15)
    return render_template(
        "plan.html", context="info", works=works, links=links, color=color
    )
