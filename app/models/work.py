from datetime import datetime
import enum
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin


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
