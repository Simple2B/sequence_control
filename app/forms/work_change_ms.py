from flask_wtf import FlaskForm
from wtforms import IntegerField


class WorkChangeMilestoneForm(FlaskForm):
    work_id = IntegerField()
    ms_id = IntegerField()
