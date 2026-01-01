import sqlite3
from datetime import datetime
import os

# Global DB path (default)
DB_PATH = os.path.join(os.path.expanduser("~"), "musings.db")


def set_db_path(path: str):
    """Set a new database path."""
    global DB_PATH
    DB_PATH = path


def init_db(db_path=None):
    """Initialize the database, creating the table if it doesn't exist."""
    if db_path is None:
        db_path = DB_PATH
    
    # Ensure directory exists
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    # create database table if not exists
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS musings (
                id INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)


def add_thought(content, db_path=None):
    """Add a new thought."""
    if db_path is None:
        db_path = DB_PATH
    else:
        set_db_path(db_path)
    init_db(db_path)  # ensure table exists

    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO musings (timestamp, content) VALUES (?, ?)",
            (timestamp, content)
        )


def get_all_thoughts(db_path=None):
    """Get all thoughts from the database."""
    if db_path is None:
        db_path = DB_PATH
    init_db(db_path)  # ensure table exists
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT id, timestamp, content FROM musings ORDER BY id DESC LIMIT 100")
        return cursor.fetchall()


def delete_thought(thought_id, db_path=None):
    """Delete a thought by ID and reindex."""
    if db_path is None:
        db_path = DB_PATH
    else:
        set_db_path(db_path)
    init_db(db_path)  # ensure table exists

    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM musings WHERE id = ?", (thought_id,))
    reindex_thoughts(db_path)


def reindex_thoughts(db_path=None):
    """Reindex thoughts after deletions."""
    if db_path is None:
        db_path = DB_PATH
    else:
        set_db_path(db_path)
    init_db(db_path)  # ensure table exists

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM musings ORDER BY id")
        thoughts = cursor.fetchall()
        cursor.execute("DELETE FROM musings")
        for new_id, (old_id, timestamp, content) in enumerate(thoughts, start=1):
            cursor.execute(
                "INSERT INTO musings (id, timestamp, content) VALUES (?, ?, ?)",
                (new_id, timestamp, content)
            )
        conn.commit()


def update_thought(db_path, thought_id, new_content):
    """Update the content of a thought."""
    if db_path is None:
        db_path = DB_PATH
    init_db(db_path)  # ensure table exists

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE musings SET content = ? WHERE id = ?",
            (new_content, thought_id)
        )
        conn.commit()
