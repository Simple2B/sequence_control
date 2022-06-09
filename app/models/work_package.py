from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class WorkPackage(db.Model, ModelMixin):

    __tablename__ = "work_packages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    number = db.Column(db.String(64), unique=True, nullable=False)
    contractor_name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return (
            f"<{self.id} #{self.number} pr_id{self.project_id} mng_id{self.manager_id}>"
        )
