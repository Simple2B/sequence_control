# import os
from datetime import datetime
from flask.testing import FlaskClient
from app.models import Work, PlanDate, Reason
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
    assert not atp_work.reason_id
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

    REASONS = [
        "Outstanding Design, Consultant, Subcontractor & Supplier design Information, TQ's and RFI's, Design approvals"
    ]
    for reason in REASONS:
        Reason(name=reason).save()

    reason: Reason = Reason.query.first()
    assert reason

    response = manager.post(
        "/work_select_reason",
        data=dict(work_id=atp_work.id, reason_id=reason.id),
        follow_redirects=True,
    )

    assert atp_work.reason_id == reason.id
