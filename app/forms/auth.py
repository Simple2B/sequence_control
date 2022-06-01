from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User


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
    ROLES = [
        (User.RoleType.project_manager.value, User.RoleType.project_manager.name),
        (User.RoleType.wp_manager.value, User.RoleType.wp_manager.name),
        (User.RoleType.viewer.value, User.RoleType.viewer),
    ]

    position = StringField("Position", validators=[DataRequired(), Length(2, 30)])
    # sc_role = SelectField(
    #     "Role", coerce=int, validators=[InputRequired()], choices=ROLES
    # )


class WPMRegistrationForm(PmRegistrationForm):
    wp_responsible = StringField(
        "WP Responsible for", validators=[DataRequired(), Length(2, 30)]
    )
