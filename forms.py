from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo



class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

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
    sumit = SubmitField("Create ticket")
