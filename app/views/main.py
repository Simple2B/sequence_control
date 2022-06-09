from flask import Blueprint, redirect, render_template, session, request
from flask.helpers import url_for
from flask_login import current_user, login_required
from app.controllers import role_required

from app.models import (
    User,
    Project,
    Reason,
    WPMilestone,
    ProjectMilestone,
    WorkPackage,
    Location,
    Building,
    Level,
)


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    return redirect(url_for("main.define"))


@main_blueprint.route("/define")
@login_required
def define():
    user: User = current_user
    if user.role == User.Role.admin:
        return redirect(url_for("main.define_users"))
    if user.role == User.Role.project_manager:
        if "project_id" in session and session["project_id"]:
            return redirect(url_for("main.define_users"))
        else:
            return redirect(url_for("project.project_choose"))
    if "wp_id" in session and session["wp_id"]:
        if user.role == User.Role.wp_manager:
            return redirect(url_for("main.define_wp_milestones"))
    if user.role == User.Role.viewer:
        if "project_id" in session and session["project_id"]:
            return redirect(url_for("plan.plan"))
        else:
            return redirect(url_for("project.project_choose"))
    return redirect(url_for("work_package.work_package_choose"))


@main_blueprint.route("/define/users")
@login_required
@role_required(roles=[User.Role.admin, User.Role.project_manager])
def define_users():
    user: User = current_user
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    search_result = User.query.filter_by(deleted=False)
    if user.role != User.Role.admin:
        search_result = search_result.filter(User.subordinate_id == user.id)
    query = query.strip()
    if query:
        search_result = search_result.filter(User.username.like(f"%{query}%"))
    users = search_result.paginate(page=page, per_page=25)
    return render_template(
        "define.html",
        context="users",
        users=users,
    )


@main_blueprint.route("/define/wp_milestones")
@login_required
@role_required(roles=[User.Role.wp_manager])
def define_wp_milestones():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    search_result = WPMilestone.query.filter_by(
        deleted=False, wp_manager_id=current_user.id
    )
    query = query.strip()
    if query:
        search_result = search_result.filter(WPMilestone.name.like(f"%{query}%"))
    wp_milestones = search_result.paginate(page=page, per_page=15)
    return render_template(
        "define.html",
        context="wp_milestones",
        wp_milestones=wp_milestones,
    )


@main_blueprint.route("/define/viewer")
@login_required
@role_required(roles=[User.Role.viewer])
def define_for_viewer():
    nothing = []
    return render_template(
        "define.html",
        context="viewer",
        nothing=nothing,
    )


@main_blueprint.route("/define/projects")
@login_required
@role_required(roles=[User.Role.admin])
def define_projects():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    search_result = Project.query.filter_by(deleted=False)
    query = query.strip()
    if query:
        search_result = search_result.filter(Project.name.like(f"%{query}%"))
    projects = search_result.paginate(page=page, per_page=25)
    return render_template(
        "define.html",
        context="projects",
        projects=projects,
    )


@main_blueprint.route("/define/reasons")
@login_required
@role_required(roles=[User.Role.admin])
def define_reasons():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    search_result = Reason.query.filter_by(deleted=False)
    query = query.strip()
    if query:
        search_result = search_result.filter(Reason.name.like(f"%{query}%"))
    reasons = search_result.paginate(page=page, per_page=25)
    return render_template(
        "define.html",
        context="reasons",
        reasons=reasons,
    )


@main_blueprint.route("/define/milestones")
@login_required
@role_required(roles=[User.Role.project_manager])
def define_milestones():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    search_result = ProjectMilestone.query.filter_by(
        deleted=False, project_id=session["project_id"]
    )
    query = query.strip()
    if query:
        search_result = search_result.filter(ProjectMilestone.name.like(f"%{query}%"))
    milestones = search_result.paginate(page=page, per_page=15)
    return render_template(
        "define.html",
        context="milestones",
        milestones=milestones,
    )


@main_blueprint.route("/define/work_packages")
@login_required
@role_required(roles=[User.Role.project_manager])
def define_work_packages():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    search_result = WorkPackage.query.filter_by(
        deleted=False, project_id=session["project_id"]
    )
    query = query.strip()
    if query:
        search_result = search_result.filter(WorkPackage.name.like(f"%{query}%"))
    work_packages = search_result.paginate(page=page, per_page=15)
    return render_template(
        "define.html",
        context="work_packages",
        work_packages=work_packages,
    )


@main_blueprint.route("/define/locations")
@login_required
@role_required(roles=[User.Role.project_manager])
def define_locations():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    project_id = session["project_id"]
    buildings = Building.query.filter(Building.project_id == project_id).all()
    building_ids = [building.id for building in buildings]
    levels = Level.query.filter(Level.building_id.in_(building_ids)).all()
    level_ids = [level.id for level in levels]
    loc_query = Location.query.filter(Location.level_id.in_(level_ids))
    search_result = loc_query.filter_by(deleted=False)
    query = query.strip()
    if query:
        search_result = search_result.filter(Location.name.like(f"%{query}%"))
    loc_query = search_result.paginate(page=page, per_page=15)
    return render_template(
        "define.html",
        context="locations",
        locations=loc_query,
    )
