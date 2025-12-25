import mysql.connector as sql
from datetime import datetime

def create_db():
    db = sql.connect(
        host='localhost',
        database='MedicalDB',
        user='root',
        password='tiger'
    )
    return db

def insert_patient(db, name, age, gender, diagnosis, treatment):
    cursor = db.cursor()
    sql_query = """
    INSERT INTO Patients (name, age, gender, diagnosis, treatment, admission_date)
    VALUES (%s, %s, %s, %s, %s, %s)"""
    admission_date = datetime.now().date()
    values = (name, age, gender, diagnosis, treatment, admission_date)
    cursor.execute(sql_query, values)
    db.commit()

def fetch_all_patients(db):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Patients")
    return cursor.fetchall()

def update_patient_diagnosis(db, patient_id, new_diagnosis):
    cursor = db.cursor()
    sql_query = "UPDATE Patients SET diagnosis = %s WHERE patient_id = %s"
    values = (new_diagnosis, patient_id)
    cursor.execute(sql_query, values)
    db.commit()

def delete_patient(db, patient_id):
    cursor = db.cursor()
    sql_query = "DELETE FROM Patients WHERE patient_id = %s"
    cursor.execute(sql_query, (patient_id,))
    db.commit()

def analyze_patient_age(db):
    cursor = db.cursor()
    cursor.execute("SELECT AVG(age) FROM Patients")
    avg_age = cursor.fetchone()[0]
    return avg_age

def analyze_diagnosis_count(db):
    cursor = db.cursor()
    cursor.execute("SELECT diagnosis, COUNT(*) FROM Patients GROUP BY diagnosis")
    return cursor.fetchall()