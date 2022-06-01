from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class WPMilestone(db.Model, ModelMixin):

    __tablename__ = "wp_milestones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    baseline_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    project_milestone_id = db.Column(db.Integer, db.ForeignKey("project_milestones.id"))

    def __repr__(self):
        return f"<WP Milestone: {self.name} {self.description} {self.baseline_date} >"