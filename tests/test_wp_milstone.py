from tests.utils import create_manager, login, logout, create_project
from app.models import WPMilestone, User, ProjectMilestone
from datetime import datetime, timedelta


# flake8: noqa F401
from .conftest import client


def test_add_wp_milestone(client):
    create_project(client)
    create_manager(
        "manager", role=User.Role.project_manager, email="manager@manager.com"
    )

    login(client, "manager")
    MILESTONE_NAME = "Test_Milestone"
    MILESTONE_DESCRIPTION = "S-2-B"
    MILESTONE_BASELINE = (datetime.now() + timedelta(days=30)).date()
    PROJECT_ID = 1
    milestones = ProjectMilestone.query.all()

    assert not milestones

    response = client.post(
        "/milestone_add",
        data=dict(
            name=MILESTONE_NAME,
            description=MILESTONE_DESCRIPTION,
            baseline_date=MILESTONE_BASELINE,
            project_id=PROJECT_ID,
        ),
        follow_redirects=True,
    )
    assert b"Milestone Registration  is successful." in response.data
    milestones = ProjectMilestone.query.all()

    assert len(milestones) == 1
    milestone: WPMilestone = milestones[0]
    assert milestone.name == MILESTONE_NAME
    assert milestone.description == MILESTONE_DESCRIPTION

    logout(client)

    create_manager(
        "wp_manager", role=User.Role.wp_manager, email="manager2@manager.com"
    )

    login(client, "wp_manager")
    WP_MILESTONE_NAME = "Test_Project"
    WP_MILESTONE_DESCRIPTION = "S-2-B"
    WP_MILESTONE_BASELINE = (datetime.now() + timedelta(days=30)).date()
    PROJECT_MILESTONE_ID = 1
    wp_milestones = WPMilestone.query.all()

    assert not wp_milestones

    response = client.post(
        "/wp_milestone_add",
        data=dict(
            name=WP_MILESTONE_NAME,
            description=WP_MILESTONE_DESCRIPTION,
            baseline_date=WP_MILESTONE_BASELINE,
            project_milestone_id=milestone.id,
        ),
        follow_redirects=True,
    )
    assert b"Milestone Registration  is successful." in response.data
    wp_milestones = WPMilestone.query.all()

    assert len(wp_milestones) == 1
    wp_milestone: WPMilestone = wp_milestones[0]
    assert wp_milestone.name == WP_MILESTONE_NAME
    assert wp_milestone.description == WP_MILESTONE_DESCRIPTION
    assert wp_milestone.project_milestone_id == milestone.id

    # test adding milestone with existing name
    WP_MILESTONE_DESCRIPTION2 = "S-3-B"
    response = client.post(
        "/wp_milestone_add",
        data=dict(
            name=WP_MILESTONE_NAME,
            description=WP_MILESTONE_DESCRIPTION2,
            baseline_date=WP_MILESTONE_BASELINE,
            project_milestone_id=PROJECT_MILESTONE_ID,
        ),
        follow_redirects=True,
    )
    assert b"This name is already registered" in response.data
    wp_milestones = WPMilestone.query.all()

    assert len(wp_milestones) == 1
    wp_milestone: WPMilestone = wp_milestones[0]
    assert wp_milestone.name == WP_MILESTONE_NAME
    assert wp_milestone.description == WP_MILESTONE_DESCRIPTION
