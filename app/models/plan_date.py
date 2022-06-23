from datetime import datetime
from sqlalchemy.orm import relationship
from app import db
from app.models.utils import ModelMixin

NOTE_LEN = 6


class PlanDate(db.Model, ModelMixin):

    __tablename__ = "plan_dates"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    note = db.Column(db.String(256), nullable=True)
    reason = db.Column(db.String(256), nullable=True)
    responsible = db.Column(db.String(128), nullable=True)

    work_id = db.Column(db.Integer, db.ForeignKey("works.id"))
    work = relationship("Work", viewonly=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", viewonly=True)

    def __repr__(self):
        return f"<{self.id} {self.date} {self.version} >"

    @property
    def short_note(self) -> str:
        return (
            (self.note[:6] + " ...")
            if self.note and len(self.note) > NOTE_LEN
            else self.note
        )
