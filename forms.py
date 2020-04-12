from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class TextForm(FlaskForm):
    text = TextAreaField('Text')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    mail = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    gdpr = BooleanField('Agree with personal data processing.', validators=[DataRequired()])
    mark = BooleanField('Agree to Receive notifications and news.')