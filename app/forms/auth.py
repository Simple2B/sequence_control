from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User, Project


class LoginForm(FlaskForm):
    user_id = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 30)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    company_name = StringField("Company", validators=[DataRequired(), Length(2, 30)])

    submit = SubmitField("Register")

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("This email is already registered.")


class PmRegistrationForm(RegistrationForm):

    position = StringField("Position", validators=[DataRequired(), Length(2, 30)])


class WPMRegistrationForm(PmRegistrationForm):
    wp_responsible = SelectField("WP Responsible for", coerce=int, choices=[])

    submit = SubmitField("Submit")


class SelectViewerForm(FlaskForm):
    viewer = SelectField("Viewer", coerce=int, choices=[])
    submit = SubmitField("Submit")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewer.choices = [
            (user.id, user.username)
            for user in User.query.filter_by(deleted=False, role=User.Role.viewer).all()
        ]


class AdminSelectViewerForm(SelectViewerForm):
    project = SelectField("Project", coerce=int, choices=[])

    submit = SubmitField("Submit")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project.choices = [
            (project.id, project.name)
            for project in Project.query.filter_by(deleted=False).all()
        ]
