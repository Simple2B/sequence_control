from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class LocationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    description = StringField("Description", validators=[DataRequired(), Length(2, 30)])
    level_id = IntegerField("Level", validators=[DataRequired()])

    submit = SubmitField("Submit")


class LevelForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    building_id = IntegerField("Building", validators=[DataRequired()])

    submit = SubmitField("Submit")


class BuildingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    project_id = IntegerField("Project", validators=[DataRequired()])

    submit = SubmitField("Submit")
