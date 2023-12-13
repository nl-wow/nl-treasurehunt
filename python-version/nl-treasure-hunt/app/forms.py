from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Brukernavn/Lagnavn', validators=[DataRequired(), Length(min=2, max=20)])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passord', validators=[DataRequired()])
    confirm_password = PasswordField('Bekreft Passord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('registrer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Det brukernavnet er allerede tatt, prøv med et nytt et!')

    #def validate_email(self, email):
        #user = User.query.filter_by(email=email.data).first()
        #if user:
            #raise ValidationError('Den eposten er allerede brukt, prøv med et nytt et!')

class LoginForm(FlaskForm):
    username = StringField('Brukernavn/Lagnavn', validators=[DataRequired()])
    password = PasswordField('Passord', validators=[DataRequired()])
    remember = BooleanField('Husk meg')
    submit = SubmitField('Logg inn')

class QuestionForm(FlaskForm):
    content = StringField('Spørsmål', validators=[DataRequired()])
    answer = StringField('Svar', validators=[DataRequired()])
    points = IntegerField('Poeng', validators=[DataRequired()])
    submit = SubmitField('Send inn')

class AnswerForm(FlaskForm):
    answer = StringField('Ditt svar', validators=[DataRequired()])
    attachment = FileField('Bilde', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'pdf', "last opp et bilde!"])])
    submit = SubmitField('Send inn')

# Additional forms can be added here as per your requirement
