from datetime import datetime
import enum
from sqlalchemy import Enum
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

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(Enum(Type), nullable=False)
    deliverable = db.Column(db.String(255))
    reference = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    wp_id = db.Column(db.Integer, db.ForeignKey("work_packages.id"))

    def __repr__(self):
        return f"<Work: {self.type} {self.deliverable} >"