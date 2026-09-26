import sqlite3
import json

def init_db():
    conn = sqlite3.connect('todo_api.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Mocking a simple API layer
class TodoAPI:
    def __init__(self):
        init_db()
        
    def _get_conn(self):
        conn = sqlite3.connect('todo_api.db')
        conn.row_factory = sqlite3.Row
        return conn

    # POST /todos
    def create_todo(self, request_body: str):
        data = json.loads(request_body)
        task = data.get("task")
        
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return {"status": 201, "body": {"id": new_id, "task": task, "completed": False}}

    # GET /todos
    def get_todos(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        conn.close()
        
        todos = [dict(row) for row in rows]
        # SQLite stores booleans as 0/1, convert back for the API
        for t in todos:
            t['completed'] = bool(t['completed'])
            
        return {"status": 200, "body": todos}

if __name__ == "__main__":
    api = TodoAPI()
    print("API Initialized.")
    
    print("\nSimulating: POST /todos")
    resp1 = api.create_todo('{"task": "Learn API Integration"}')
    print(resp1)
    
    print("\nSimulating: GET /todos")
    resp2 = api.get_todos()
    print(resp2)
