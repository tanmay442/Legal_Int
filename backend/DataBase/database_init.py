import sqlite3
import os

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def create_tables():
    """Creates all the necessary tables in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('advocate', 'judge', 'government_agency', 'private_intel')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Cases table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cases (
        case_id TEXT PRIMARY KEY,
        case_name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Open',
        creator_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (creator_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Documents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Documents (
        doc_id TEXT PRIMARY KEY,
        case_id TEXT NOT NULL,
        uploader_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        storage_path TEXT UNIQUE NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES Cases(case_id) ON DELETE CASCADE,
        FOREIGN KEY (uploader_id) REFERENCES Users(user_id)
    )
    ''')

    print("Tables created successfully.")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()