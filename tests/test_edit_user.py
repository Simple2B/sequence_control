from flask.testing import FlaskClient
from app.models import User
from tests.utils import login


def test_add_location(manager: FlaskClient):
    user: User = User.query.filter(User.username == "manager").first()
    OLD_PASSWORD = "manager"
    response = login(manager, OLD_PASSWORD)
    assert response
    before_password_hash = user.password_hash
    NEW_PASSWORD = "Super_SEcret_PasWord"
    manager.post(
        "/user_edit",
        data=dict(password=NEW_PASSWORD, password_confirmation=NEW_PASSWORD),
        follow_redirects=True,
    )
    assert response
    after_hash = user.password_hash
    assert before_password_hash != after_hash
