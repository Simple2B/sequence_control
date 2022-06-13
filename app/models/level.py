from datetime import datetime
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin


class Level(db.Model, ModelMixin):

    __tablename__ = "levels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))
    building = relationship("Building", viewonly=True)

    def __repr__(self):
        return f"<{self.id} {self.name} {self.building_id}>"
