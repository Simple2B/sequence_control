import pytest
from typing import Iterator
from flask.testing import FlaskClient
from app import db, create_app
from .utils import (
    create_admin_register,
    create_manager,
    create_project,
    create_work_package,
    create_milestone,
)
from app.models import User, Reason


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


@pytest.fixture
def admin(client: FlaskClient) -> Iterator[FlaskClient]:
    create_admin_register("admin")
    # adding reasons
    REASONS = [
        "Outstanding Design",
        "Consultant",
        "Subcontractor & Supplier design Information",
        "TQ's and RFI's",
        "Design approvals",
    ]
    for reason in REASONS:
        Reason(name=reason).save()
    yield client


@pytest.fixture
def manager(admin: FlaskClient) -> Iterator[FlaskClient]:
    manager_id = create_manager("manager")
    project_id = create_project(manager_id)
    create_manager("wp_manager", role=User.Role.wp_manager)
    admin.post(
        "/login",
        data=dict(user_id="manager", password="password"),
        follow_redirects=True,
    )
    admin.post(
        "/project_choose",
        data=dict(name=str(project_id)),
        follow_redirects=True,
    )
    yield admin


@pytest.fixture
def wp_manager(manager: FlaskClient) -> Iterator[FlaskClient]:
    package_id = create_work_package(3)
    create_milestone()
    manager.post(
        "/login",
        data=dict(user_id="wp_manager", password="password"),
        follow_redirects=True,
    )
    manager.post(
        "/work_package_choose",
        data=dict(number=str(package_id)),
        follow_redirects=True,
    )
    yield manager
