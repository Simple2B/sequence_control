from datetime import datetime
from app import db
from app.models.utils import ModelMixin

# TODO: connected to PM and WPM and VIEWER


class Project(db.Model, ModelMixin):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    location = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Project: {self.name} >"
