from datetime import datetime
import pandas as pd
import numpy as np
from sqlalchemy.exc import IntegrityError
from app.models import Work, PlanDate, ProjectMilestone, Location, Level, Building
from app import db


def import_data_file(file_path: str, wp_id: int) -> bool:
    data = pd.read_excel(file_path, sheet_name=None)
    if not data:
        return False
    START_INDEX = 2

    for sheet_name in data:
        # check can we read only sheets with types we need and skip others
        try:
            work_type: Work.Type = Work.Type[sheet_name]
            sheet = data[sheet_name]
            if sheet[sheet.columns[2]][0].lower() == "zone":
                rows = sheet[[sheet.columns[1], sheet.columns[3], sheet.columns[4]]]
            else:
                rows = sheet[[sheet.columns[1], sheet.columns[2], sheet.columns[3]]]
            rows = rows[START_INDEX:]
            for _, row in rows.iterrows():
                if row[0] is np.NAN:
                    continue
                work = Work(
                    wp_id=wp_id,
                    type=work_type,
                    ppc_type=Work.ppc_type_by_type(work_type),
                    deliverable=row[0],
                    reference=row[1],
                ).save()
                if isinstance(row[2], datetime):
                    PlanDate(date=row[2].date(), work_id=work.id).save()
        except KeyError:
            continue
    return True


def import_milestone_file(file_path: str, project_id: int) -> bool:
    data = pd.read_excel(file_path, sheet_name=None)
    if not data:
        return False

    for sheet_name in data:

        # check can we read only sheets with types we need and skip others
        sheet = data[sheet_name]

        rows = sheet[[sheet.columns[0], sheet.columns[1], sheet.columns[2]]]
        for _, row in rows.iterrows():
            if np.NAN in [row[0], row[1], row[2]]:
                continue
            try:
                ProjectMilestone(
                    name=row[0],
                    description=row[1],
                    baseline_date=row[2].date(),
                    project_id=project_id,
                ).save()
            except IntegrityError:
                db.session.rollback()
                continue
            except AttributeError:
                continue
    return True


def import_location_file(file_path: str, project_id: int) -> bool:
    data = pd.read_excel(file_path, sheet_name=None)
    if not data:
        return False

    for sheet_name in data:

        # check can we read only sheets with types we need and skip others
        sheet = data[sheet_name]

        rows = sheet[[sheet.columns[0], sheet.columns[1], sheet.columns[2]]]
        for _, row in rows.iterrows():
            if np.NAN in [row[0], row[1], row[2]]:
                continue
            building: Building = Building.query.filter(
                Building.name.like(f"%{row[0]}%", Building.project_id == project_id)
            ).first()
            if not building:
                building = Building(
                    name=row[0],
                    project_id=project_id,
                ).save()

            level: Level = Level.query.filter(
                Level.name.like(f"%{row[1]}%"), Level.building_id == building.id
            ).first()
            if not level:
                level = Level(
                    name=row[1],
                    building_id=building.id,
                ).save()

            Location(
                name=row[2],
                level_id=level.id,
            ).save()

    return True
