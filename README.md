# Student Performance Tracker

A professional **Flask web application** for teachers to track and manage student performance across different subjects.  
Features a **modern dark theme**, smooth animations, and comprehensive reporting capabilities.

---

## ✨ Features

- ✅ Add students with unique roll numbers  
- ✅ Assign grades for various subjects  
- ✅ View detailed student profiles with grade history  
- ✅ Calculate individual student averages  
- ✅ Identify subject-wise top performers  
- ✅ View class averages and performance reports  
- ✅ Export data in multiple formats (CSV, JSON, Text)  
- ✅ Responsive design with modern dark theme  
- ✅ Smooth animations and interactive UI  

---

## ⚙️ Installation & Running Locally

- ✅ **Clone the repository**  
  ```bash
  git clone https://github.com/MrStrange001/student-performance-tracker.git
✅ Navigate to the project folder

bash
Copy code
cd student-performance-tracker
✅ Create a virtual environment

bash
Copy code
python -m venv venv 
✅ Activate the virtual environment

Windows

bash
Copy code
.\venv\Scripts\activate
macOS/Linux

bash
Copy code
source venv/bin/activate
✅ Install dependencies

bash
Copy code
pip install -r requirements.txt
✅ Initialize the database

bash
Copy code
python database.py
✅ Run the application

bash
Copy code
python app.py
✅ Open the application in your browser

cpp
Copy code
http://127.0.0.1:5000/
📖 How to Use the Application
✅ Adding a Student

Click on "Add Student" in the navigation menu

Enter the student's full name

Enter a unique roll number

Click "Add Student" button

See confirmation message; the student appears in the list

✅ Assigning Grades

Click on "Add Grades" in the navigation menu

Select a student from the dropdown list

Enter the subject name

Enter the grade (0-100)

Click "Add Grade" button

See confirmation message

✅ Viewing Student Details

From the main page, find the student in the list

Click "View Details" button next to the student

View all grades and average score

Click "Back to Students" to return

✅ Generating Reports

Click on "Reports" in the navigation menu

View subject-wise top performers

Check class averages for each subject

See overall class performance

✅ Exporting Data

Click on "Export Data" in the navigation menu

Choose format: CSV, JSON, or Text

File will automatically download

## 📂 File Structure
graphql
Copy code
student-performance-tracker/
│
├── app.py              # Main Flask application
├── models.py           # Student and StudentTracker classes
├── database.py         # Database initialization and connection
├── templates/          # HTML templates
├── static/             # CSS styles and assets
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment configuration (optional)
└── runtime.txt         # Python version specification
