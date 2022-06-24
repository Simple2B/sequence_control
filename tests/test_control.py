from datetime import datetime, timedelta
from flask.testing import FlaskClient
from sqlalchemy import desc
from app.models import Work, PlanDate, Reason
from .utils import create_work_package


def test_control(manager: FlaskClient):

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
    work.date_planed = date
    work.save()

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

    assert not atp_work.is_completed
    manager.post(
        f"/complete/{atp_work.id}",
        follow_redirects=True,
    )
    assert atp_work.is_completed


def test_control_date_filtering(manager: FlaskClient):

    date_today = datetime.now()
    date_today = date_today.date()
    reason: Reason = Reason.query.first()
    assert reason
    # creating wp and work
    wp_id = create_work_package(3)
    work = Work(
        wp_id=wp_id,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="work",
        reference="work",
        date_planed=date_today,
    ).save()
    assert work
    PlanDate(
        date=date_today,
        work_id=work.id,
        user_id=2,
    ).save()

    date_week_before = date_today - timedelta(weeks=1)
    work2 = Work(
        wp_id=wp_id,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="work2",
        reference="work2",
        date_planed=date_week_before,
    ).save()
    PlanDate(
        date=date_week_before,
        work_id=work2.id,
        user_id=2,
    ).save()

    date_three_weeks_before = date_today - timedelta(weeks=3)
    work3 = Work(
        wp_id=wp_id,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="work3",
        reference="work3",
        date_planed=date_three_weeks_before,
    ).save()

    PlanDate(
        date=date_three_weeks_before,
        work_id=work3.id,
        user_id=2,
    ).save()

    date_three_weeks_after = date_today + timedelta(weeks=2, days=6)
    work4 = Work(
        wp_id=wp_id,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="work4",
        reference="work4",
        date_planed=date_three_weeks_after,
    ).save()
    PlanDate(
        date=date_three_weeks_after,
        work_id=work4.id,
        user_id=2,
    ).save()

    date_week_after = date_today + timedelta(days=6)
    work5 = Work(
        wp_id=wp_id,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="work5",
        reference="work5",
        date_planed=date_week_after,
    ).save()
    PlanDate(
        date=date_week_after,
        work_id=work5.id,
        user_id=2,
    ).save()

    atp_work: Work = Work.query.all()
    assert len(atp_work) == 5

    FILTER = -3
    response = manager.get(
        f"/control?filter={FILTER}",
        follow_redirects=True,
    )
    assert response

    assert b"work" in response.data
    assert b"work2" in response.data
    assert b"work3" in response.data
    assert b"work4" not in response.data
    assert b"work5" not in response.data

    FILTER = -1
    response = manager.get(
        f"/control?filter={FILTER}",
        follow_redirects=True,
    )
    assert response

    assert b"work" in response.data
    assert b"work2" in response.data
    assert b"work3" not in response.data
    assert b"work4" not in response.data
    assert b"work5" not in response.data

    FILTER = 1
    response = manager.get(
        f"/control?filter={FILTER}",
        follow_redirects=True,
    )
    assert response

    assert b"work" in response.data
    assert b"work2" not in response.data
    assert b"work3" not in response.data
    assert b"work4" not in response.data
    assert b"work5" in response.data

    FILTER = 3
    response = manager.get(
        f"/control?filter={FILTER}",
        follow_redirects=True,
    )
    assert response

    assert b"work" in response.data
    assert b"work2" not in response.data
    assert b"work3" not in response.data
    assert b"work4" in response.data
    assert b"work5" in response.data
