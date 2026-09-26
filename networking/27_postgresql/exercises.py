# Module 27: PostgreSQL - Exercises

# Tier 1: Recall
# 1. What is the default port for PostgreSQL?
# TODO: Assign the integer value.
postgres_default_port = 0

# 2. What does MVCC stand for?
# TODO: Assign the string value.
mvcc_meaning = ""

# Tier 2: Modify
def build_connection_string(user, password, host, port, dbname):
    # TODO: Modify this function to return a correctly formatted PostgreSQL connection URI.
    # Format: postgresql://user:password@host:port/dbname
    pass

# Tier 3: Build
# (Conceptual build, assuming psycopg2 is not installed in the testing environment)
def safe_insert_query():
    # TODO: Write the EXACT SQL string with psycopg2 parameter placeholders (%s)
    # to insert a name and email into a 'users' table.
    # Return the string.
    pass

# Tier 4: Debug
def process_data(conn):
    # TODO: This function opens a cursor but fails to close it if an exception occurs.
    # Fix the code using a try/finally block.
    
    cursor = conn.cursor()
    # Assume this might raise an error
    cursor.execute("SELECT * FROM some_table")
    data = cursor.fetchall()
    cursor.close()
    return data
