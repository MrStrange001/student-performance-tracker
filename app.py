from flask import Flask, render_template, request, redirect, url_for, flash, Response
from database import get_db_connection, init_db
from models import StudentTracker
import os
import csv
import io
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Initialize database
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    tracker = StudentTracker(conn)
    students = tracker.get_all_students()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        
        if not name or not roll_number:
            flash('Name and roll number are required!', 'error')
            return redirect(url_for('add_student'))
        
        conn = get_db_connection()
        tracker = StudentTracker(conn)
        success, message = tracker.add_student(name, roll_number)
        conn.close()
        
        flash(message, 'success' if success else 'error')
        return redirect(url_for('index'))
    
    return render_template('add_student.html')

@app.route('/add_grades', methods=['GET', 'POST'])
def add_grades():
    conn = get_db_connection()
    tracker = StudentTracker(conn)
    
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        subject = request.form['subject']
        grade = request.form['grade']
        
        if not all([roll_number, subject, grade]):
            flash('All fields are required!', 'error')
            return redirect(url_for('add_grades'))
        
        try:
            grade = int(grade)
            if grade < 0 or grade > 100:
                flash('Grade must be between 0 and 100!', 'error')
                return redirect(url_for('add_grades'))
        except ValueError:
            flash('Grade must be a number!', 'error')
            return redirect(url_for('add_grades'))
        
        student = tracker.get_student(roll_number=roll_number)
        if not student:
            flash('Student not found!', 'error')
            return redirect(url_for('add_grades'))
        
        success, message = tracker.add_grade(student.id, subject, grade)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('index'))
    
    students = tracker.get_all_students()
    conn.close()
    return render_template('add_grades.html', students=students)

@app.route('/view_student/<roll_number>')
def view_student(roll_number):
    conn = get_db_connection()
    tracker = StudentTracker(conn)
    student = tracker.get_student(roll_number=roll_number)
    conn.close()
    
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('view_student.html', student=student)

@app.route('/reports')
def reports():
    conn = get_db_connection()
    tracker = StudentTracker(conn)
    
    # Get all subjects from the database
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT subject FROM grades ORDER BY subject')
    subjects_data = cursor.fetchall()
    subjects = [subject['subject'] for subject in subjects_data] if subjects_data else ['Math', 'Science', 'English']
    
    subject_toppers = {}
    subject_averages = {}
    
    for subject in subjects:
        topper = tracker.get_subject_topper(subject)
        subject_toppers[subject] = topper
        subject_averages[subject] = tracker.get_class_average(subject)
    
    overall_average = tracker.get_class_average()
    conn.close()
    
    return render_template('reports.html', 
                          subjects=subjects,
                          subject_toppers=subject_toppers,
                          subject_averages=subject_averages,
                          overall_average=overall_average)

# Export routes
@app.route('/export_data')
def export_data():
    conn = get_db_connection()
    tracker = StudentTracker(conn)
    students = tracker.get_all_students()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Roll Number', 'Name', 'Subject', 'Grade', 'Average'])
    
    # Write data
    for student in students:
        if student.grades:
            for subject, grade in student.grades.items():
                writer.writerow([
                    student.roll_number, 
                    student.name, 
                    subject, 
                    grade, 
                    student.calculate_average()
                ])
        else:
            writer.writerow([
                student.roll_number, 
                student.name, 
                'No grades', 
                '', 
                ''
            ])
    
    conn.close()
    
    # Return CSV file
    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=student_data.csv"}
    )

@app.route('/export_json')
def export_json():
    conn = get_db_connection()
    tracker = StudentTracker(conn)
    students = tracker.get_all_students()
    
    # Prepare data for JSON
    data = {
        "export_date": datetime.now().isoformat(),
        "students": []
    }
    
    for student in students:
        student_data = {
            "roll_number": student.roll_number,
            "name": student.name,
            "grades": student.grades,
            "average": student.calculate_average()
        }
        data["students"].append(student_data)
    
    conn.close()
    
    # Return JSON file
    return Response(
        json.dumps(data, indent=2),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=student_data.json"}
    )

@app.route('/backup')
def backup():
    conn = get_db_connection()
    tracker = StudentTracker(conn)
    students = tracker.get_all_students()
    
    # Create text backup
    backup_text = f"Student Data Backup - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    backup_text += "=" * 50 + "\n\n"
    
    for student in students:
        backup_text += f"Student: {student.name} ({student.roll_number})\n"
        if student.grades:
            for subject, grade in student.grades.items():
                backup_text += f"  {subject}: {grade}\n"
            backup_text += f"  Average: {student.calculate_average():.2f}\n"
        else:
            backup_text += "  No grades recorded\n"
        backup_text += "\n"
    
    conn.close()
    
    # Return text file
    return Response(
        backup_text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=student_backup.txt"}
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)