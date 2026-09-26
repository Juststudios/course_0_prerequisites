# Module 23: API Security Basics - Exercises

# Tier 1: Recall
# 1. What HTTP status code is used to indicate that a client has hit a rate limit?
# TODO: Write the integer status code in the variable `rate_limit_status_code`.
rate_limit_status_code = 0

# 2. What does TLS stand for?
# TODO: Write the full string in `tls_meaning`.
tls_meaning = ""


# Tier 2: Modify
import requests

def insecure_api_call(url):
    # TODO: Modify this function so it does NOT suppress TLS verification warnings,
    # and properly verifies the server's certificate.
    # Currently it is dangerously ignoring certificate errors.
    response = requests.get(url, verify=False)
    return response


# Tier 3: Build
def handle_rate_limit(url, max_retries=3):
    # TODO: Build a function that makes a GET request to the URL.
    # If it receives a 429 status code, it should wait 1 second and retry,
    # up to `max_retries` times.
    # Return the final response object.
    pass


# Tier 4: Debug
def process_user_input(db_connection, user_id):
    # TODO: This code is vulnerable to SQL Injection.
    # Fix the implementation to use parameterized queries instead of string formatting.
    
    # Buggy code:
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor = db_connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()
