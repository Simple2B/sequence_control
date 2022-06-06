from app import db
from app.models.utils import ModelMixin


class Reason(db.Model, ModelMixin):

    __tablename__ = "reasons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Reason: {self.name}>"
