import os
from flask.testing import FlaskClient
from app.models import Work


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
