from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password")
    password2 = PasswordField("Repeate password", validators=[EqualTo("password")])
    submit = SubmitField("Registration")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Sign in")
