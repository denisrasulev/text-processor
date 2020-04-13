from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class TextForm(FlaskForm):
    m_inp = u'Max length is 1000 symbols!'
    input = TextAreaField(u'Source:',
                          validators=[DataRequired(), Length(max=1000, message=m_inp)],
                          render_kw={'class': 'form-control', 'rows': 5})
    outp = TextAreaField(u'Output:',
                         render_kw={'class': 'form-control', 'rows': 5, 'readonly': True})
    subm = SubmitField('Submit')
    down = SubmitField('Download')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    mail = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    gdpr = BooleanField('Agree with personal data processing.', validators=[DataRequired()])
    mark = BooleanField('Agree to Receive notifications and news.', validators=[Optional()])
    submit = SubmitField('Submit')
