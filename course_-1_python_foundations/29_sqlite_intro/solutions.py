"""
Module 29 Solutions
"""
import sqlite3

# Level 1:
# 1. To prevent SQL injection attacks.
# 2. Saves the changes made during the current transaction.

# Level 2:
def get_all_users(conn: sqlite3.Connection):
    return conn.execute("SELECT name FROM users").fetchall()

# Level 3:
def create_logs_table(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT
        )
    """)
    conn.commit()

# Level 4:
def get_user_by_name(conn: sqlite3.Connection, name: str):
    return conn.execute("SELECT * FROM users WHERE name=?", (name,)).fetchall()
