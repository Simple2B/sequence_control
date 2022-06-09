from tests.utils import create_admin_register, login, logout
from app.models import User


def test_add_users(client):

    create_admin_register("admin")

    response = login(client, "admin")
    USER_NAME = "sam"
    PASSWORD = "password"
    project_managers = User.query.filter(User.role == User.Role.project_manager).all()
    assert not project_managers
    response = client.post(
        "/project_manager_add",
        data=dict(
            username=USER_NAME,
            email="sam@test.com",
            password=PASSWORD,
            password_confirmation=PASSWORD,
            company_name="test_name",
            position="test_pm",
        ),
        follow_redirects=True,
    )
    assert b"Registration successful." in response.data
    project_managers = User.query.filter(User.role == User.Role.project_manager).all()
    assert len(project_managers) == 1
    pm: User = project_managers[0]
    assert pm.username == USER_NAME
    assert pm.role == User.Role.project_manager

    # test adding user with existing name
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
    assert b"This username is taken." in response.data
    project_managers = User.query.filter(User.role == User.Role.project_manager).all()
    assert len(project_managers) == 1
    assert project_managers[0].username == USER_NAME

    # check to see there is only one admin
    admins = User.query.filter(User.role == User.Role.admin).all()
    assert len(admins) == 1
    admin: User = admins[0]
    assert admin.username == "admin"
    assert admin.role == User.Role.admin

    # test adding admin
    ADMIN2 = "admin2"
    ADMIN_EMAIL = "admin@gmail.com"
    response = client.post(
        "/admin_add",
        data=dict(
            username=ADMIN2,
            email=ADMIN_EMAIL,
            password="password",
            password_confirmation="password",
            company_name="test_name",
            position="test_pm",
        ),
        follow_redirects=True,
    )
    assert b"Registration successful." in response.data
    admins = User.query.filter(User.role == User.Role.admin).all()
    assert len(admins) == 2
    admin: User = admins[1]
    assert admin.username == ADMIN2
    assert admin.role == User.Role.admin

    # check if only admins can create admins
    logout(client)
    res = login(client, USER_NAME)
    assert res

    ADMIN3 = "cant_create_admin"
    ADMIN_EMAIL = "admin3@gmail.com"
    response = client.post(
        "/admin_add",
        data=dict(
            username=ADMIN3,
            email=ADMIN_EMAIL,
            password="password",
            password_confirmation="password",
            company_name="test_name",
            position="test_pm",
        ),
        follow_redirects=True,
    )
    admins = User.query.filter(User.role == User.Role.admin).all()
    assert len(admins) == 2
    admin: User = admins[1]
    assert admins[1].username == ADMIN2
    assert admins[0].username == "admin"
