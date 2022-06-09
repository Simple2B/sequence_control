from datetime import datetime, timedelta
from tests.utils import create_admin_register, login, create_manager
from app.models import Project


def test_add_project(client):

    create_admin_register("admin")
    manager_id = create_manager("manager")

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
            manager_id=manager_id,
        ),
        follow_redirects=True,
    )
    assert b"Project Registration  is successful." in response.data
    projects = Project.query.all()

    assert len(projects) == 1
    project: Project = projects[0]
    assert project.name == PROJECT_NAME
    assert project.number == PROJECT_NUMBER

    # test adding project with existing name
    PROJECT_NAME2 = "Test_Project_2"
    response = client.post(
        "/project_add",
        data=dict(
            name=PROJECT_NAME2,
            number=PROJECT_NUMBER,
            location=PROJECT_LOCATION,
            start_date=START_DATE,
            end_date=END_DATE,
            manager_id=manager_id,
        ),
        follow_redirects=True,
    )
    assert b"This number is already registered." in response.data
    projects = Project.query.all()

    assert len(projects) == 1
    project: Project = projects[0]
    assert project.name == PROJECT_NAME
    assert project.number == PROJECT_NUMBER
