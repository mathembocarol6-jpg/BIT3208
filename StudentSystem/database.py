import sqlite3

connection = sqlite3.connect("student_management.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        course TEXT,
        email TEXT UNIQUE
    )
''')

connection.commit()
connection.close()

print("Database and 'students' table created successfully!")