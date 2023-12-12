from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import RegistrationForm, LoginForm
from app.models import User, Question, db
from flask_login import login_user, logout_user, current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    # Logic for displaying the main game page
    return render_template('home.html')

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
    return render_template('admin.html')

@main.route('/leaderboard')
def leaderboard():
    # Logic to display the leaderboard
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)

# Additional routes can be added here as per your requirement
