from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, DateField, SelectField
from wtforms.validators import DataRequired, Length
from flask import session
from app.models import WPMilestone, ProjectMilestone, WorkPackage


class WPMilestoneFrom(FlaskForm):

    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    description = StringField("Description", validators=[DataRequired(), Length(2, 30)])
    baseline_date = DateField("Baseline", validators=[DataRequired()])
    project_milestone_id = SelectField(
        "Project Milestone", validators=[DataRequired()], coerce=int, choices=[]
    )

    submit = SubmitField("Submit")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        wp_id = int(session.get("wp_id"))
        if wp_id:
            wp: WorkPackage = WorkPackage.query.get(wp_id)
        self.project_milestone_id.choices = [
            (milestone.id, milestone.name)
            for milestone in ProjectMilestone.query.filter_by(
                deleted=False, project_id=wp.project_id
            ).all()
        ]

    def validate_name(form, field):
        if WPMilestone.query.filter_by(name=field.data).first() is not None:
            raise ValidationError("This name is already registered.")


class MilestoneFrom(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    description = StringField("Description", validators=[DataRequired(), Length(2, 30)])
    baseline_date = DateField("Baseline", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate_name(form, field):
        if ProjectMilestone.query.filter_by(name=field.data).first() is not None:
            raise ValidationError("This name is already registered.")
