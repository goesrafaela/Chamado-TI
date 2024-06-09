import sqlite3

def init_db():
    conn = sqlite3.connect('requests.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            issue TEXT NOT NULL,
            urgency TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            resolved_by TEXT,
            resolved_timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
