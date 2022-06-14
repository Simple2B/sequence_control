from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Optional
from app.models import Work


class WorkAddForm(FlaskForm):

    ppc_type = StringField(
        "PPC type",
        validators=[DataRequired(), Length(2, 16)],
    )
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


class WorkEditForm(WorkAddForm):
    reference = StringField(
        "Reference",
        validators=[DataRequired(), Length(2, 64)],
        render_kw={"readonly": True},
    )
    plan_date = DateField(
        "Planned Date",
        validators=[Optional()],
        render_kw={"readonly": True},
    )
    new_plan_date = DateField("New Date")
    submit = SubmitField("Submit")

    def validate_reference(form, field):
        if Work.query.filter_by(reference=field.data).first() is None:
            raise ValidationError("This reference is not registered.")


class WorkDeleteForm(FlaskForm):

    ppc_type = StringField(
        "PPC type",
        validators=[DataRequired(), Length(2, 16)],
        render_kw={"readonly": True},
    )
    type = StringField(
        "Sub-type",
        validators=[DataRequired(), Length(2, 16)],
        render_kw={"readonly": True},
    )
    deliverable = StringField(
        "Deliverable",
        validators=[DataRequired(), Length(2, 64)],
        render_kw={"readonly": True},
    )
    reference = StringField(
        "Reference",
        validators=[DataRequired(), Length(2, 64)],
        render_kw={"readonly": True},
    )
    plan_date = DateField(
        "Planned Date", validators=[DataRequired()], render_kw={"readonly": True}
    )
