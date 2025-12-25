import mysql.connector as sql  
from datetime import datetime  
import matplotlib.pyplot as plt  

# Login variables  
n='Sam'  
p="Sam@2024_25"  
# Function to connect to the MySQL database  
def create_db():  
    db = sql.connect(  
        host='localhost',  
        database='MedicalDB',  
        user='root',  
        password='tiger'  
    )  
    if db.is_connected():  
        print("Connected to MySQL database")  
        return db  

# Function to get user login credentials  
def user():  
    name = input('Enter your name: ')  
    password = input('Enter your password: ')  
    return (name, password)  

# Function to insert a new patient  
def insert_patient(db, name, age, gender, diagnosis, treatment):  
    cursor = db.cursor()  
    sql_query = """  
    INSERT INTO Patients (name, age, gender, diagnosis, treatment, admission_date)  
    VALUES (%s, %s, %s, %s, %s, %s)"""  
    admission_date = datetime.now().date()  
    values = (name, age, gender, diagnosis, treatment, admission_date)  
    cursor.execute(sql_query, values)  
    db.commit()  
    print(f"Patient {name} added successfully.")  

# Function to fetch all patients  
def fetch_all_patients(db):  
    cursor = db.cursor()  
    cursor.execute("SELECT * FROM Patients")  
    rows = cursor.fetchall()  
    for row in rows:  
        print(row)  

# Function to update diagnosis for a specific patient  
def update_patient_diagnosis(db, patient_id, new_diagnosis):  
    cursor = db.cursor()  
    sql_query = "UPDATE Patients SET diagnosis = %s WHERE patient_id = %s"  
    values = (new_diagnosis, patient_id)  
    cursor.execute(sql_query, values)  
    db.commit()  
    print(f"Patient ID {patient_id}'s diagnosis updated successfully.")  

# Function to delete patient record  
def delete_patient(db, patient_id):  
    cursor = db.cursor()  
    sql_query = "DELETE FROM Patients WHERE patient_id = %s"  
    cursor.execute(sql_query, (patient_id,))  
    db.commit()  
    print(f"Patient ID {patient_id} deleted successfully.")  

# Function to analyze and print average age  
def analyze_patient_age(db):  
    cursor = db.cursor()  
    cursor.execute("SELECT AVG(age) FROM Patients")  
    avg_age = cursor.fetchone()[0]  
    print(f"The average age of patients is {avg_age:.2f} years.")  

# Function to analyze diagnosis count  
def analyze_diagnosis_count(db):  
    cursor = db.cursor()  
    cursor.execute("SELECT diagnosis, COUNT(*) FROM Patients GROUP BY diagnosis")  
    results = cursor.fetchall()  
    print("Diagnosis count:")  
    for diagnosis, count in results:  
        print(f"{diagnosis}: {count} patients")  

# Function to visualize average age by diagnosis  
def visualize_age_by_diagnosis(db):  
    cursor = db.cursor()  
    cursor.execute("SELECT diagnosis, AVG(age) FROM Patients GROUP BY diagnosis")  
    results = cursor.fetchall()  
    
    diagnoses = [row[0] for row in results]  
    avg_ages = [row[1] for row in results]  

    plt.figure(figsize=(10, 6))  
    plt.bar(diagnoses, avg_ages, color='skyblue')  
    plt.title('Average Age of Patients by Diagnosis')  
    plt.xlabel('Diagnosis')  
    plt.ylabel('Average Age')  
    plt.xticks(rotation=45)  
    plt.tight_layout()  
    plt.show()  

# Function to visualize age distribution by gender  
def visualize_age_by_gender(db):  
    cursor = db.cursor()  
    cursor.execute("SELECT gender, age FROM Patients")  
    results = cursor.fetchall()  

    # Separate ages by gender  
    ages_by_gender = {}  
    for row in results:  
        gender = row[0]  
        age = row[1]  
        if gender not in ages_by_gender:  
            ages_by_gender[gender] = []  
        ages_by_gender[gender].append(age)  

    # Create histogram  
    plt.figure(figsize=(10, 6))  
    for gender, ages in ages_by_gender.items():  
        plt.hist(ages, bins=10, alpha=0.5, label=gender)  

    plt.title('Age Distribution of Patients by Gender')  
    plt.xlabel('Age')  
    plt.ylabel('Frequency')  
    plt.legend(title='Gender')  
    plt.xticks(rotation=45)  
    plt.tight_layout()  
    plt.show()
    
# Function to visualize number of patients by treatment  
def visualize_patients_by_treatment(db):  
    cursor = db.cursor()  
    cursor.execute("SELECT treatment, COUNT(*) FROM Patients GROUP BY treatment")  
    results = cursor.fetchall()  

    treatments = [row[0] for row in results]  
    counts = [row[1] for row in results]  

    plt.figure(figsize=(10, 6))  
    plt.pie(counts, labels=treatments, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightskyblue'])  
    plt.title('Number of Patients by Treatment')  
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.  
    plt.tight_layout()  
    plt.show()

# Function to close MySQL db  
def close_db(db):  
    if db.is_connected():  
        db.close()  
        print("MySQL db is closed")  

# Main function to run the system  
def main():  
    name, password = user()  
    if n == name and p == password:  
        print('Correct\n', 'Welcome Sir')  
        while True:  
            db = create_db()  
            choice = int(input("""  
            MEDICAL DATA MANAGEMENT AND ANALYSIS\n  
            1. Add New Patient\n  
            2. Show all records\n  
            3. Update diagnosis\n  
            4. Data Analysis on age\n  
            5. Data Analysis on diagnosis\n  
            6. Delete record of a patient\n  
            7. Visualize Average Age by Diagnosis\n  
            8. Visualize Average Age by Gender\n  
            9. Visualize Number of Patients by Treatment\n  
            10. Exit\n  
            Enter your choice: """))  
            
            if choice == 1:  
                name = input('Enter your name: ')  
                age = int(input('Enter your age: '))  
                gender = input('Enter your gender: ')  
                problem = input('Enter your problem: ')  
                treatment = input('Enter the treatment which doctor starts: ')  
                insert_patient(db, name, age, gender, problem, treatment)  
                print("\nAll Patient Data:")  
        
            elif choice == 2:  
                fetch_all_patients(db)  
                print("\nData Analysis:")  

            elif choice == 3:  
                new_diagnosis = input("Enter the new diagnosis: ")  
                patient_id = int(input('Enter patient ID: '))  
                update_patient_diagnosis(db, patient_id, new_diagnosis)   
        
            elif choice == 4:  
                print("\nData Analysis:")  
                analyze_patient_age(db)  
    
            elif choice == 5:  
                print("\nData Analysis:")  
                analyze_diagnosis_count(db)  
        
            elif choice == 6:  
                print("\nAll Patient Data:")  
                fetch_all_patients(db)  
                patient_id = int(input('Enter patient ID: '))  
                delete_patient(db, patient_id)  
        
            elif choice == 7:  
                visualize_age_by_diagnosis(db)  

            elif choice == 8:  
                visualize_age_by_gender(db)  

            elif choice == 9:  
                visualize_patients_by_treatment(db)  

            else:  
                end = input('Do you want to exit (y, n): ')  
                if end == 'y':  
                    close_db(db)  
                    break  
        else:  
            print('Continue.....')  

if __name__ == "__main__":  
    main()