import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'DataBase', 'database.db'))

def get_db_connection():
    """Creates a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def sanitize_case_id(case_id):
    """Removes hyphens from the case_id to create a valid table name."""
    return case_id.replace('-', '')

def get_permissions_table_name(case_id):
    """Returns the sanitized table name for a given case_id."""
    return f"CaseAccessPermissions_{sanitize_case_id(case_id)}"

def create_permissions_table(case_id):
    """Creates a new permissions table for a specific case."""
    conn = get_db_connection()
    cursor = conn.cursor()
    table_name = get_permissions_table_name(case_id)
    
    try:
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            case_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            access_level TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES Cases(case_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            UNIQUE (case_id, user_id)
        )
        ''')
        conn.commit()
    finally:
        conn.close()

def grant_access(case_id, user_id, access_level):
    """Grants a user access to a case."""
    create_permissions_table(case_id)

    conn = get_db_connection()
    cursor = conn.cursor()
    table_name = get_permissions_table_name(case_id)

    try:
        cursor.execute(
            f"INSERT INTO {table_name} (case_id, user_id, access_level) VALUES (?, ?, ?)",
            (case_id, user_id, access_level)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # If user already has access, update their access level
        cursor.execute(
            f"UPDATE {table_name} SET access_level = ? WHERE user_id = ? AND case_id = ?",
            (access_level, user_id, case_id)
        )
        conn.commit()
        return True
    finally:
        conn.close()

def check_access(case_id, user_id):
    """Checks if a user has any access to a given case."""
    conn = get_db_connection()
    cursor = conn.cursor()
    table_name = get_permissions_table_name(case_id)

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if cursor.fetchone() is None:
            return False

        cursor.execute(f"SELECT 1 FROM {table_name} WHERE user_id = ? AND case_id = ?", (user_id, case_id))
        result = cursor.fetchone()
        return result is not None
    finally:
        conn.close()

def get_user_access_level(case_id, user_id):
    """Gets the access level for a user on a specific case."""
    conn = get_db_connection()
    cursor = conn.cursor()
    table_name = get_permissions_table_name(case_id)

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if cursor.fetchone() is None:
            return None

        cursor.execute(f"SELECT access_level FROM {table_name} WHERE user_id = ? AND case_id = ?", (user_id, case_id))
        result = cursor.fetchone()
        return result['access_level'] if result else None
    finally:
        conn.close()

def get_case_permissions(case_id):
    """Retrieves all user permissions for a specific case."""
    conn = get_db_connection()
    cursor = conn.cursor()
    table_name = get_permissions_table_name(case_id)

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if cursor.fetchone() is None:
            return []

        # Join with Users table to get user details
        query = f"""
            SELECT p.user_id, u.full_name, u.email, p.access_level
            FROM {table_name} p
            JOIN Users u ON p.user_id = u.user_id
            WHERE p.case_id = ?
        """
        cursor.execute(query, (case_id,))
        permissions = cursor.fetchall()
        return permissions
    finally:
        conn.close()