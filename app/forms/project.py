from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, DateField
from wtforms.validators import DataRequired, Length

from app.models import Project


class ProjectForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    number = StringField(
        "Number", validators=[DataRequired(), Length(2, 30)]
    )  # unique=True
    location = StringField("Location", validators=[DataRequired(), Length(2, 30)])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate_number(form, field):
        if Project.query.filter_by(number=field.data).first() is not None:
            raise ValidationError("This number is already registered.")

    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            raise ValidationError("End Date sooner than Start date")