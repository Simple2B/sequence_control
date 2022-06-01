import os

import pytest
from app.controllers.read_file import read_file
from app.models.work import Work


@pytest.mark.skip(reason="no way of currently testing this")
def test_read_file():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../"))
    # file_path = os.path.join(BASE_DIR, "CLIENT_DATA/test_data.xlsx")
    file_path = os.path.join(BASE_DIR, "CLIENT_DATA/PPC.xlsx")

    data = read_file(file_path)
    assert data
    types = []
    for i in data:
        # check can we read only sheets with types we need and skip others
        if i in Work.Type._value2member_map_:
            sheet = data[i]
            sheet
            types.append(i)
    assert len(types) == 22
