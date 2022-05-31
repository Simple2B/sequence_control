import os
import pytest
from app.controllers.read_file import read_file


@pytest.mark.skip(reason="no way of currently testing this")
def test_read_file():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../"))
    file_path = os.path.join(BASE_DIR, "CLIENT_DATA/test_data.xlsx")
    data = read_file(file_path)
    assert data
