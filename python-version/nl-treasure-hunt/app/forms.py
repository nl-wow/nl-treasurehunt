from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Det brukernavnet er allerede tatt, prøv med et nytt et!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Den eposten er allerede brukt, prøv med et nytt et!')

class LoginForm(FlaskForm):
    email = StringField('Epost', validators=[DataRequired(), Email()])
    password = PasswordField('Passord', validators=[DataRequired()])
    remember = BooleanField('Husk meg')
    submit = SubmitField('Logg inn')

class QuestionForm(FlaskForm):
    content = TextAreaField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    points = IntegerField('Points', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Additional forms can be added here as per your requirement
