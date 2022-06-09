from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class Project(db.Model, ModelMixin):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    number = db.Column(db.String(64), unique=True, nullable=False)
    location = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<{self.id} {self.name} {self.number} {self.manager_id}>"
