import sqlite3

DB_NAME = "student_management.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            email TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def add_student():
    print("\n--- Add New Student ---")
    name = input("Enter Name: ")
    if not name.strip():
        print("Error: Student name cannot be empty.")
        return
    try:
        age = int(input("Enter Age: "))
    except ValueError:
        print("Invalid age. Must be an integer.")
        return
    course = input("Enter Course: ")
    email = input("Enter Email: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)", 
                       (name, age, course, email))
        conn.commit()
        print(f"Success: Student '{name}' added successfully!")
    except sqlite3.IntegrityError:
        print("Error: A student with this email already exists.")
    finally:
        conn.close()

def view_students():
    print("\n--- Student Records ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No student records found.")
        return

    print(f"{'ID':<5} | {'Name':<20} | {'Age':<5} | {'Course':<20} | {'Email':<25}")
    print("-" * 85)
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<5} | {row[3]:<20} | {row[4]:<25}")

def edit_student():
    print("\n--- Edit Student Information ---")
    try:
        student_id = int(input("Enter Student ID to edit: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        conn.close()
        return

    print(f"\nCurrent Data -> Name: {student[1]}, Age: {student[2]}, Course: {student[3]}, Email: {student[4]}")
    print("Press Enter to keep current value.")

    new_name = input(f"Enter new name ({student[1]}): ") or student[1]
    new_age_input = input(f"Enter new age ({student[2]}): ")
    new_age = int(new_age_input) if new_age_input.strip() else student[2]
    new_course = input(f"Enter new course ({student[3]}): ") or student[3]
    new_email = input(f"Enter new email ({student[4]}): ") or student[4]

    try:
        cursor.execute('''UPDATE students SET name = ?, age = ?, course = ?, email = ? WHERE id = ?''',
                       (new_name, new_age, new_course, new_email, student_id))
        conn.commit()
        print("Success: Student information updated.")
    except sqlite3.IntegrityError:
        print("Error: Email already in use by another student.")
    finally:
        conn.close()

def delete_student():
    print("\n--- Delete Student ---")
    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        print("Student not found.")
        conn.close()
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    print("Success: Student record deleted.")
    conn.close()

def main():
    init_db()  # <-- This line fixes your error by building the table right away!
    while True:
        print("\n==============================")
        print("  Student Management System   ")
        print("==============================")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Edit Existing Student")
        print("4. Delete Student Profile")
        print("5. Exit Program")
        
        choice = input("\nSelect an option (1-5): ")
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            edit_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("System shutting down. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()