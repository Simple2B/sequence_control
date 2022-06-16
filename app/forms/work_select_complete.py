from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField


class WorkSelectCompleteForm(FlaskForm):
    work_id = IntegerField()
    complete = StringField()
