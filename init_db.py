from app import app, db
from models import User, Exercise, Workout, PersonalRecord

with app.app_context():
    db.create_all()
    print("Database initialized.")

    # Add sample exercises
    sample_exercises = ["Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row"]
    for exercise_name in sample_exercises:
        if not Exercise.query.filter_by(name=exercise_name).first():
            new_exercise = Exercise(name=exercise_name)
            db.session.add(new_exercise)
    
    db.session.commit()
    print("Sample exercises added.")
