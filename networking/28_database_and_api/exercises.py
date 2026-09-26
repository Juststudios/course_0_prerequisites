# Module 28: Database and API - Exercises

# Tier 1: Recall
# 1. What does ORM stand for?
# TODO: Assign the string value.
orm_meaning = ""

# 2. Which HTTP method is conventionally used for the 'Update' operation in CRUD?
# TODO: Assign the string value.
update_http_method = ""

# Tier 2: Modify
def get_user_data(user_id):
    # TODO: This mock API handler returns the entire database row.
    # Modify it to only return the 'id' and 'username', explicitly EXCLUDING the 'password_hash'.
    
    db_row = {"id": 1, "username": "admin", "password_hash": "bcrypt_xyz123", "is_active": True}
    return db_row

# Tier 3: Build
def map_crud_to_http():
    # TODO: Return a dictionary mapping the 4 CRUD operations to their standard HTTP methods.
    # Example format: {"Create": "POST", ...}
    pass

# Tier 4: Debug
def handle_request(db_pool):
    # TODO: This handler checks out a connection but crashes before returning it if there's an error.
    # Fix it using a try/finally block so the connection is always released.
    
    conn = db_pool.get_connection()
    # Buggy code:
    data = run_dangerous_query(conn) # This might throw an exception!
    db_pool.release(conn)
    return data

def run_dangerous_query(conn):
    raise ValueError("DB Crash!")
