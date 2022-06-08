from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length
from app.models import Level, Building


class LocationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    description = StringField("Description", validators=[DataRequired(), Length(2, 30)])
    level_id = SelectField("Level", validators=[DataRequired()], coerce=int, choices=[])

    submit = SubmitField("Submit")

    def validate_level_id(form, field):
        if Level.query.filter_by(id=field.data).first() is None:
            raise ValidationError("No such level id registered.")


class LevelForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    building_id = SelectField("Building", coerce=int, choices=[])
    submit = SubmitField("Submit")

    def validate_building_id(form, field):
        if Building.query.filter_by(id=field.data).first() is None:
            raise ValidationError("No such building id registered.")


class BuildingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])

    submit = SubmitField("Submit")
