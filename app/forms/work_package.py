from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length

from app.models import WorkPackage, User


class WorkPackageForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 30)])
    number = StringField("Number", validators=[DataRequired(), Length(2, 30)])
    contractor_name = StringField(
        "Contractor Name", validators=[DataRequired(), Length(2, 30)]
    )
    wp_manager = SelectField("WP Manager", coerce=int, choices=[])
    submit = SubmitField("Submit")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wp_manager.choices = [
            (user.id, user.username)
            for user in User.query.filter_by(
                deleted=False, role=User.Role.wp_manager
            ).all()
        ]

    def validate_number(form, field):
        if WorkPackage.query.filter_by(number=field.data).first() is not None:
            raise ValidationError("This number is already registered.")
