from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length
from app.models import Reason


class WorkReforecastForm(FlaskForm):

    deliverable = StringField(
        "Deliverable",
        validators=[DataRequired(), Length(2, 64)],
        render_kw={"readonly": True},
    )
    reference = StringField(
        "Reference",
        validators=[DataRequired(), Length(2, 64)],
        render_kw={"readonly": True},
    )
    responsible = SelectField(
        "Responsible", validators=[DataRequired()], coerce=str, choices=[]
    )
    reason = SelectField("Reason", validators=[DataRequired()], coerce=str, choices=[])
    note = TextAreaField("Note", validators=[Length(0, 256)])
    old_plan_date = DateField(
        "Planned Date", validators=[DataRequired()], render_kw={"readonly": True}
    )
    new_plan_date = DateField("New Date", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.reason.choices = [
            (reason.name, reason.name)
            for reason in Reason.query.filter_by(deleted=False).all()
        ]
