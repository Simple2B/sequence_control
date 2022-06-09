from tests.utils import create_manager, login, create_project
from app.models import WorkPackage, User


# flake8: noqa F401
from .conftest import client


def test_add_work_package(client):
    create_project(client)
    create_manager(
        "manager",
        role=User.Role.project_manager,
    )

    login(client, "manager")

    PACKAGE_NAME = "Test_Milestone"
    PACKAGE_NUMBER = "S-2-B"
    CONTRACTOR_NAME = "Test Contractor"
    PROJECT_ID = 1
    work_packages = WorkPackage.query.all()

    assert not work_packages

    response = client.post(
        "/work_package_add",
        data=dict(
            name=PACKAGE_NAME,
            number=PACKAGE_NUMBER,
            contractor_name=CONTRACTOR_NAME,
            project_id=PROJECT_ID,
        ),
        follow_redirects=True,
    )
    assert b"Work Package Registration  is successful" in response.data
    work_packages = WorkPackage.query.all()

    assert len(work_packages) == 1
    work_package: WorkPackage = work_packages[0]
    assert work_package.name == PACKAGE_NAME
    assert work_package.number == PACKAGE_NUMBER
    assert work_package.contractor_name == CONTRACTOR_NAME
    assert work_package.project_id == PROJECT_ID

    # test adding work package with existing number
    PACKAGE_NAME2 = "Test Name 2"
    response = client.post(
        "/work_package_add",
        data=dict(
            name=PACKAGE_NAME,
            number=PACKAGE_NUMBER,
            contractor_name=CONTRACTOR_NAME,
            project_id=PROJECT_ID,
        ),
        follow_redirects=True,
    )
    assert b"This number is already registered" in response.data
    work_packages = WorkPackage.query.all()

    assert len(work_packages) == 1
    work_package: WorkPackage = work_packages[0]
    assert work_package.name == PACKAGE_NAME
    assert work_package.number == PACKAGE_NUMBER
