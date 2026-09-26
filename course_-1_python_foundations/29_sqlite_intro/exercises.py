"""
Module 29 Exercises — SQLite Intro
"""
import sqlite3

# Level 1: Recall
# 1. Why do we use placeholders (?) instead of f-strings for SQL?
# 2. What does conn.commit() do?

# Level 2: Modify
# TODO: Modify this function to return all names from the users table.
def get_all_users(conn: sqlite3.Connection):
    raise NotImplementedError("Implement get_all_users")

# Level 3: Build
# TODO: Write a function that takes a connection, creates a table called 'logs' 
# with id (INTEGER PRIMARY KEY) and message (TEXT).
def create_logs_table(conn: sqlite3.Connection):
    raise NotImplementedError("Implement create_logs_table")

# Level 4: Debug
# TODO: The following function has a SQL injection vulnerability. Fix it.
def get_user_by_name(conn: sqlite3.Connection, name: str):
    # cursor = conn.execute(f"SELECT * FROM users WHERE name='{name}'")
    raise NotImplementedError("Fix the bug")
