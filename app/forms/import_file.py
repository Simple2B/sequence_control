from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class ImportFileForm(FlaskForm):
    file = FileField(
        "Select File",
        validators=[FileRequired()],
    )
    submit = SubmitField("Upload")
