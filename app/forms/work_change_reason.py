from flask_wtf import FlaskForm
from wtforms import IntegerField


class WorkChangeReasonForm(FlaskForm):
    work_id = IntegerField()
    reason_id = IntegerField()
