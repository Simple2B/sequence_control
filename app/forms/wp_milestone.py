from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, DateField, IntegerField
from wtforms.validators import DataRequired, Length

from app.models import WPMilestone


class WPMilestoneFrom(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    description = StringField("Description", validators=[DataRequired(), Length(2, 30)])
    baseline_date = DateField("Baseline", validators=[DataRequired()])
    project_milestone_id = IntegerField(
        "Project Milestone", validators=[DataRequired()]
    )

    submit = SubmitField("Submit")

    def validate_name(form, field):
        if WPMilestone.query.filter_by(name=field.data).first() is not None:
            raise ValidationError("This name is already registered.")
