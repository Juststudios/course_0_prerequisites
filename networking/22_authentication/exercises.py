# Module 22: Authentication - Exercises

# Tier 1: Recall
# 1. What HTTP header is typically used to transmit authentication credentials?
# TODO: Write your answer as a string in the variable `auth_header_name`.
auth_header_name = ""

# 2. Base64 encoding is a form of encryption. (True/False)
# TODO: Write your answer as a boolean in the variable `is_base64_encryption`.
is_base64_encryption = None


# Tier 2: Modify
import requests

def get_data_with_api_key(url, api_key):
    # TODO: Modify this function to send the API key in a custom header called "X-API-Key"
    # instead of the standard Authorization header.
    headers = {}
    response = requests.get(url, headers=headers)
    return response


# Tier 3: Build
def authenticate_and_fetch(login_url, data_url, username, password):
    # TODO: Build a function that first logs in to `login_url` using Basic Auth to get a token.
    # The login endpoint returns JSON like {"token": "abcdef"}.
    # Then, use that token as a Bearer token to fetch data from `data_url`.
    # Return the response object from the `data_url` request.
    pass


# Tier 4: Debug
def flawed_bearer_auth(url, token):
    # TODO: This function has a bug that will cause the server to reject the authentication.
    # Identify and fix the bug.
    headers = {
        "Authorization": f"token {token}"
    }
    return requests.get(url, headers=headers)
