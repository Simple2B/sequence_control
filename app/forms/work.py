from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, ValidationError
from wtforms.validators import DataRequired, Length
from app.models import Work


class WorkEditDateForm(FlaskForm):
    reference = StringField("Reference", validators=[DataRequired(), Length(2, 64)])
    old_plan_date = DateField(
        "Planned Date", validators=[DataRequired()], render_kw={"readonly": True}
    )
    new_plan_date = DateField("New Date", validators=[DataRequired()])
    submit = SubmitField("Submit")


class WorkAddForm(FlaskForm):
    ppc_type = StringField("PPC type", validators=[DataRequired(), Length(2, 16)])
    type = StringField("Sub-type", validators=[DataRequired(), Length(2, 16)])
    deliverable = StringField("Deliverable", validators=[DataRequired(), Length(2, 64)])
    reference = StringField("Reference", validators=[DataRequired(), Length(2, 64)])
    plan_date = DateField("Planned Date", validators=[DataRequired()])

    submit = SubmitField("Submit")

    def validate_reference(form, field):
        if Work.query.filter_by(reference=field.data).first() is not None:
            raise ValidationError("This reference is already registered.")

    def validate_ppc_type(form, field):

        if field.data.lower() not in Work.PpcType._value2member_map_:
            raise ValidationError("No such PPC Type registered.")

    def validate_type(form, field):
        try:
            Work.Type[field.data.upper()]
        except KeyError:
            raise ValidationError("No such PPC Sub-type registered.")
