from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class PlanDate(db.Model, ModelMixin):

    __tablename__ = "plan_dates"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    work_id = db.Column(db.Integer, db.ForeignKey("works.id"))

    def __repr__(self):
        return f"<PlanDate: {self.date} {self.version} >"
