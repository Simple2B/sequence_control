from wsgi import add_reasons
from tests.utils import create_admin_register, login
from app.models import Reason


def test_add_reasons_cli(client):
    add_reasons()


def test_add_reasons(client):
    create_admin_register("admin")

    login(client, "admin")
    REASON_NAME = "Test_REASON"

    reasons = Reason.query.all()

    assert not reasons

    client.post(
        "/reason_add",
        data=dict(
            name=REASON_NAME,
        ),
        follow_redirects=True,
    )
    reasons = Reason.query.all()

    assert len(reasons) == 1
    reason: reason = reasons[0]
    assert reason.name == REASON_NAME
