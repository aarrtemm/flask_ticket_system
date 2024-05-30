from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, ValidationError
from wtforms.validators import DataRequired, EqualTo

from database.models import User


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class TicketForm(FlaskForm):
    note = TextAreaField("Note", validators=[DataRequired()])
    status = SelectField(
        "Status", 
        choices=[("Pending", "Pending"), ("Closed", "Closed"), ("In review", "In review")],
        default="Pending",
        validators=[DataRequired()]
        )
    submit = SubmitField("Create ticket")
