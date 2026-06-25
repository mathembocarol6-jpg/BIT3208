import sqlite3

connection = sqlite3.connect("employee_management.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        department TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        salary REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')

connection.commit()
connection.close()

print("Employee database and Users authentication table initialized successfully!")