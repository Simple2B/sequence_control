from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class Location(db.Model, ModelMixin):

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(64), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    room_description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Location: {self.building} {self.level} {self.room} >"
