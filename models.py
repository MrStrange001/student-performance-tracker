import sqlite3

class Student:
    def __init__(self, id, name, roll_number):
        self.id = id
        self.name = name
        self.roll_number = roll_number
        self.grades = {}
    
    def add_grade(self, subject, grade):
        self.grades[subject] = grade
    
    def calculate_average(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)
    
    def get_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'roll_number': self.roll_number,
            'grades': self.grades,
            'average': self.calculate_average()
        }

class StudentTracker:
    def __init__(self, db_connection):
        self.conn = db_connection
        # Detect if we're using SQLite or PostgreSQL
        self.is_sqlite = 'sqlite' in str(type(db_connection)).lower()
    
    def _get_placeholder(self):
        """Return the correct parameter placeholder for the database"""
        return '?' if self.is_sqlite else '%s'
    
    def add_student(self, name, roll_number):
        try:
            cursor = self.conn.cursor()
            placeholder = self._get_placeholder()
            query = f'INSERT INTO students (name, roll_number) VALUES ({placeholder}, {placeholder})'
            cursor.execute(query, (name, roll_number))
            self.conn.commit()
            return True, "Student added successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_student(self, student_id=None, roll_number=None):
        cursor = self.conn.cursor()
        placeholder = self._get_placeholder()
        
        if student_id:
            query = f'SELECT * FROM students WHERE id = {placeholder}'
            cursor.execute(query, (student_id,))
        elif roll_number:
            query = f'SELECT * FROM students WHERE roll_number = {placeholder}'
            cursor.execute(query, (roll_number,))
        else:
            return None
        
        student_data = cursor.fetchone()
        if not student_data:
            return None
        
        student = Student(student_data['id'], student_data['name'], student_data['roll_number'])
        
        # Get grades for this student
        query = f'SELECT subject, grade FROM grades WHERE student_id = {placeholder}'
        cursor.execute(query, (student.id,))
        grades_data = cursor.fetchall()
        for grade_data in grades_data:
            student.add_grade(grade_data['subject'], grade_data['grade'])
        
        return student
    
    def get_all_students(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, roll_number FROM students')
        students_data = cursor.fetchall()
        
        students = []
        for student_data in students_data:
            student = Student(student_data['id'], student_data['name'], student_data['roll_number'])
            
            # Get grades for this student
            placeholder = self._get_placeholder()
            query = f'SELECT subject, grade FROM grades WHERE student_id = {placeholder}'
            cursor.execute(query, (student.id,))
            grades_data = cursor.fetchall()
            for grade_data in grades_data:
                student.add_grade(grade_data['subject'], grade_data['grade'])
            
            students.append(student)
        
        return students
    
    def add_grade(self, student_id, subject, grade):
        try:
            cursor = self.conn.cursor()
            placeholder = self._get_placeholder()
            
            # Check if grade already exists for this subject and student
            query = f'SELECT id FROM grades WHERE student_id = {placeholder} AND subject = {placeholder}'
            cursor.execute(query, (student_id, subject))
            existing_grade = cursor.fetchone()
            
            if existing_grade:
                # Update existing grade
                query = f'UPDATE grades SET grade = {placeholder} WHERE id = {placeholder}'
                cursor.execute(query, (grade, existing_grade['id']))
                message = "Grade updated successfully!"
            else:
                # Insert new grade
                query = f'INSERT INTO grades (student_id, subject, grade) VALUES ({placeholder}, {placeholder}, {placeholder})'
                cursor.execute(query, (student_id, subject, grade))
                message = "Grade added successfully!"
                
            self.conn.commit()
            return True, message
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_subject_topper(self, subject):
        cursor = self.conn.cursor()
        placeholder = self._get_placeholder()
        
        query = f'''
            SELECT s.id, s.name, s.roll_number, g.grade 
            FROM students s 
            JOIN grades g ON s.id = g.student_id 
            WHERE g.subject = {placeholder} 
            ORDER BY g.grade DESC 
            LIMIT 1
        '''
        cursor.execute(query, (subject,))
        
        result = cursor.fetchone()
        if result:
            return {
                'name': result['name'],
                'roll_number': result['roll_number'],
                'grade': result['grade']
            }
        return None
    
    def get_class_average(self, subject=None):
        cursor = self.conn.cursor()
        placeholder = self._get_placeholder()
        
        if subject:
            query = f'SELECT AVG(grade) as avg FROM grades WHERE subject = {placeholder}'
            cursor.execute(query, (subject,))
        else:
            cursor.execute('SELECT AVG(grade) as avg FROM grades')
        
        result = cursor.fetchone()
        return result['avg'] if result and result['avg'] else 0