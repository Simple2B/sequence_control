from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class Building(db.Model, ModelMixin):

    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def __repr__(self):
        return f"<{self.id}: {self.name} project_id:{self.project_id}>"
