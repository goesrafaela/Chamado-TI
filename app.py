import sqlite3
from flask import Flask, request, jsonify, render_template, redirect

from datetime import datetime, timedelta

app = Flask(__name__)

DATABASE = 'requests.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
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

@app.before_request
def before_request():
    init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests')
    requests_list = cursor.fetchall()
    conn.close()
    return render_template('admin.html', requests=requests_list)

@app.route('/submit-request', methods=['POST'])
def submit_request():
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    issue = request.form['issue']
    urgency = request.form['urgency']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (name, email, department, issue, urgency, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, department, issue, urgency, timestamp, 'Pending'))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Solicitação enviada com sucesso!'})

@app.route('/admin', methods=['GET'])
def admin_panel():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests')
    requests_list = cursor.fetchall()
    conn.close()
    return render_template('admin.html', requests=requests_list)

@app.route('/admin/delete-request', methods=['POST'])
def delete_request():
    request_id = request.form['request_id']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM requests WHERE id = ?', (request_id,))
    conn.commit()
    conn.close()
    
    return redirect('/admin')

@app.route('/resolve-request/<int:request_id>', methods=['POST'])
def resolve_request(request_id):
    resolved_by = request.form['resolved_by']
    resolved_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE requests
        SET status = ?, resolved_by = ?, resolved_timestamp = ?
        WHERE id = ?
    ''', ('Resolved', resolved_by, resolved_timestamp, request_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Solicitação marcada como resolvida!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
