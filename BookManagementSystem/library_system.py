import sqlite3

DB_NAME = "library_management.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_book():
    print("\n--- Add New Book (CREATE) ---")
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    category = input("Enter Category: ")

    if not title.strip() or not author.strip() or not category.strip():
        print("Error: All fields are required.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, category) VALUES (?, ?, ?)", (title, author, category))
    conn.commit()
    print(f"Success: '{title}' added to library catalog.")
    conn.close()

def read_books():
    print("\n--- Library Catalogue (READ) ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("The library catalog is currently empty.")
        return

    print(f"{'Book ID':<9} | {'Title':<30} | {'Author':<20} | {'Category':<15}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<9} | {row[1]:<30} | {row[2]:<20} | {row[3]:<15}")

def update_book():
    print("\n--- Update Book Details (UPDATE) ---")
    try:
        book_id = int(input("Enter Book ID to update: "))
    except ValueError:
        print("Invalid Book ID format.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print("Book record not found.")
        conn.close()
        return

    print(f"\nCurrent Data -> Title: {book[1]}, Author: {book[2]}, Category: {book[3]}")
    print("Press Enter without typing to keep current details.")

    new_title = input(f"New Title ({book[1]}): ") or book[1]
    new_author = input(f"New Author ({book[2]}): ") or book[2]
    new_category = input(f"New Category ({book[3]}): ") or book[3]

    cursor.execute('''UPDATE books SET title = ?, author = ?, category = ? WHERE book_id = ?''',
                   (new_title, new_author, new_category, book_id))
    conn.commit()
    print("Success: Book records updated.")
    conn.close()

def delete_book():
    print("\n--- Remove Book (DELETE) ---")
    try:
        book_id = int(input("Enter Book ID to delete: "))
    except ValueError:
        print("Invalid Book ID format.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    if not cursor.fetchone():
        print("Book record not found.")
        conn.close()
        return

    cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()
    print("Success: Book removed from library system.")
    conn.close()

def main():
    init_db()  # This safely auto-builds your table structure if it is missing
    while True:
        print("\n==============================")
        print("      Library Management      ")
        print("==============================")
        print("1. Create (Add Book)")
        print("2. Read (View Books)")
        print("3. Update (Edit Book)")
        print("4. Delete (Remove Book)")
        print("5. Exit Program")
        
        choice = input("\nSelect an option (1-5): ")
        if choice == '1':
            create_book()
        elif choice == '2':
            read_books()
        elif choice == '3':
            update_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            print("Exiting Library System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()