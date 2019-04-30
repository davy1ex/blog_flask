from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app.models import User


class RegForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password")
    password2 = PasswordField("Repeate password", validators=[EqualTo("password")])
    submit = SubmitField("Registration")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        
        if user is not None:
            raise ValidationError("Enter different email.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        
        if user is not None:
            raise ValidationError("Enter different username.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Sign in")


class ProfileSettingsForm(FlaskForm):
    username = StringField("Username")
    about = TextAreaField("About...")
    submit = SubmitField("Ok")


class TextEditorForm(FlaskForm):
    title = StringField("Title")
    text = TextAreaField("AddText")
    submit = SubmitField("Ok")


class AddCommentForm(FlaskForm):
    author = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    body = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")
