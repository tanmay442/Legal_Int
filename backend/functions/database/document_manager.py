import sqlite3
import uuid
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'DataBase', 'database.db'))

def get_db_connection():
    """Creates a database connection."""
    return sqlite3.connect(DB_PATH)

def add_document(case_id, uploader_id, file_name, storage_path):
    """Adds a new document record to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    doc_id = str(uuid.uuid4())
    
    try:
        cursor.execute(
            "INSERT INTO Documents (doc_id, case_id, uploader_id, file_name, storage_path) VALUES (?, ?, ?, ?, ?)",
            (doc_id, case_id, uploader_id, file_name, storage_path)
        )
        conn.commit()
        return doc_id
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_case_documents(case_id):
    """Retrieves all documents for a given case."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Documents WHERE case_id = ? ORDER BY uploaded_at DESC", (case_id,))
    documents = cursor.fetchall()
    conn.close()
    return documents

def get_document_by_id(doc_id):
    """Retrieves a single document by its ID."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Documents WHERE doc_id = ?", (doc_id,))
    document = cursor.fetchone()
    conn.close()
    return document
