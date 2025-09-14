import sqlite3

def check_database():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables in database:", tables)
    
    # Check structure of students table
    try:
        cursor.execute("PRAGMA table_info(students)")
        students_columns = cursor.fetchall()
        print("\nStudents table columns:")
        for col in students_columns:
            print(col)
    except:
        print("Students table doesn't exist or has issues")
    
    # Check structure of grades table
    try:
        cursor.execute("PRAGMA table_info(grades)")
        grades_columns = cursor.fetchall()
        print("\nGrades table columns:")
        for col in grades_columns:
            print(col)
    except:
        print("Grades table doesn't exist or has issues")
    
    conn.close()

if __name__ == '__main__':
    check_database()