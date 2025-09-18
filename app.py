from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory storage
students = []

# Structure: {roll_number: {'mst1': {subject: marks}, 'mst2': {...}, 'final': {...}}}
marks_data = {}

# Utility functions
def calculate_student_average(roll_number):
    student_marks = marks_data.get(roll_number, {})
    total = 0
    count = 0
    for exam in ['mst1', 'mst2', 'final']:
        for subject, mark in student_marks.get(exam, {}).items():
            total += mark
            count += 1
    return total / count if count > 0 else 0

def get_subjects():
    subjects = set()
    for student_marks in marks_data.values():
        for exam_marks in student_marks.values():
            subjects.update(exam_marks.keys())
    return sorted(subjects)

def get_subject_toppers():
    toppers = {}
    subjects = get_subjects()
    for subject in subjects:
        max_mark = -1
        topper = None
        for student in students:
            roll = student['roll_number']
            student_marks = marks_data.get(roll, {})
            for exam in ['mst1', 'mst2', 'final']:
                mark = student_marks.get(exam, {}).get(subject)
                if mark is not None and mark > max_mark:
                    max_mark = mark
                    topper = {'name': student['name'], 'roll_number': roll, 'grade': mark}
        toppers[subject] = topper
    return toppers

def get_subject_averages():
    averages = {}
    subjects = get_subjects()
    for subject in subjects:
        total = 0
        count = 0
        for student_marks in marks_data.values():
            for exam in ['mst1','mst2','final']:
                mark = student_marks.get(exam, {}).get(subject)
                if mark is not None:
                    total += mark
                    count += 1
        averages[subject] = total / count if count else 0
    return averages

def calculate_overall_average():
    total = 0
    count = 0
    for student in students:
        roll = student['roll_number']
        avg = calculate_student_average(roll)
        if avg:
            total += avg
            count += 1
    return total / count if count else 0

# Routes
@app.route("/")
def index():
    return render_template("index.html", students=students)

@app.route("/add_student", methods=["GET","POST"])
def add_student():
    if request.method == "POST":
        name = request.form['name']
        roll_number = request.form['roll_number']
        if any(s['roll_number'] == roll_number for s in students):
            flash("Roll Number already exists!", "error")
            return redirect(url_for('add_student'))
        students.append({'name': name, 'roll_number': roll_number})
        flash(f"Student {name} added!", "success")
        return redirect(url_for('index'))
    return render_template("add_student.html")

@app.route("/add_marks", methods=["GET","POST"])
def add_marks():
    exam_type = request.args.get('exam_type', None)  # optional, handled in page
    if request.method == "POST":
        roll_number = request.form['roll_number']
        exam_type = request.form['exam_type']
        subject = request.form['subject']
        marks = request.form.get('marks', None)
        if not marks:
            flash("Please enter marks", "error")
            return redirect(url_for('add_marks'))
        marks = float(marks)

        if roll_number not in marks_data:
            marks_data[roll_number] = {'mst1': {}, 'mst2': {}, 'final': {}}
        marks_data[roll_number][exam_type][subject] = marks
        flash(f"Added marks for {subject} under {exam_type.upper()} for student {roll_number}", "success")
        return redirect(url_for('add_marks'))

    return render_template("add_marks.html", students=students, exam_type=exam_type)

@app.route("/student/<roll_number>")
def view_student(roll_number):
    student = next((s for s in students if s['roll_number']==roll_number), None)
    if not student:
        flash("Student not found!", "error")
        return redirect(url_for('index'))
    student_marks = marks_data.get(roll_number, {})
    # Combine all exams into a single dict for display
    combined_grades = {}
    for exam in ['mst1','mst2','final']:
        combined_grades.update(student_marks.get(exam, {}))
    student['grades'] = combined_grades
    student['average'] = calculate_student_average(roll_number)
    return render_template("view_student.html", student=student)

@app.route("/reports")
def reports():
    subjects = get_subjects()
    subject_toppers = get_subject_toppers()
    subject_averages = get_subject_averages()
    overall_average = calculate_overall_average()
    return render_template("reports.html", subjects=subjects,
                           subject_toppers=subject_toppers,
                           subject_averages=subject_averages,
                           overall_average=overall_average)

# Export routes
@app.route("/export/csv")
def export_data():
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Roll Number','Name','Exam','Subject','Marks'])
    for roll, exams in marks_data.items():
        student_name = next((s['name'] for s in students if s['roll_number']==roll), '')
        for exam, subjects in exams.items():
            for subject, marks in subjects.items():
                cw.writerow([roll, student_name, exam.upper(), subject, marks])
    return si.getvalue(), 200, {'Content-Type':'text/csv'}

@app.route("/export/json")
def export_json():
    import json
    data = []
    for roll, exams in marks_data.items():
        student_name = next((s['name'] for s in students if s['roll_number']==roll), '')
        for exam, subjects in exams.items():
            for subject, marks in subjects.items():
                data.append({'roll_number': roll, 'name': student_name, 'exam': exam.upper(), 'subject': subject, 'marks': marks})
    return json.dumps(data, indent=4), 200, {'Content-Type':'application/json'}

@app.route("/backup")
def backup():
    data = ""
    for roll, exams in marks_data.items():
        student_name = next((s['name'] for s in students if s['roll_number']==roll), '')
        data += f"Student: {student_name} ({roll})\n"
        for exam, subjects in exams.items():
            data += f"  {exam.upper()}:\n"
            for subject, marks in subjects.items():
                data += f"    {subject}: {marks}\n"
        data += "\n"
    return data, 200, {'Content-Type':'text/plain'}

if __name__ == "__main__":
    app.run(debug=True)
