from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from JobtransparencyNLP.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()
    ,EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired()])
    adminkey = StringField('Admin Key')
    submit = SubmitField('Register!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your Email has already been taken')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your Username has already been taken')