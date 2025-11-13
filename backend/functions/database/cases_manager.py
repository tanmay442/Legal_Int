import sqlite3
import uuid
import os
from . import permissions_manager

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'DataBase', 'database.db'))

def get_db_connection():
    """Creates a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_case(case_name, creator_id):
    """Creates a new case and a corresponding permissions table."""
    conn = get_db_connection()
    cursor = conn.cursor()

    case_id = str(uuid.uuid4())
    
    try:
        cursor.execute(
            "INSERT INTO Cases (case_id, case_name, creator_id) VALUES (?, ?, ?)",
            (case_id, case_name, creator_id)
        )
        conn.commit()

        permissions_manager.grant_access(case_id, creator_id, 'sudo')

        return case_id
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_all_cases():
    """Retrieves all cases from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases ORDER BY created_at DESC")
    cases = cursor.fetchall()
    conn.close()
    return cases

def get_user_cases(user_id):
    """Retrieves all cases a user has access to."""
    conn = get_db_connection()
    cursor = conn.cursor()

    accessible_cases_query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'CaseAccessPermissions_%'"
    cursor.execute(accessible_cases_query)
    permission_tables = cursor.fetchall()

    accessible_case_ids = []
    for table in permission_tables:
        table_name = table['name']
        query = f"SELECT case_id FROM {table_name} WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            accessible_case_ids.append(result['case_id'])
    
    if not accessible_case_ids:
        return []

    placeholders = ','.join('?' for _ in accessible_case_ids)
    query = f"SELECT * FROM Cases WHERE case_id IN ({placeholders}) ORDER BY created_at DESC"
    cursor.execute(query, accessible_case_ids)
    cases = cursor.fetchall()
    
    conn.close()
    return cases

def get_case_by_id(case_id):
    """Retrieves a single case by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cases WHERE case_id = ?", (case_id,))
    case = cursor.fetchone()
    conn.close()
    return case

def update_case_status(case_id, status):
    """Updates the status of a case."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Cases SET status = ? WHERE case_id = ?",
            (status, case_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()
