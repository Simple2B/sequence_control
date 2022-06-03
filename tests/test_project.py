import pytest
from app import db, create_app
from tests.utils import create_admin_register, login
from app.models import Project
from datetime import datetime, timedelta


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


def test_add_project(client):

    create_admin_register("admin")

    login(client, "admin")
    PROJECT_NAME = "Test_Project"
    PROJECT_NUMBER = "S-2-B"
    PROJECT_LOCATION = "TEST_LOCAL"
    START_DATE = datetime.now().date()
    END_DATE = (datetime.now() + timedelta(days=30)).date()
    projects = Project.query.all()

    assert not projects

    response = client.post(
        "/project_add",
        data=dict(
            name=PROJECT_NAME,
            number=PROJECT_NUMBER,
            location=PROJECT_LOCATION,
            start_date=START_DATE,
            end_date=END_DATE,
        ),
        follow_redirects=True,
    )
    assert b"Project Registration  is successful." in response.data
    projects = Project.query.all()

    assert len(projects) == 1
    project: Project = projects[0]
    assert project.name == PROJECT_NAME
    assert project.number == PROJECT_NUMBER

    # test adding user with existing name
    PROJECT_NAME2 = "Test_Project_2"
    response = client.post(
        "/project_add",
        data=dict(
            name=PROJECT_NAME2,
            number=PROJECT_NUMBER,
            location=PROJECT_LOCATION,
            start_date=START_DATE,
            end_date=END_DATE,
        ),
        follow_redirects=True,
    )
    assert b"This number is already registered." in response.data
    projects = Project.query.all()

    assert len(projects) == 1
    project: Project = projects[0]
    assert project.name == PROJECT_NAME
    assert project.number == PROJECT_NUMBER
