import os

from app.controllers.read_file import read_file
from app.models.work import Work


# @pytest.mark.skip(reason="no way of currently testing this")
def test_read_file(client):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(BASE_DIR, "CLIENT_DATA/test_data.xlsx")
    file_path = os.path.join(BASE_DIR, "DATA/PPC.xlsx")

    res = read_file(file_path)
    assert res
    works: list[Work] = Work.query.all()
    assert works
    assert Work.query.filter(Work.type == Work.Type.DWG).count() == 3
    assert Work.query.filter(Work.type == Work.Type.TS).count() == 4
    assert Work.query.filter(Work.type == Work.Type.TS).count() == 4
    assert Work.query.filter(Work.type == Work.Type.HOD).count() == 4
