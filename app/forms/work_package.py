from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models import WorkPackage, Project


class WorkPackageForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    number = StringField("Number", validators=[DataRequired(), Length(2, 30)])
    contractor_name = StringField(
        "Contractor Name", validators=[DataRequired(), Length(2, 30)]
    )

    submit = SubmitField("Submit")

    def validate_number(form, field):
        if WorkPackage.query.filter_by(number=field.data).first() is not None:
            raise ValidationError("This number is already registered.")

    def validate_project_id(form, field):
        if Project.query.filter_by(id=field.data).first() is None:
            raise ValidationError("No such project id registered.")
