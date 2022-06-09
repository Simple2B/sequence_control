from app.models import User, Project, WorkPackage, ProjectMilestone
from datetime import datetime, timedelta


def create_admin_register(username, email="@test.com", password="password"):
    user = User(
        username=username,
        email=username + email,
        password=password,
        company="ADMIN_COMPANY",
        wp_responsible="ADMIN_WP_RES",
        role=User.Role.admin,
    )

    user.save()
    return user.id


def create_manager(
    username,
    email="username@test.com",
    password="password",
    role=User.Role.project_manager,
    subordinate_id=1,
):
    user = User(
        username=username,
        email=username + email,
        password=password,
        company="ADMIN_COMPANY",
        # wp_responsible="ADMIN_WP_RES",
        role=role,
        position="TEST_position",
        subordinate_id=subordinate_id,
    )

    user.save()
    return user.id


def login(client, username, password="password"):
    return client.post(
        "/login", data=dict(user_id=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def create_project(manager_id):
    # create_admin_register("admin")

    # login(client, "admin")
    PROJECT_NAME = "Test_Project"
    PROJECT_NUMBER = "S-2-B"
    PROJECT_LOCATION = "TEST_LOCAL"
    START_DATE = datetime.now().date()
    END_DATE = (datetime.now() + timedelta(days=30)).date()

    project = Project(
        name=PROJECT_NAME,
        number=PROJECT_NUMBER,
        location=PROJECT_LOCATION,
        start_date=START_DATE,
        end_date=END_DATE,
        manager_id=manager_id,
    ).save()
    return project.id


def create_work_package(manager_id):

    PACKAGE_NAME = "Test_PACKAGE"
    PACKAGE_NUMBER = "S-2-B"
    CONTRACTOR_NAME = "TEST_CONTRACTOR"

    work_package = WorkPackage(
        name=PACKAGE_NAME,
        number=PACKAGE_NUMBER,
        contractor_name=CONTRACTOR_NAME,
        project_id=1,
        manager_id=manager_id,
    ).save()
    return work_package.id


def create_milestone():
    NAME = "Test_MILE_STONE"
    DESCRIPTION = "S-2-B"
    BASE_LINE_DATE = (datetime.now() + timedelta(days=30)).date()
    milestone = ProjectMilestone(
        name=NAME,
        description=DESCRIPTION,
        baseline_date=BASE_LINE_DATE,
        project_id=1,
    ).save()
    return milestone.id
