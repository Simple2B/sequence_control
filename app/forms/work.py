from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class WorkForm(FlaskForm):
    reference = StringField("Reference", validators=[DataRequired(), Length(2, 64)])
    old_plan_date = DateField(
        "Planned Date", validators=[DataRequired()], render_kw={"readonly": True}
    )
    new_plan_date = DateField("New Date", validators=[DataRequired()])
    submit = SubmitField("Submit")
