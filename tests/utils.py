from app.models import User
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


def create_project(client):
    create_admin_register("admin")

    login(client, "admin")
    PROJECT_NAME = "Test_Project"
    PROJECT_NUMBER = "S-2-B"
    PROJECT_LOCATION = "TEST_LOCAL"
    START_DATE = datetime.now().date()
    END_DATE = (datetime.now() + timedelta(days=30)).date()
    client.post(
        "/project_add",
        data=dict(
            name=PROJECT_NAME,
            number=PROJECT_NUMBER,
            location=PROJECT_LOCATION,
            start_date=START_DATE,
            end_date=END_DATE,
            manager_id=1,
        ),
        follow_redirects=True,
    )
