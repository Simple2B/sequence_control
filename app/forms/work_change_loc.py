from flask_wtf import FlaskForm
from wtforms import IntegerField


class WorkChangeLocationForm(FlaskForm):
    work_id = IntegerField()
    loc_id = IntegerField()
