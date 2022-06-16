from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class WorkEditNoteForm(FlaskForm):
    reference = StringField("Reference", validators=[DataRequired(), Length(2, 64)])
    note = TextAreaField("Note", validators=[Length(0, 256)])
    submit = SubmitField("Submit")
