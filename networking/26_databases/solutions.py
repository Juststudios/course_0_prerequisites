# Module 26: Databases - Solutions

# Tier 1: Recall
acid_meaning = "Atomicity, Consistency, Isolation, Durability"
is_sqlite_nosql = False

# Tier 2: Modify
import sqlite3

def get_db_version():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    query = "SELECT sqlite_version();"
    cursor.execute(query)
    version = cursor.fetchone()[0]
    conn.close()
    return version

# Tier 3: Build
def create_and_insert():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, price REAL)")
    cursor.execute("INSERT INTO products (price) VALUES (19.99)")
    conn.commit()
    return conn

# Tier 4: Debug
def fetch_user(user_id):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    # Fix: SQL uses a single '=' for equality, not '==' like Python
    # Also, better to use parameterized queries
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result
