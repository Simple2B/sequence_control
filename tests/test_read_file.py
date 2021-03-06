import os

from app.controllers.read_file import (
    import_data_file,
    import_milestone_file,
    import_location_file,
)
from app.models import Work, ProjectMilestone, Location, Level, Building


# @pytest.mark.skip(reason="no way of currently testing this")
def test_read_file(client):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "DATA/PPC.xlsx")

    res = import_data_file(file_path, 1, 3)
    assert res
    works: list[Work] = Work.query.all()
    assert works
    assert Work.query.filter(Work.type == Work.Type.DWG).count() == 3
    assert Work.query.filter(Work.type == Work.Type.TS).count() == 4
    assert Work.query.filter(Work.type == Work.Type.TS).count() == 4
    assert Work.query.filter(Work.type == Work.Type.HOD).count() == 4


def test_import_milestone_file(client):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "DATA/milestone.xlsx")

    res = import_milestone_file(file_path, 1)
    assert res
    milestones: list[ProjectMilestone] = ProjectMilestone.query.all()
    assert len(milestones) == 9


def test_import_location_file(client):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "DATA/location.xlsx")

    res = import_location_file(file_path, 1)
    assert res
    milestones: list[Location] = Location.query.all()
    levels: list[Level] = Level.query.all()
    buildings: list[Building] = Building.query.all()
    assert len(milestones) == 56
    assert len(levels) == 8
    assert len(buildings) == 1
