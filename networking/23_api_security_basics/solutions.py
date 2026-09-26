# Module 23: API Security Basics - Solutions

# Tier 1: Recall
rate_limit_status_code = 429
tls_meaning = "Transport Layer Security"

# Tier 2: Modify
import requests

def insecure_api_call(url):
    # Fix: Remove verify=False (it defaults to True), or explicitly set verify=True.
    response = requests.get(url, verify=True)
    return response

# Tier 3: Build
import time

def handle_rate_limit(url, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 429:
            time.sleep(1)
            continue
        return response
    # If we exhaust retries, just return the last response
    return response

# Tier 4: Debug
def process_user_input(db_connection, user_id):
    # Fix: Use parameterized queries to let the database driver handle escaping
    query = "SELECT * FROM users WHERE id = ?" # or %s depending on the driver
    cursor = db_connection.cursor()
    cursor.execute(query, (user_id,))
    return cursor.fetchall()
