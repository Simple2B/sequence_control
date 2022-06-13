from flask import session
from flask_login import current_user

from app.logger import log
from app.models import User, Work, PlanDate, WorkPackage


def get_works_for_project(ppc_type: Work.PpcType, type: Work.Type = None):
    if current_user.role == User.Role.wp_manager:
        wp_id = session.get("wp_id")
        if wp_id:
            wp_id = int(wp_id)
            if type:
                return Work.query.filter_by(deleted=False, wp_id=wp_id, type=type)
            else:
                return Work.query.filter_by(
                    deleted=False, wp_id=wp_id, ppc_type=ppc_type
                )
        else:
            plan_dates_ids = []
            log(log.ERROR, "[get_works_for_project] No wp_id in session!")
    else:
        project_id = session.get("project_id")
        if project_id:
            project_id = int(project_id)
            wp_ids = [
                wp.id
                for wp in WorkPackage.query.filter_by(
                    project_id=project_id, deleted=False
                ).all()
            ]
            query = (
                Work.query.filter_by(deleted=False, type=type)
                if type
                else Work.query.filter_by(deleted=False, ppc_type=ppc_type)
            )
            return query.filter(Work.wp_id.in_(wp_ids))
        else:
            plan_dates_ids = []
            log(log.ERROR, "[get_works_for_project] No project_id in session!")

    return PlanDate.query.filter(PlanDate.id.in_(plan_dates_ids))