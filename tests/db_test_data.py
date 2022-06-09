from datetime import datetime, timedelta
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
from app.logger import log
from .utils import create_manager


def create_project(number: int, manager_id: int):
    PROJECT_NAME = f"{manager_id}-{number}-Test_Project"
    PROJECT_NUMBER = f"{manager_id}-{number}-S-2-B"
    PROJECT_LOCATION = f"{manager_id}-{number}-TEST_LOCAL"
    START_DATE = datetime.now().date()
    END_DATE = (datetime.now() + timedelta(days=number)).date()

    project = Project(
        name=PROJECT_NAME,
        number=PROJECT_NUMBER,
        location=PROJECT_LOCATION,
        start_date=START_DATE,
        end_date=END_DATE,
        manager_id=manager_id,
    ).save()
    return project.id


def fill_test_data(amount: int = 2):
    log(log.INFO, "start to fill test data")
    EMAIL = "@g.com"
    ADMIN_NAME = "admin"
    MANAGER_NAME = "manager"
    WP_MANAGER = "wp_manager"
    admin = User(
        username=ADMIN_NAME,
        email=ADMIN_NAME + EMAIL,
        password="password",
        company="ADMIN_COMPANY",
        wp_responsible="ADMIN_WP_RES",
        role=User.Role.admin,
    ).save()

    for i in range(amount):
        project_manager_id = create_manager(
            f"{i}-{MANAGER_NAME}",
            role=User.Role.project_manager,
            email=f"{i}{MANAGER_NAME}" + EMAIL,
            subordinate_id=admin.id,
        )
        for j in range(amount):
            project_id = create_project(j, project_manager_id)

            wp_manager_id = create_manager(
                username=f"{project_manager_id}-{j}-{WP_MANAGER}",
                role=User.Role.wp_manager,
                email=f"{j}{WP_MANAGER}" + EMAIL,
                subordinate_id=project_manager_id,
            )
            WorkPackage(
                name=f"{project_id}-{project_manager_id}-{j}-WorkPackage",
                number=f"{project_manager_id}-{j}-{i}-number",
                contractor_name=f"{j}-Contractor",
                project_id=project_id,
                manager_id=wp_manager_id,  # pm or wpm id
            ).save()

            for build in range(2):
                building = Building(
                    name=f"{project_id}-Building-{build}",
                    project_id=project_id,
                ).save()
                for lev in range(5):
                    level = Level(
                        name=f"{building.id}-Level-{lev}",
                        building_id=building.id,
                    ).save()
                    for loc in range(3):
                        Location(
                            name=f"{level.id}-Location-{loc}",
                            description=f"{level.id}-description-{loc}",
                            level_id=level.id,
                        ).save()

            for mile in range(2):
                milestone = ProjectMilestone(
                    name=f"{project_id}-Milestone-{mile}",
                    description=f"{project_id}-description-{mile}",
                    baseline_date=(datetime.now() + timedelta(days=mile + 1)).date(),
                    project_id=project_id,
                ).save()
                for wp_mile in range(2):
                    WPMilestone(
                        name=f"{project_id}-{milestone.id}-WorkPackageMilestone-{wp_mile}",
                        description=f"{project_id}-{milestone.id}-description-{wp_mile}",
                        baseline_date=(
                            datetime.now() + timedelta(days=wp_mile + 1)
                        ).date(),
                        wp_manager_id=wp_manager_id,  # who's id
                        project_milestone_id=milestone.id,
                    ).save()
