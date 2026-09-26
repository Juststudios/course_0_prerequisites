# Module 22: Authentication - Solutions

# Tier 1: Recall
auth_header_name = "Authorization"
is_base64_encryption = False # Base64 is just encoding, it provides no cryptographic security.

# Tier 2: Modify
import requests

def get_data_with_api_key(url, api_key):
    headers = {
        "X-API-Key": api_key
    }
    response = requests.get(url, headers=headers)
    return response

# Tier 3: Build
def authenticate_and_fetch(login_url, data_url, username, password):
    # 1. Login to get the token
    login_resp = requests.post(login_url, auth=(username, password))
    if login_resp.status_code != 200:
        return None
    
    token = login_resp.json().get("token")
    if not token:
        return None
        
    # 2. Use the token to fetch data
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.get(data_url, headers=headers)

# Tier 4: Debug
def flawed_bearer_auth(url, token):
    # Fix: The scheme name for standard bearer tokens is 'Bearer', not 'token'.
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.get(url, headers=headers)
