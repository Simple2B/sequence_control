from datetime import datetime
import enum

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import Enum, func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    class RoleType(enum.Enum):
        admin = 1
        project_manager = 2
        wp_manager = 3
        viewer = 4

    # TODO: make different models?..
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    company = db.Column(db.String(64), nullable=False)
    position = db.Column(db.String(64), nullable=True)
    wp_responsible = db.Column(db.String(64), nullable=True)
    sc_role = db.Column(Enum(RoleType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter(
            func.lower(cls.username) == func.lower(username)
        ).first()
        if user and check_password_hash(user.password, password):
            return user

    def __repr__(self):
        return f"<User: {self.username}>"


class AnonymousUser(AnonymousUserMixin):
    pass
