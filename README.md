Student Performance Tracker

A professional Flask web application for teachers to track and manage student performance across different subjects. Features a modern dark theme with smooth animations and comprehensive reporting capabilities.

Features

✅ Add students with unique roll numbers

✅ Assign grades for various subjects

✅ View detailed student profiles with grade history

✅ Calculate individual student averages

✅ Identify subject-wise top performers

✅ View class averages and performance reports

✅ Export data in multiple formats (CSV, JSON, Text)

✅ Responsive design with modern dark theme

✅ Smooth animations and interactive UI

Installation

Clone the repository

Create a virtual environment:

python -m venv venv


Activate the virtual environment:

Windows:

.\venv\Scripts\activate


macOS/Linux:

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Initialize the database:

python database.py


Run the application:

python app.py

📖 How to Use the Application

Open your browser and go to http://127.0.0.1:5000/

1. Running the App Locally

Open your project folder (D:\Python\student_performance_tracker or wherever you saved it).

Create and activate your virtual environment.

Install dependencies with pip install -r requirements.txt.

Run the application using python app.py.

The app will start at http://127.0.0.1:5000/ in your browser.

2. Adding a Student

Click on "Add Student" in the navigation menu

Enter the student's full name

Enter a unique roll number

Click "Add Student" button

See confirmation message and student appears in list

3. Assigning Grades

Click on "Add Grades" in the navigation menu

Select a student from the dropdown list

Enter the subject name

Enter the grade (0-100)

Click "Add Grade" button

See confirmation message

4. Viewing Student Details

From the main page, find the student in the list

Click "View Details" button next to the student

View all grades and average score

Click "Back to Students" to return

5. Generating Reports

Click on "Reports" in the navigation menu

View subject-wise top performers

Check class averages for each subject

See overall class performance

6. Exporting Data

Click on "Export Data" in the navigation menu

Choose format: CSV, JSON, or Text

File will automatically download

File Structure

app.py - Main Flask application

models.py - Student and StudentTracker classes

database.py - Database initialization and connection

templates/ - HTML templates

static/ - CSS styles

requirements.txt - Python dependencies

Procfile - Deployment configuration (optional)

runtime.txt - Python version specification
