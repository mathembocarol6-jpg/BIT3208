import sqlite3

connection = sqlite3.connect("library_management.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')

connection.commit()
connection.close()

print("Library Database and 'books' table created successfully!")