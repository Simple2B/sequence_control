from datetime import datetime
import enum
from typing import Iterator
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin
from .wp_milestone import WPMilestone
from .location import Location
from .reasons import Reason


class Work(db.Model, ModelMixin):

    __tablename__ = "works"

    class Type(enum.Enum):
        DWG = "DWG"
        TS = "TS"
        SCH = "SCH"
        MDL = "MDL"
        CPD = "CPD"
        EDA = "EDA"
        TDRG = "TDRG"
        TENQ = "TENQ"
        CFO = "CFO"
        DSC = "DSC"
        PSD = "PSD"
        RAMS = "RAMS"
        TWS = "TWS"
        CMS = "CMS"
        QS_QBM_P_MU = "QS_QBM_P_MU"
        Fab_QSO = "Fab_QSO"
        Ins_QSO = "Ins_QSO"
        QHP = "QHP"
        ATP1 = "ATP1"
        ATP2 = "ATP2"
        ATP3 = "ATP3"
        HOD = "HOD"

    class PpcType(enum.Enum):
        info = "info"
        docs = "docs"
        quality = "quality"
        atp = "atp"
        hod = "hod"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(Enum(Type), nullable=False)
    ppc_type = db.Column(Enum(PpcType), nullable=False)
    deliverable = db.Column(db.String(255))
    reference = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    milestone_id = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    reason_id = db.Column(db.Integer, nullable=True)

    wp_id = db.Column(db.Integer, db.ForeignKey("work_packages.id"))
    work_package = relationship("WorkPackage", viewonly=True)
    plan_dates = relationship(
        "PlanDate", viewonly=True, order_by="asc(PlanDate.version)"
    )

    def __repr__(self):
        return f"< {self.id} {self.type} {self.deliverable} >"

    @staticmethod
    def ppc_type_by_type(type: Type) -> PpcType:
        return {
            Work.Type.DWG: Work.PpcType.info,
            Work.Type.TS: Work.PpcType.info,
            Work.Type.SCH: Work.PpcType.info,
            Work.Type.MDL: Work.PpcType.info,
            Work.Type.CPD: Work.PpcType.info,
            Work.Type.EDA: Work.PpcType.info,
            Work.Type.TDRG: Work.PpcType.info,
            Work.Type.TENQ: Work.PpcType.info,
            Work.Type.CFO: Work.PpcType.info,
            Work.Type.DSC: Work.PpcType.info,
            Work.Type.PSD: Work.PpcType.docs,
            Work.Type.RAMS: Work.PpcType.docs,
            Work.Type.TWS: Work.PpcType.docs,
            Work.Type.CMS: Work.PpcType.docs,
            Work.Type.QS_QBM_P_MU: Work.PpcType.quality,
            Work.Type.Fab_QSO: Work.PpcType.quality,
            Work.Type.Ins_QSO: Work.PpcType.quality,
            Work.Type.QHP: Work.PpcType.quality,
            Work.Type.ATP1: Work.PpcType.atp,
            Work.Type.ATP2: Work.PpcType.atp,
            Work.Type.ATP3: Work.PpcType.atp,
            Work.Type.HOD: Work.PpcType.hod,
        }[type]

    @property
    def latest_date(self) -> datetime:
        from app.models import PlanDate

        try:
            plan_date: PlanDate = self.plan_dates[-1]
        except IndexError:
            return ""
        return plan_date.date

    @property
    def latest_date_version(self) -> int:
        from app.models import PlanDate

        try:
            plan_date: PlanDate = self.plan_dates[-1]
        except IndexError:
            return ""
        return plan_date.version

    @property
    def color(self) -> str:
        duplicates = Work.query.filter_by(
            reference=self.reference, wp_id=self.wp_id
        ).count()
        a = [
            value
            for _, value in self.__dict__.items()
            if value is None or value == "NaN"
        ]

        return (
            "red"
            if duplicates > 1 or len(a) > 0 or not self.latest_date_version
            else ""
        )

    @property
    def milestones(self) -> Iterator[WPMilestone]:
        from app.models import Project, ProjectMilestone

        project: Project = self.work_package.project
        for milestone in project.milestones:
            milestone: ProjectMilestone = milestone
            for wp_ms in milestone.wp_milestones:
                yield wp_ms

    @property
    def locations(self) -> Iterator[Location]:

        project_id = self.work_package.project_id
        locations_ids = [
            loc.id
            for loc in Location.query.filter_by(deleted=False)
            if loc.level.building.project_id == project_id
        ]
        for location in Location.query.filter(Location.id.in_(locations_ids)):
            location: Location = location
            yield location

    @property
    def level_name(self) -> str:

        if self.location_id:
            location: Location = Location.query.get(self.location_id)
            return location.level.name
        else:
            return "----"

    @property
    def reasons(self) -> Iterator[Reason]:
        for reason in Reason.query.filter_by(deleted=False):
            reason: Reason = reason
            yield reason
