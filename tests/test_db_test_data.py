# flake8: noqa F401
from .conftest import client
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


def test_add_db_test_data(client):
    fill_test_data(2)
    users = User.query.all()
    projects = Project.query.all()
    work_packages = WorkPackage.query.all()
    buildings = Building.query.all()
    levels = Level.query.all()
    locations = Location.query.all()
    milestones = ProjectMilestone.query.all()
    wp_milestones = WPMilestone.query.all()

    a = []
