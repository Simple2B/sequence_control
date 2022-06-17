from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)


class SearchForm(FlaskForm):
    search_field = StringField("search")
    search_button = SubmitField("Submit")
