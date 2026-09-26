# Module 27: PostgreSQL - Solutions

# Tier 1: Recall
postgres_default_port = 5432
mvcc_meaning = "Multi-Version Concurrency Control"

# Tier 2: Modify
def build_connection_string(user, password, host, port, dbname):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Tier 3: Build
def safe_insert_query():
    return "INSERT INTO users (name, email) VALUES (%s, %s);"

# Tier 4: Debug
def process_data(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM some_table")
        data = cursor.fetchall()
        return data
    finally:
        cursor.close() # Ensures the cursor is always closed
