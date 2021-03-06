from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

from app.logger import log


def role_required(roles):
    """
    Modified login_required decorator to restrict access to views.
    """

    def wrap(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.role not in roles:
                flash("You don't have permission to access this resource.", "danger")
                log(
                    log.WARNING,
                    "User [%s] has not permissions for the action",
                    current_user,
                )
                return redirect(url_for("main.define"))
            return func(*args, **kwargs)

        return decorated_view

    return wrap
