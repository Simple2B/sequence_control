from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length
from app.models import Level, Building, Project


class LocationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    description = StringField("Description", validators=[DataRequired(), Length(2, 30)])
    level_id = IntegerField("Level", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate_level_id(form, field):
        if Level.query.filter_by(id=field.data).first() is None:
            raise ValidationError("No such level id registered.")


class LevelForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    building_id = IntegerField("Building", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate_building_id(form, field):
        if Building.query.filter_by(id=field.data).first() is None:
            raise ValidationError("No such building id registered.")


class BuildingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    project_id = IntegerField("Project", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate_project_id(form, field):
        if Project.query.filter_by(id=field.data).first() is None:
            raise ValidationError("No such project id registered.")
