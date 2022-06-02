import pytest
from app import db, create_app
from tests.utils import register, login
from app.models import User


@pytest.fixture
def client():
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


def test_add_project_manager(client):

    register("admin")

    response = login(client, "admin")
    USER_NAME = "sam"
    project_managers = User.query.filter(User.role == User.Role.project_manager).all()
    assert not project_managers
    response = client.post(
        "/project_manager_add",
        data=dict(
            username=USER_NAME,
            email="sam@test.com",
            password="password",
            password_confirmation="password",
            company_name="test_name",
            position="test_pm",
        ),
        follow_redirects=True,
    )
    assert b"Registration successful." in response.data
    project_managers = User.query.filter(User.role == User.Role.project_manager).all()
    assert len(project_managers) == 1
    assert project_managers[0].username == USER_NAME
