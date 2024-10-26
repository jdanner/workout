let workouts = JSON.parse(localStorage.getItem('workouts')) || [];
let chart = null;

function addWorkout(date, exercise, weight, reps, sets) {
    workouts.push({ date, exercise, weight: Number(weight), reps: Number(reps), sets: Number(sets) });
    localStorage.setItem('workouts', JSON.stringify(workouts));
    updateDashboard();
}

function deleteWorkout(index) {
    workouts.splice(index, 1);
    localStorage.setItem('workouts', JSON.stringify(workouts));
    updateDashboard();
}

function displayWorkouts() {
    const workoutList = document.getElementById('workout-list');
    workoutList.innerHTML = '';
    workouts.forEach((workout, index) => {
        const workoutElement = document.createElement('div');
        workoutElement.innerHTML = `
            <p>${workout.date} - ${workout.exercise}: ${workout.weight}lbs, ${workout.reps} reps, ${workout.sets} sets
            <button onclick="deleteWorkout(${index})">Delete</button></p>
        `;
        workoutList.appendChild(workoutElement);
    });
}

function updateSummary() {
    document.getElementById('total-workouts').textContent = workouts.length;
    const exerciseCounts = workouts.reduce((acc, workout) => {
        acc[workout.exercise] = (acc[workout.exercise] || 0) + 1;
        return acc;
    }, {});
    const mostCommonExercise = Object.entries(exerciseCounts).reduce((a, b) => a[1] > b[1] ? a : b)[0];
    document.getElementById('most-common-exercise').textContent = mostCommonExercise || 'None';
}

function updateExerciseSelect() {
    const exerciseSelect = document.getElementById('exercise-select');
    const exercises = [...new Set(workouts.map(w => w.exercise))];
    exerciseSelect.innerHTML = '<option value="">Select an exercise</option>';
    exercises.forEach(exercise => {
        const option = document.createElement('option');
        option.value = exercise;
        option.textContent = exercise;
        exerciseSelect.appendChild(option);
    });
}

function updateGraph() {
    const exercise = document.getElementById('exercise-select').value;
    if (!exercise) return;

    const exerciseData = workouts
        .filter(w => w.exercise === exercise)
        .sort((a, b) => new Date(a.date) - new Date(b.date));

    const labels = exerciseData.map(w => w.date);
    const weights = exerciseData.map(w => w.weight);

    if (chart) chart.destroy();

    const ctx = document.getElementById('progress-chart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${exercise} Progress`,
                data: weights,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function updateDashboard() {
    displayWorkouts();
    updateSummary();
    updateExerciseSelect();
    updateGraph();
}

document.getElementById('workout-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const date = document.getElementById('date').value;
    const exercise = document.getElementById('exercise').value;
    const weight = document.getElementById('weight').value;
    const reps = document.getElementById('reps').value;
    const sets = document.getElementById('sets').value;
    addWorkout(date, exercise, weight, reps, sets);
    this.reset();
});

document.getElementById('exercise-select').addEventListener('change', updateGraph);

updateDashboard();
