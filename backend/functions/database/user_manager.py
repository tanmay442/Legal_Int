import sqlite3
import uuid
import bcrypt
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'DataBase', 'database.db'))

def get_db_connection():
    """Creates a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(email, password, full_name, role):
    """Creates a new user in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = str(uuid.uuid4())
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO Users (user_id, email, hashed_password, full_name, role) VALUES (?, ?, ?, ?, ?)",
            (user_id, email, hashed_password, full_name, role)
        )
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None  # User with this email already exists
    finally:
        conn.close()

def find_user_by_email(email):
    """Finds a user by their email address."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def find_user_by_id(user_id):
    """Finds a user by their user ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, email, full_name, role, created_at FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_password(stored_hash, provided_password):
    """Verifies a password against a stored hash."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

def search_users_by_email(email_query):
    """Finds users by a partial email match."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Using LIKE for a partial match, and limiting results
    cursor.execute(
        "SELECT user_id, email, full_name FROM Users WHERE email LIKE ? LIMIT 10", 
        (f'%{email_query}%',)
    )
    users = cursor.fetchall()
    conn.close()
    return users
