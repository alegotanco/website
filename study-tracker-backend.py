from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Ensure the database file is created in the same directory as this script
db_path = os.path.join(os.path.dirname(__file__), 'study_tracker.db')

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS classes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  goal INTEGER NOT NULL,
                  studied INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/classes', methods=['GET', 'POST'])
def handle_classes():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    if request.method == 'GET':
        c.execute("SELECT * FROM classes")
        classes = [{'id': row[0], 'name': row[1], 'goal': row[2], 'studied': row[3]} for row in c.fetchall()]
        conn.close()
        return jsonify(classes)
    
    elif request.method == 'POST':
        data = request.json
        c.execute("INSERT INTO classes (name, goal, studied) VALUES (?, ?, ?)",
                  (data['name'], data['goal'], 0))
        conn.commit()
        class_id = c.lastrowid
        conn.close()
        return jsonify({'id': class_id, 'name': data['name'], 'goal': data['goal'], 'studied': 0}), 201

@app.route('/classes/<int:class_id>', methods=['PUT', 'DELETE'])
def handle_class(class_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        c.execute("UPDATE classes SET name = ?, goal = ?, studied = ? WHERE id = ?",
                  (data['name'], data['goal'], data['studied'], class_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Class updated successfully'}), 200
    
    elif request.method == 'DELETE':
        c.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Class deleted successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
