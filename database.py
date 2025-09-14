import sqlite3
import os
from urllib.parse import urlparse
import time

def get_db_connection():
    # Check if we're on Heroku (DATABASE_URL will be set)
    if 'DATABASE_URL' in os.environ:
        # Heroku uses PostgreSQL, not SQLite
        import psycopg2
        from psycopg2.extras import DictCursor
        
        # Parse the database URL
        url = urlparse(os.environ['DATABASE_URL'])
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            sslmode='require'
        )
        conn.cursor_factory = DictCursor
        return conn
    else:
        # Local development with SQLite
        conn = sqlite3.connect('students.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    # For SQLite, check if we can safely remove the existing file
    if not 'DATABASE_URL' in os.environ and os.path.exists('students.db'):
        try:
            # Try to open the file to see if it's accessible
            test_conn = sqlite3.connect('students.db')
            test_conn.close()
            # If we can connect, we can remove it
            os.remove('students.db')
            print("Removed old database file")
        except (sqlite3.Error, PermissionError):
            print("Database file is locked or inaccessible. Using existing database.")
            # Continue with existing database instead of failing
            return setup_tables()
    
    return setup_tables()

def setup_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if we're using PostgreSQL
    if 'DATABASE_URL' in os.environ:
        # Create students table for PostgreSQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                roll_number TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Create grades table for PostgreSQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id SERIAL PRIMARY KEY,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                grade INTEGER NOT NULL CHECK(grade >= 0 AND grade <= 100),
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
            )
        ''')
    else:
        # SQLite implementation - use IF NOT EXISTS to avoid errors
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT UNIQUE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                grade INTEGER NOT NULL CHECK(grade >= 0 AND grade <= 100),
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
    
    conn.commit()
    conn.close()
    print("Database tables created successfully!")
    return True

if __name__ == '__main__':
    init_db()