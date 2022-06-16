# import os
from datetime import timedelta, datetime
from flask.testing import FlaskClient
from app.models import Work, PlanDate
from .utils import create_work_package


def test_control(manager: FlaskClient):
    wp_id = create_work_package(3)
    work = Work(
        wp_id=wp_id,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="test_deliverable",
        reference="test_ref",
    ).save()
    assert work
    date = datetime(2003, 9, 25, 0, 0)
    PlanDate(
        date=date,
        work_id=work.id,
    ).save()

    atp_work: Work = Work.query.first()
    assert atp_work
    response = manager.get(
        "/control",
        follow_redirects=True,
    )
    assert response
    assert b"Type" in response.data
    assert b"Deliv" in response.data
    assert b"Ref No." in response.data
    assert b"Responsible" in response.data
    assert b"ATP1" in response.data
    assert b"test_deliverable" in response.data
    assert b"test_ref" in response.data
    assert b"2003-09-25" in response.data
    assert b"TEST_CONTRACTOR" in response.data
