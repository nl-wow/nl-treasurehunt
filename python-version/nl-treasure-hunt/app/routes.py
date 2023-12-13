from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, send_from_directory, current_app
from werkzeug.security import check_password_hash, generate_password_hash, safe_join
from app.forms import RegistrationForm, LoginForm, QuestionForm, AnswerForm
from app.models import User, Question, db, UserAnswer
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os
import datetime

main = Blueprint('main', __name__)

@main.route('/', defaults={'question_id': None},  methods=['GET', 'POST'])
@main.route('/<int:question_id>',methods=['GET', 'POST'])
@login_required
def home(question_id):
    form = AnswerForm()
    allow_next = False

    if question_id is None:
        question = Question.query.order_by(Question.id).first()
    else:
        question = Question.query.get_or_404(question_id)

    user_answer = UserAnswer.query.filter_by(user_id=current_user.id, question_id=question.id).first()

    if form.validate_on_submit():
        correct_answer = question.answer.lower().strip()  # Assuming the answer field is a string and lowercase
        user_submitted_answer = form.answer.data.lower().strip()  # Sanitize input

        if user_answer:
            # Update existing answer
            user_answer.answer = user_submitted_answer
            user_answer.is_correct = (user_submitted_answer == correct_answer)
        else:
            # Create new answer
            user_answer = UserAnswer(
                user_id=current_user.id,
                question_id=question.id,
                answer=user_submitted_answer,
                is_correct=(user_submitted_answer == correct_answer),
                attachment_filename=None  # Handle attachments as needed
            )
            db.session.add(user_answer)

        if user_answer.is_correct:
            # Only add points if this is the first correct submission for this question
            if not user_answer.points_awarded:
                current_user.points += question.points  # Add points from the question
                user_answer.points_awarded = True  # Mark that points were awarded for this question
            flash('Rett svar! Trykk "neste" for å gå videre', 'success')
            allow_next = True
        else:
            flash('Feil svar! Prøv igjen. Husk å sjekke stavelse!', 'danger')

        db.session.commit()

    # Logic for fetching prev and next questions remains the same
    prev_question = Question.query.filter(Question.id < question.id).order_by(Question.id.desc()).first()
    next_question = Question.query.filter(Question.id > question.id).order_by(Question.id).first() if allow_next else None
    
    return render_template('home.html', question=question, form=form, user_answer=user_answer,
                           prev_question_id=prev_question.id if prev_question else None,
                           next_question_id=next_question.id if next_question else None)


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    # Optional: Add authentication/authorization logic here
    if not current_user.is_authenticated:
        abort(403)
    
    # Ensure the filename is safe
    safe_filename = secure_filename(filename)  # Use 'secure_filename' to sanitize the filename
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)

    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], safe_filename)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('spiller/lag opprettet! du kan nå logge inn.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Innlogging feilet. vennligst sjekk brukernavn/lagnavn og passord', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    # Admin page logic here
    form = QuestionForm()
    if form.validate_on_submit():
        new_question = Question(content=form.content.data, 
                                answer=form.answer.data, 
                                points=form.points.data)
        db.session.add(new_question)
        db.session.commit()
        flash('nytt spørsmål opprettet!', 'success')
        return redirect(url_for('main.admin'))
    submissions = (db.session.query(UserAnswer, User, Question)
                   .join(User, User.id == UserAnswer.user_id)
                   .join(Question, Question.id == UserAnswer.question_id)
                   .order_by(Question.id)
                   .all())
    
    return render_template('admin.html', form=form, submissions=submissions)


@main.route('/leaderboard')
def leaderboard():
    # Logic to display the leaderboard
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)

# Additional routes can be added here as per your requirement
