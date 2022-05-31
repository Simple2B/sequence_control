from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class Milestone(db.Model, ModelMixin):

    __tablename__ = "milestones"

    id = db.Column(db.Integer, primary_key=True)
    milestone = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    baseline_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Location: {self.building} {self.level} {self.room} >"
