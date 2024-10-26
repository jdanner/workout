from flask import render_template, url_for, flash, redirect, request, jsonify
from weightlifting_tracker.app import app, db, bcrypt
from models import User, Exercise, Workout, PersonalRecord
from forms import RegistrationForm, LoginForm, WorkoutForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).limit(5).all()
    personal_records = PersonalRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', workouts=workouts, personal_records=personal_records)

@app.route("/log_workout", methods=['GET', 'POST'])
@login_required
def log_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        exercise = Exercise.query.filter_by(name=form.exercise.data).first()
        if not exercise:
            exercise = Exercise(name=form.exercise.data)
            db.session.add(exercise)
            db.session.commit()
        
        workout = Workout(user_id=current_user.id, exercise_id=exercise.id,
                          date=form.date.data,
                          sets=form.sets.data, reps=form.reps.data, weight=form.weight.data)
        db.session.add(workout)
        
        # Check for personal record
        pr = PersonalRecord.query.filter_by(user_id=current_user.id, exercise_id=exercise.id).first()
        if not pr or form.weight.data > pr.weight:
            if pr:
                pr.weight = form.weight.data
                pr.date = workout.date
            else:
                pr = PersonalRecord(user_id=current_user.id, exercise_id=exercise.id, weight=form.weight.data, date=workout.date)
                db.session.add(pr)
        
        db.session.commit()
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('log_workout.html', title='Log Workout', form=form)

@app.route("/progress/<int:exercise_id>")
@login_required
def progress(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    workouts = Workout.query.filter_by(user_id=current_user.id, exercise_id=exercise_id).order_by(Workout.date).all()
    dates = [workout.date.strftime('%Y-%m-%d') for workout in workouts]
    weights = [workout.weight for workout in workouts]
    return render_template('progress.html', title='Progress', exercise=exercise, dates=dates, weights=weights)

@app.route("/exercise_progress/<int:exercise_id>")
@login_required
def exercise_progress(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    workouts = Workout.query.filter_by(user_id=current_user.id, exercise_id=exercise_id).order_by(Workout.date).all()
    dates = [workout.date.strftime('%Y-%m-%d') for workout in workouts]
    weights = [workout.weight for workout in workouts]
    return render_template('exercise_progress.html', title='Exercise Progress', exercise=exercise, dates=dates, weights=weights)
