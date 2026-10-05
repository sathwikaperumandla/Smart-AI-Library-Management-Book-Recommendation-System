import sqlite3

DATABASE = "library.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # Add sample books
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:
        books = [
            ("Python Programming", "John Smith", "Programming"),
            ("Data Structures", "Mark Allen", "Computer Science"),
            ("Machine Learning", "Tom Brown", "AI"),
            ("Artificial Intelligence", "Andrew Wilson", "AI"),
            ("Database Management", "James Brown", "Database"),
            ("Web Development", "Robert Smith", "Programming"),
            ("Java Programming", "James Gosling", "Programming"),
            ("Computer Networks", "Andrew Tanenbaum", "Networking")
        ]

        cursor.executemany("""
            INSERT INTO books (title, author, category)
            VALUES (?, ?, ?)
        """, books)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")