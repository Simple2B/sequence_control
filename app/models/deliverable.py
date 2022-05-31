from datetime import datetime
import enum
from sqlalchemy import Enum
from app import db
from app.models.utils import ModelMixin

# TODO: connect users and this (need a project model?)

# TODO: connect with other versions of same model


class Deliverable(db.Model, ModelMixin):

    __tablename__ = "deliverables"

    class TypeColor(enum.Enum):
        yellow = "yellow"
        red = "red"
        blue = "blue"
        viewer = "green"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    deliverable = db.Column(db.String(255))
    # TODO: must be like this: unique=True, nullable=False, but we have sheets with empty fields..
    reference = db.Column(db.String(64))
    planned_date = created_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # version = db.Column(db.Integer)
    color = db.Column(Enum(TypeColor), nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Deliverable: {self.type} {self.deliverable} {self.planned_date}>"
