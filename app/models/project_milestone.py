from datetime import datetime
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin


class ProjectMilestone(db.Model, ModelMixin):

    __tablename__ = "project_milestones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    baseline_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    wp_milestones = relationship("WPMilestone", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: {self.name} project_id{self.project_id}>"
