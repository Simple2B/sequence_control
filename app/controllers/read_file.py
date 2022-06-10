from datetime import datetime
import pandas as pd
import numpy as np

from app.models import Work, PlanDate


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
