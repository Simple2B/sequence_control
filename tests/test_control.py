# import os
from datetime import datetime, timedelta
from flask.testing import FlaskClient
from sqlalchemy import desc
from app.models import Work, PlanDate, Reason
from .utils import create_work_package


def test_control(manager: FlaskClient):
    # adding reasons
    REASONS = [
        "Outstanding Design",
        "Consultant",
        "Subcontractor & Supplier design Information",
        "TQ's and RFI's",
        "Design approvals",
    ]
    for reason in REASONS:
        Reason(name=reason).save()

    reason: Reason = Reason.query.first()
    assert reason
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
        user_id=2,
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
    assert b"Deliverable" in response.data
    assert b"Ref No." in response.data
    assert b"ATP1" in response.data
    assert b"test_deliverable" in response.data
    assert b"test_ref" in response.data
    assert b"2003-09-25" in response.data

    # checking old current information
    old_date = atp_work.latest_date
    old_version = atp_work.latest_date_version
    assert old_version == 1

    # simulating new reforecast
    new_date = (old_date + timedelta(days=10)).date()
    reason = "Consultant"
    note = "THIS IS AWESOME NOTE !!!"
    responsible = "TEST_CONTRACTOR"

    response = manager.post(
        f"/reforecast/{atp_work.id}",
        data=dict(
            new_plan_date=new_date, reason=reason, note=note, responsible=responsible
        ),
        follow_redirects=True,
    )

    # checking if information have changed
    atp_work: Work = Work.query.filter(Work.ppc_type == Work.PpcType.atp).first()
    plan_dates: PlanDate = (
        PlanDate.query.filter_by(work_id=atp_work.id)
        .order_by(desc(PlanDate.version))
        .all()
    )
    assert len(plan_dates) == 2
    assert atp_work.latest_date.date() == new_date
    assert atp_work.latest_date_version == 2
    plan_date: PlanDate = plan_dates[0]
    assert plan_date.reason == reason
    assert plan_date.responsible == responsible
    assert plan_date.note == note
