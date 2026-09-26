# Module 28: Database and API - Solutions

# Tier 1: Recall
orm_meaning = "Object-Relational Mapper"
update_http_method = "PUT" # (or PATCH)

# Tier 2: Modify
def get_user_data(user_id):
    db_row = {"id": 1, "username": "admin", "password_hash": "bcrypt_xyz123", "is_active": True}
    # Fix: Selectively build the response dictionary (DTO)
    return {
        "id": db_row["id"],
        "username": db_row["username"]
    }

# Tier 3: Build
def map_crud_to_http():
    return {
        "Create": "POST",
        "Read": "GET",
        "Update": "PUT", # or PATCH
        "Delete": "DELETE"
    }

# Tier 4: Debug
def handle_request(db_pool):
    conn = db_pool.get_connection()
    try:
        data = run_dangerous_query(conn)
        return data
    finally:
        # Fix: Ensure the connection is released back to the pool even if an error occurs
        db_pool.release(conn)

def run_dangerous_query(conn):
    raise ValueError("DB Crash!")
