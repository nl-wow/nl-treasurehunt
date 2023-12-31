from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Question {self.content[:50]}>'

class UserAnswer(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    answer = db.Column(db.String(500), nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    attachment_filename = db.Column(db.String(128))
    is_correct = db.Column(db.Boolean)
    points_awarded = db.Column(db.Boolean, default=False, nullable=False)



# Additional models can be added here as per your requirement
