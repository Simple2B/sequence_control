from flask import Blueprint, redirect, render_template, request
from flask.helpers import url_for
from flask_login import current_user, login_required
from app.controllers import role_required

from app.models import User, Project


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
@login_required
def index():
    return redirect(url_for("main.define"))


@main_blueprint.route("/define")
@login_required
def define():
    user: User = current_user
    if user.role in (User.Role.admin, User.Role.project_manager):
        return redirect(url_for("main.define_users"))
    if user.role == User.Role.viewer:
        return redirect(url_for("main.define_for_viewer"))
    return redirect(url_for("main.define_wp_milestones"))


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


@main_blueprint.route("/define/define_wp_milestones")
@role_required(roles=[User.Role.wp_manager])
@login_required
def define_wp_milestones():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    search_result = User.query.filter_by(deleted=False)
    query = query.strip()
    if query:
        search_result = search_result.filter(User.name.like(f"%{query}%"))
    wp_milestones = search_result.paginate(page=page, per_page=15)
    return render_template(
        "define.html",
        context="wp_milestones",
        wp_milestones=wp_milestones,
    )


@main_blueprint.route("/define/viewer")
@role_required(roles=[User.Role.admin, User.Role.project_manager])
@login_required
def define_for_viewer():
    nothing = []
    return render_template(
        "define.html",
        context="viewer",
        nothing=nothing,
    )


@main_blueprint.route("/define/projects")
@role_required(roles=[User.Role.admin])
@login_required
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
