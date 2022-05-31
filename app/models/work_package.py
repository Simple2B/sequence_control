from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class WorkPackage(db.Model, ModelMixin):

    __tablename__ = "work_packages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    contractor_name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<WorkPackage: {self.name} {self.number} {self.contractor_name} >"
