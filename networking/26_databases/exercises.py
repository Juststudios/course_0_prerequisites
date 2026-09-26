# Module 26: Databases - Exercises

# Tier 1: Recall
# 1. What does ACID stand for in the context of databases?
# TODO: Assign the string value to the variable.
acid_meaning = ""

# 2. SQLite is an example of a NoSQL database. (True/False)
# TODO: Assign a boolean.
is_sqlite_nosql = None

# Tier 2: Modify
import sqlite3

def get_db_version():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    # TODO: Modify the query to select the sqlite version. 
    # Hint: The query string is "SELECT sqlite_version();"
    query = ""
    cursor.execute(query)
    version = cursor.fetchone()[0]
    conn.close()
    return version

# Tier 3: Build
def create_and_insert():
    # TODO: Connect to an in-memory sqlite database.
    # Create a table called 'products' with columns 'id' (INTEGER PRIMARY KEY) and 'price' (REAL).
    # Insert a product with a price of 19.99.
    # Return the connection object.
    pass

# Tier 4: Debug
def fetch_user(user_id):
    # TODO: This code has a syntax error in the SQL string. Fix it.
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    # Buggy code:
    cursor.execute(f"SELECT * FROM users WHERE id == {user_id}")
    result = cursor.fetchone()
    conn.close()
    return result
