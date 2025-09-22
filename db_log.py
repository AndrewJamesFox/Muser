import sqlite3
from datetime import datetime

DB_PATH = "musings.db"

def init_db():
    # create database (id, timestamp, content)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS musings (
                id INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

def add_thought(content):
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')   # get datetime as string (ISO format)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO musings (timestamp, content) VALUES (?, ?)", (timestamp, content))


def get_all_thoughts():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id, timestamp, content FROM musings ORDER BY id DESC LIMIT 100")
        return cursor.fetchall()


def delete_thought(thought_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM musings WHERE id = ?", (thought_id,))
    reindex_thoughts()  # reindex after deletion


def reindex_thoughts():
    """Reindex thoughts after deletions."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM musings ORDER BY id") # ordered by old IDs
        thoughts = cursor.fetchall()                        # fetch all rows as list of tuples
        cursor.execute("DELETE FROM musings")               # clear table

        # Reinsert with new IDs (1...N)
        # enumerate(thoughts, start=1) gives (new_id, (old_id, timestamp, content))
        for new_id, (old_id, timestamp, content) in enumerate(thoughts, start=1):
            cursor.execute("INSERT INTO musings (id, timestamp, content) VALUES (?, ?, ?)",
                           (new_id, timestamp, content))

        conn.commit()                                       # commit changes


def update_thought(thought_id, new_content):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE musings SET content = ? WHERE id = ?", (new_content, thought_id))

