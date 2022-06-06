from tests.utils import create_manager, login, logout
from app.models import User, Building, Level, Location


# flake8: noqa F401
from .conftest import client


def test_add_location(client):

    create_manager(
        "manager", role=User.Role.project_manager, email="manager@manager.com"
    )

    login(client, "manager")

    BUILDING_NAME = "Test_Building"
    PROJECT_ID = 1
    buildings = Building.query.all()

    assert not buildings

    response = client.post(
        "/building_add",
        data=dict(
            name=BUILDING_NAME,
            project_id=PROJECT_ID,
        ),
        follow_redirects=True,
    )
    assert b"Building Registration  is successful." in response.data
    buildings = Building.query.all()

    assert len(buildings) == 1
    building: Building = buildings[0]
    assert building.name == BUILDING_NAME
    assert building.project_id == PROJECT_ID

    # adding level
    LEVEL_NAME = "Test Level"
    BUILDING_ID = building.id
    response = client.post(
        "/level_add",
        data=dict(
            name=LEVEL_NAME,
            building_id=BUILDING_ID,
        ),
        follow_redirects=True,
    )
    assert b"Level Registration  is successful." in response.data
    levels = Level.query.all()

    assert len(levels) == 1
    level: Level = levels[0]
    assert level.name == LEVEL_NAME
    assert level.building_id == BUILDING_ID

    LOCATION_NAME = "Test Location"
    LOCATION_DESCRIPTION = "Test Description"
    LEVEL_ID = level.id
    response = client.post(
        "/location_add",
        data=dict(
            name=LOCATION_NAME, description=LOCATION_DESCRIPTION, level_id=LEVEL_ID
        ),
        follow_redirects=True,
    )
    assert b"Location Registration  is successful." in response.data
    locations = Location.query.all()

    assert len(locations) == 1
    location: Location = locations[0]
    assert location.name == LOCATION_NAME
    assert location.level_id == LEVEL_ID
    assert location.description == LOCATION_DESCRIPTION

    response = client.get(
        "/define/locations",
        follow_redirects=True,
    )
