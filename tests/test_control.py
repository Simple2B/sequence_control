# import os
from datetime import datetime, timedelta
from flask.testing import FlaskClient
from app.models import Work, PlanDate, Reason
from .utils import create_work_package


def test_control(manager: FlaskClient):
    # creating wp and work
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

    # checking control page
    response = manager.get(
        "/control",
        follow_redirects=True,
    )
    assert response
    # assert to see table and work details in response
    assert b"Type" in response.data
    assert b"Deliv" in response.data
    assert b"Ref No." in response.data
    assert b"Responsible" in response.data
    assert b"ATP1" in response.data
    assert b"test_deliverable" in response.data
    assert b"test_ref" in response.data
    assert b"2003-09-25" in response.data
    assert b"TEST_CONTRACTOR" in response.data

    # adding reasons
    REASONS = [
        "Outstanding Design, Consultant, Subcontractor & Supplier design Information, TQ's and RFI's, Design approvals"
    ]
    for reason in REASONS:
        Reason(name=reason).save()

    reason: Reason = Reason.query.first()
    assert reason

    # check for select reason
    assert not atp_work.reason_id

    response = manager.post(
        "/work_select_reason",
        data=dict(work_id=atp_work.id, reason_id=reason.id),
        follow_redirects=True,
    )

    assert atp_work.reason_id == reason.id

    # check for date edit
    old_date = atp_work.latest_date
    old_version = atp_work.latest_date_version
    assert old_version == 1

    response = manager.get(
        f"/edit_work_date/{atp_work.id}",
        follow_redirects=True,
    )
    assert response

    new_date = (old_date + timedelta(days=10)).date()

    response = manager.post(
        f"/edit_work_date/{atp_work.id}",
        data=dict(
            new_plan_date=new_date,
        ),
        follow_redirects=True,
    )
    assert response

    atp_work: Work = Work.query.filter(Work.ppc_type == Work.PpcType.atp).first()
    assert atp_work.latest_date.date() == new_date
    assert atp_work.latest_date_version == 2

    # check edit notes
    assert not atp_work.note
    NEW_NOTE = "THIS IS AWESOME NOTE !!!"
    response = manager.post(
        f"/edit_work_note/{atp_work.id}",
        data=dict(reference=atp_work.reference, note=NEW_NOTE),
        follow_redirects=True,
    )

    assert atp_work.note == NEW_NOTE

    # check edit notes
    assert not atp_work.complete

    response = manager.post(
        "/work_select_complete",
        data=dict(work_id=atp_work.id, complete="yes"),
        follow_redirects=True,
    )

    assert atp_work.complete == "yes"
