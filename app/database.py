import sqlite3
import os
from datetime import datetime

DB_PATH = "data/events.db"

def init_db():
    """Initializes the database and creates the events table."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Added 'score' column for Phase III AI Threat Scoring
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT,
            src TEXT,
            dst TEXT,
            details TEXT,
            score REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

def save_event(event_type, src, dst, details, score=0.0):
    """Saves a network event to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO events (timestamp, type, src, dst, details, score) VALUES (?, ?, ?, ?, ?, ?)",
            (timestamp, event_type, src, dst, details, score)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[!] Database Error: {e}")

def get_recent_events(limit=50):
    """Fetches the latest events for the dashboard. (The missing function!)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        # Use Row factory to return data as a dictionary (easier for Flask)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Order by autoincrement id so newest inserts are always first,
        # even when multiple events share the same second timestamp.
        cursor.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[!] Fetch Error: {e}")
        return []