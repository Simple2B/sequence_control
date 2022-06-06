from app.models import User


def create_admin_register(username, email="username@test.com", password="password"):
    user = User(
        username=username,
        email=email,
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
):
    user = User(
        username=username,
        email=email,
        password=password,
        company="ADMIN_COMPANY",
        wp_responsible="ADMIN_WP_RES",
        role=role,
    )

    user.save()
    return user.id


def login(client, username, password="password"):
    return client.post(
        "/login", data=dict(user_id=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
