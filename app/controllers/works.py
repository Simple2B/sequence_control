from flask import session
from flask_login import current_user
from app.models import User, Work, WorkPackage


def get_works_for_project(ppc_type: Work.PpcType = None, type: Work.Type = None):
    if current_user.role == User.Role.wp_manager:
        wp_id = session.get("wp_id")
        if wp_id:
            wp_id = int(wp_id)
            if type:
                return Work.query.filter_by(
                    deleted=False, wp_id=wp_id, type=type, wp_manager_id=current_user.id
                )
            if ppc_type:
                return Work.query.filter_by(
                    deleted=False,
                    wp_id=wp_id,
                    ppc_type=ppc_type,
                    wp_manager_id=current_user.id,
                )
            return Work.query.filter_by(
                deleted=False, wp_id=wp_id, wp_manager_id=current_user.id
            )
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

            query = Work.query.filter_by(deleted=False)
            if type:
                query = query.filter_by(type=type)
                return query.filter(Work.wp_id.in_(wp_ids))

            if ppc_type:
                query = query.filter_by(ppc_type=ppc_type)
                return query.filter(Work.wp_id.in_(wp_ids))

            return query.filter(Work.wp_id.in_(wp_ids))
