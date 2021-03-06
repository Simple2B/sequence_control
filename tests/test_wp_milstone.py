# from tests.utils import create_manager, login, logout, create_project
from flask.testing import FlaskClient
from app.models import WPMilestone, ProjectMilestone
from datetime import datetime, timedelta


def test_add_milestone(manager: FlaskClient):

    MILESTONE_NAME = "Test_Milestone"
    MILESTONE_DESCRIPTION = "S-2-B"
    MILESTONE_BASELINE = (datetime.now() + timedelta(days=30)).date()
    PROJECT_ID = 1
    milestones = ProjectMilestone.query.all()

    assert not milestones

    response = manager.post(
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


def test_add_wp_milestone(wp_manager: FlaskClient):

    WP_MILESTONE_NAME = "Test_Project"
    WP_MILESTONE_DESCRIPTION = "S-2-B"
    WP_MILESTONE_BASELINE = (datetime.now() + timedelta(days=30)).date()
    PROJECT_MILESTONE_ID = 1
    wp_milestones = WPMilestone.query.all()

    assert not wp_milestones

    response = wp_manager.post(
        "/wp_milestone_add",
        data=dict(
            name=WP_MILESTONE_NAME,
            description=WP_MILESTONE_DESCRIPTION,
            baseline_date=WP_MILESTONE_BASELINE,
            project_milestone_id=1,
        ),
        follow_redirects=True,
    )
    assert b"Milestone Registration  is successful." in response.data
    wp_milestones = WPMilestone.query.all()

    assert len(wp_milestones) == 1
    wp_milestone: WPMilestone = wp_milestones[0]
    assert wp_milestone.name == WP_MILESTONE_NAME
    assert wp_milestone.description == WP_MILESTONE_DESCRIPTION
    assert wp_milestone.project_milestone_id == 1

    # test adding milestone with existing name
    WP_MILESTONE_DESCRIPTION2 = "S-3-B"
    response = wp_manager.post(
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
