import os
from datetime import timedelta, datetime
from flask.testing import FlaskClient
from app.models import Work, PlanDate
from .utils import create_work_package


def test_add_get_works(wp_manager: FlaskClient):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # creating file to post it
    file_path = os.path.join(BASE_DIR, "DATA/PPC.xlsx")
    file = open(file_path, "rb")
    # simulate importing file
    response = wp_manager.post(
        "/import_file",
        data=dict(
            file=file,
        ),
        follow_redirects=True,
    )
    assert response

    # checking do we have saved works from file
    works: list[Work] = Work.query.all()
    assert works
    assert Work.query.filter(Work.type == Work.Type.DWG).count() == 3
    assert Work.query.filter(Work.type == Work.Type.TS).count() == 4
    assert Work.query.filter(Work.type == Work.Type.TS).count() == 4
    assert Work.query.filter(Work.type == Work.Type.HOD).count() == 4

    # checking work for get requests
    ppc_type = "atp"
    atp_works = Work.query.filter(Work.ppc_type == Work.PpcType[ppc_type]).all()
    assert len(atp_works) == 10

    # checking control work(we must not see them in response)
    hod_works = Work.query.filter(Work.ppc_type == Work.PpcType.hod).all()
    assert hod_works

    # simulating request to get ATP works only
    response = wp_manager.get(
        f"/info/{ppc_type}",
        follow_redirects=True,
    )
    assert response

    # we expect to see this types in template
    assert b"ATP1" in response.data
    assert b"ATP2" in response.data
    assert b"ATP3" in response.data

    # we expect to see this Reference's in response
    assert b"ATP-00" in response.data
    assert b"ATP-11" in response.data
    assert b"ATP-88" in response.data

    # we must not see different works
    assert b"222-HOD-55" not in response.data

    response = wp_manager.get(
        f"/info/{ppc_type}?type=ATP3",
        follow_redirects=True,
    )
    assert response

    # we expect to see this Reference's in response
    assert b"ATP-00" not in response.data
    assert b"ATP-11" not in response.data
    assert b"ATP-88" in response.data
    assert b"222-HOD-55" not in response.data


def test_edit_work(wp_manager: FlaskClient):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # creating file to post it
    file_path = os.path.join(BASE_DIR, "DATA/PPC.xlsx")
    file = open(file_path, "rb")
    # simulate importing file
    response = wp_manager.post(
        "/import_file",
        data=dict(
            file=file,
        ),
        follow_redirects=True,
    )
    assert response

    atp_work: Work = Work.query.filter(Work.ppc_type == Work.PpcType.atp).first()
    assert atp_work

    old_date = atp_work.latest_date
    old_version = atp_work.latest_date_version
    assert old_version == 1

    reference = atp_work.reference
    deliverable = atp_work.deliverable
    ppc_type = atp_work.ppc_type.name
    type = atp_work.type.name
    new_date = (old_date + timedelta(days=10)).date()

    # changing only deliverable and type (and entered type with small letters)
    deliverable = "test deliverable"
    type = "atp3"

    response = wp_manager.post(
        f"/edit_work/{atp_work.id}",
        data=dict(
            reference=reference,
            new_plan_date=new_date,
            deliverable=deliverable,
            plan_date=new_date,
            ppc_type=ppc_type,
            type=type,
        ),
        follow_redirects=True,
    )
    assert response

    atp_work: Work = Work.query.filter(Work.ppc_type == Work.PpcType.atp).first()
    assert atp_work.latest_date
    assert atp_work.latest_date_version == 1

    assert atp_work.deliverable == deliverable
    assert atp_work.type.name == "ATP3"


def test_add_work(wp_manager: FlaskClient):
    all_works = Work.query.all()
    assert not all_works
    PPC_TYPE = "atp"
    TYPE = "ATP1"
    PLAN_DATE = (datetime.now() + timedelta(days=30)).date()
    REFERENCE = "ROCK-1408-AS-YL-UM-0001"
    DELIVERABLE = "Temporary test works 1"

    # creating new work with correct data and unique reference
    response = wp_manager.post(
        f"/work_add/{PPC_TYPE}?type={TYPE}",
        data=dict(plan_date=PLAN_DATE, reference=REFERENCE, deliverable=DELIVERABLE),
        follow_redirects=True,
    )
    assert response

    all_works = Work.query.all()
    assert len(all_works) == 1
    atp_works: Work = Work.query.filter(Work.ppc_type == Work.PpcType.atp).all()
    assert len(atp_works) == 1
    atp_work: Work = atp_works[0]
    assert atp_work.reference == REFERENCE
    assert atp_work.deliverable == DELIVERABLE

    # creating new work with correct data and existing reference
    response = wp_manager.post(
        f"/work_add/{PPC_TYPE}?type={TYPE}",
        data=dict(plan_date=PLAN_DATE, reference=REFERENCE, deliverable=DELIVERABLE),
        follow_redirects=True,
    )

    # cant add Deliverable with same reference and redirected to add new again
    assert b"Add new Deliverable" in response.data

    all_works = Work.query.all()
    assert len(all_works) == 1
    atp_works: Work = Work.query.filter(Work.ppc_type == Work.PpcType.atp).all()
    assert len(atp_works) == 1

    # creating new work with incorrect data
    response = wp_manager.post(
        f"/work_add/{PPC_TYPE}?type={TYPE}",
        data=dict(deliverable=DELIVERABLE),
        follow_redirects=True,
    )

    # cant add Deliverable with no data and redirected to add new again
    assert b"Add new Deliverable" in response.data

    # creating new work with correct data and no type in query
    REFERENCE2 = "ROCK-1408-AS-YL-UM-0002"
    DELIVERABLE2 = "Temporary test works 2"

    response = wp_manager.post(
        f"/work_add/{PPC_TYPE}",
        data=dict(
            plan_date=PLAN_DATE,
            reference=REFERENCE2,
            deliverable=DELIVERABLE2,
            type=TYPE,
        ),
        follow_redirects=True,
    )

    all_works = Work.query.all()
    assert len(all_works) == 2
    atp_works: Work = Work.query.filter(Work.ppc_type == Work.PpcType.atp).all()
    assert len(atp_works) == 2
    atp_work: Work = atp_works[1]
    assert atp_work.reference == REFERENCE2
    assert atp_work.deliverable == DELIVERABLE2
    plan_dates = PlanDate.query.all()
    assert len(plan_dates) == 2
    assert plan_dates[0].work_id == atp_works[0].id
    assert plan_dates[1].work_id == atp_works[1].id

    # creating new work with incorrect type
    REFERENCE3 = "ROCK-1408-AS-YL-UM-0003"
    DELIVERABLE3 = "Temporary test works 3"
    WRONG_TYPE = "RAP"
    response = wp_manager.post(
        f"/work_add/{PPC_TYPE}",
        data=dict(
            plan_date=PLAN_DATE,
            reference=REFERENCE3,
            deliverable=DELIVERABLE3,
            type=WRONG_TYPE,
        ),
        follow_redirects=True,
    )

    # cant add Deliverable with wrong type and redirected to add new again
    assert b"Add new Deliverable" in response.data

    # edit date and creates new version
    # simulating new reforecast
    new_date = (atp_work.latest_date + timedelta(days=10)).date()
    reason = "Consultant"
    note = "THIS IS AWESOME NOTE !!!"
    responsible = "TEST_CONTRACTOR"

    response = wp_manager.post(
        f"/reforecast/{atp_work.id}",
        data=dict(
            new_plan_date=new_date, reason=reason, note=note, responsible=responsible
        ),
        follow_redirects=True,
    )

    plan_dates: PlanDate = PlanDate.query.filter_by(work_id=atp_work.id).all()
    assert len(plan_dates) == 2
    assert atp_work.latest_date.date() == new_date
    assert atp_work.latest_date_version == 2
    plan_date: PlanDate = plan_dates[1]
    assert plan_date.reason == reason
    assert plan_date.responsible == responsible
    assert plan_date.note == note


def test_delete_work(manager: FlaskClient):
    wp_id = create_work_package(3)
    work = Work(
        wp_id=wp_id,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="test_deliverable",
        reference="test_ref",
    ).save()
    assert work
    response = manager.post(
        f"/delete_work/{work.id}",
        follow_redirects=True,
    )
    assert response
    assert work.deleted is True


def test_work_version_check(wp_manager: FlaskClient):
    atp_work = Work(
        wp_id=1,
        type=Work.Type.ATP1,
        ppc_type=Work.PpcType.atp,
        deliverable="test_deliverable",
        reference="test_ref",
        wp_manager_id=3,
    ).save()
    assert atp_work
    date = datetime(2003, 9, 25, 0, 0)
    PlanDate(
        date=date,
        work_id=atp_work.id,
    ).save()

    assert atp_work
    assert atp_work.latest_date
    assert atp_work.latest_date_version == 1

    response = wp_manager.get(
        f"/work_version/{1}",
        follow_redirects=True,
    )
    assert response
    assert b"Version" in response.data
    assert b"Edited by" in response.data
    assert b"Edit Date" in response.data
    assert b"Planned Date" in response.data
    assert b"Responsible" in response.data
    assert b"Note" in response.data
    assert b"Reason" in response.data
    assert b"test_ref" in response.data
    assert b"2003-09-25" in response.data
