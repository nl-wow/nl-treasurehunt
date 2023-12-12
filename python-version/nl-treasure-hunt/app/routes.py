from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, send_from_directory, current_app
from werkzeug.security import check_password_hash, generate_password_hash, safe_join
from app.forms import RegistrationForm, LoginForm, QuestionForm, AnswerForm
from app.models import User, Question, db, UserAnswer
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.route('/', defaults={'question_id': None})
@main.route('/<int:question_id>')
@login_required
def home(question_id=None):
    # Logic for displaying the main game page
    if question_id is None:
        question = Question.query.first()
    else:
        question = Question.query.get_or_404(question_id)

    prev_question = Question.query.filter(Question.id < question.id).order_by(Question.id.desc()).first()
    next_question = Question.query.filter(Question.id > question.id).order_by(Question.id).first()

    form = AnswerForm()


    if form.validate_on_submit():
        # Logic to save user's answer
        user_answer = UserAnswer(user_id=current_user.id, 
                                 question_id=question.id, 
                                 answer=form.answer.data)
        if form.attachment.data:
            filename = secure_filename(form.attachment.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.attachment.data.save(file_path)
            user_answer.attachment_filename = filename

        db.session.add(user_answer)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
    return render_template('home.html', question=question, form=form,
                            prev_question_id=prev_question.id if prev_question else None,
                            next_question_id=next_question.id if next_question else None)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    # Optional: Add authentication/authorization logic here
    if not current_user.is_authenticated:
        abort(403)
    # Ensure the filename is safe
    filename = safe_join(current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(filename):
        abort(404)

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

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
        flash('Your account has been created! You are now able to log in', 'success')
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
        flash('New question created!', 'success')
        return redirect(url_for('main.admin'))
    return render_template('admin.html', form=form)

@main.route('/leaderboard')
def leaderboard():
    # Logic to display the leaderboard
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)

# Additional routes can be added here as per your requirement
