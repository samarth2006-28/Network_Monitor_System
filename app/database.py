import sqlite3

DB_PATH = "data/events.db"

def init_db():
    """Creates the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            source_ip TEXT,
            dest_ip TEXT,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_event(event_type, src, dst, details):
    """Inserts a new event into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO network_events (event_type, source_ip, dest_ip, details)
        VALUES (?, ?, ?, ?)
    ''', (event_type, src, dst, details))
    conn.commit()
    conn.close()