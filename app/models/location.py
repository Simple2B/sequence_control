from datetime import datetime
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin


class Location(db.Model, ModelMixin):

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"))

    level = relationship("Level", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: {self.name} level_id {self.level_id}>"
