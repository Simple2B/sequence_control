from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class ProjectWPManager(db.Model, ModelMixin):

    __tablename__ = "project_wpmanagers"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    wp_manager_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<ProjectWPManager: id: {self.id} project: {self.project_id} wp_manager: {self.wp_manager_id} >"
