from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# Path to the database we created earlier
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.db')

def get_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM network_events ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    events = get_events()
    return render_template('index.html', events=events)

if __name__ == '__main__':
    print("[*] Dashboard running at http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000) # '0.0.0.0' means "listen to everyone on the network"