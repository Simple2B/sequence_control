from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# from app.models import Reason


class ReasonForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 64)])
    submit = SubmitField("Submit")

    # def validate_name(form, field):
    #     if Reason.query.filter_by(name=field.data).first() is not None:
    #         raise ValidationError("This name is already registered.")
