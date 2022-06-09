from .db_test_data import fill_test_data
from app.models import (
    User,
    Project,
    WorkPackage,
    Building,
    Level,
    Location,
    ProjectMilestone,
    WPMilestone,
)


def test_add_db_test_data():
    fill_test_data(2)
    users = User.query.all()
    assert users
    projects = Project.query.all()
    assert projects
    work_packages = WorkPackage.query.all()
    assert work_packages
    buildings = Building.query.all()
    assert buildings
    levels = Level.query.all()
    assert levels
    locations = Location.query.all()
    assert locations
    milestones = ProjectMilestone.query.all()
    assert milestones
    wp_milestones = WPMilestone.query.all()
    assert wp_milestones
