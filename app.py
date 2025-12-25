from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import *
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory user store for demo
users = {'Sam': 'Sam@2024_25'}

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = 'Username already exists'
        else:
            users[username] = password
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        db = create_db()
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        insert_patient(db, name, age, gender, diagnosis, treatment)
        db.close()
        flash('Patient added successfully!')
        return redirect(url_for('show_patients'))
    return render_template('add_patient.html')

@app.route('/show_patients')
def show_patients():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = create_db()
    patients = fetch_all_patients(db)
    db.close()
    return render_template('show_patients.html', patients=patients)

@app.route('/update_diagnosis', methods=['GET', 'POST'])
def update_diagnosis():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = create_db()
    if request.method == 'POST':
        patient_id = int(request.form['patient_id'])
        new_diagnosis = request.form['new_diagnosis']
        update_patient_diagnosis(db, patient_id, new_diagnosis)
        db.close()
        flash('Diagnosis updated successfully!')
        return redirect(url_for('show_patients'))
    patients = fetch_all_patients(db)
    db.close()
    return render_template('update_diagnosis.html', patients=patients)

@app.route('/delete_patient', methods=['GET', 'POST'])
def delete_patient_route():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = create_db()
    if request.method == 'POST':
        patient_id = int(request.form['patient_id'])
        delete_patient(db, patient_id)
        db.close()
        flash('Patient deleted successfully!')
        return redirect(url_for('show_patients'))
    patients = fetch_all_patients(db)
    db.close()
    return render_template('delete_patient.html', patients=patients)

@app.route('/analyze_age')
def analyze_age():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = create_db()
    avg_age = analyze_patient_age(db)
    db.close()
    return render_template('analyze_age.html', avg_age=avg_age)

@app.route('/analyze_diagnosis')
def analyze_diagnosis():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = create_db()
    results = analyze_diagnosis_count(db)
    db.close()
    return render_template('analyze_diagnosis.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)