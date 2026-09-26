import os

module_dir = "/home/settings/Documents/pearl/networking/22_authentication"

readme_content = """# Authentication

## What You Will Learn
In this module, you will learn the fundamentals of authentication in networking and APIs. You will understand how clients prove their identity to servers using various methods, such as Basic Authentication, Bearer Tokens, and API Keys. You will also learn the difference between authentication and authorization.

## Prerequisites
- Basic understanding of HTTP methods (GET, POST).
- Knowledge of HTTP headers.
- Familiarity with the concepts of clients and servers.

## Key Terminology
- **Authentication (AuthN):** The process of verifying *who* you are.
- **Authorization (AuthZ):** The process of verifying *what* you are allowed to do.
- **Credentials:** The information used to prove identity (e.g., username/password).
- **Token:** A piece of data that acts as a temporary credential (e.g., JWT).
- **Basic Auth:** An HTTP authentication scheme that transmits credentials as a base64-encoded string.
- **Bearer Token:** A token that gives the "bearer" (the one holding it) access to a resource.

## The Problem
APIs and web services expose valuable data and actions. If anyone can access an API without proving who they are, bad actors can steal data, impersonate users, or abuse resources. The server needs a reliable, secure way to verify the identity of the client making a request.

## How It Works
Authentication typically involves the client sending credentials along with their request, usually in the HTTP headers. The server inspects these credentials, checks them against a database or identity provider, and either accepts the request (200 OK) or rejects it (401 Unauthorized).

## Intuition
Think of a nightclub. Authentication is the bouncer checking your ID at the door to verify you are who you say you are and are old enough to enter. Authorization is the VIP pass that dictates whether you can go to the regular dance floor or the exclusive VIP lounge.

## Technical Explanation
The most common way to authenticate HTTP requests is via the `Authorization` header.
- **Basic Auth:** The header looks like `Authorization: Basic <base64(username:password)>`. It's simple but insecure unless used over HTTPS.
- **Bearer Tokens:** The header looks like `Authorization: Bearer <token_string>`. The token is usually obtained via a separate login request and has an expiration time.
- **API Keys:** Sometimes sent in a custom header (e.g., `X-API-Key: <key>`), a query parameter, or the Authorization header. They are static strings assigned to a developer or application.

When the server receives the request, it extracts the credentials from the header and validates them. If valid, the request proceeds. If not, it returns a `401 Unauthorized` status code.

## Example
If you want to access a protected profile endpoint, your HTTP request might look like this:

```http
GET /api/profile HTTP/1.1
Host: api.example.com
Authorization: Bearer abcdef123456
```

## Python Implementation
```python
import requests

def get_protected_data_basic(url, username, password):
    # requests handles the base64 encoding and Authorization header for us
    response = requests.get(url, auth=(username, password))
    return response

def get_protected_data_bearer(url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

if __name__ == "__main__":
    # Example usage (URLs are fictional)
    # basic_resp = get_protected_data_basic("https://api.example.com/basic", "admin", "secret")
    # bearer_resp = get_protected_data_bearer("https://api.example.com/bearer", "my_secret_token")
    pass
```

## What Happens Underneath
1. The client code formats the credentials according to the chosen scheme.
2. The HTTP client library serializes this into the HTTP headers.
3. The request is transmitted over the network (hopefully encrypted via TLS/HTTPS).
4. The server's web framework parses the incoming bytes, extracts the header, and passes it to an authentication middleware.
5. The middleware validates the credentials (e.g., by hashing a password and comparing it to a DB, or cryptographically verifying a token).

## Common Mistakes
- **Hardcoding credentials:** Never commit passwords or API keys in your source code. Use environment variables.
- **Using Basic Auth over HTTP:** Base64 is encoding, not encryption. If you use Basic Auth without HTTPS, anyone sniffing the network can read your password in plain text.
- **Confusing AuthN with AuthZ:** Just because someone is authenticated doesn't mean they should have access to *everything*. Always check permissions (AuthZ) after verifying identity (AuthN).

## Security Considerations
- Always use HTTPS to protect credentials in transit.
- Store secrets securely using environment variables or secret managers (e.g., AWS Secrets Manager, HashiCorp Vault).
- Implement rate limiting on login endpoints to prevent brute-force attacks.
- Ensure tokens have a reasonable expiration time to minimize damage if stolen.

## Real-World Applications
- **GitHub API:** Uses Personal Access Tokens (Bearer tokens) to authenticate developers interacting with repositories.
- **Stripe API:** Uses API Keys sent via Basic Auth (where the username is the API key and password is empty).
- **OAuth2 Login:** "Login with Google/Facebook" uses tokens to authenticate users without sharing their passwords with the third-party app.

## AI-Agent Connection
AI agents interacting with external APIs (e.g., calling a weather API or a database) must securely manage and provide authentication credentials. Understanding how to properly format HTTP Authorization headers allows an agent to seamlessly bridge different authenticated systems.

## Exercises
Complete the exercises in `exercises.py`.

## Challenge
Implement a mock server using the built-in `http.server` that requires a specific Bearer token. Then, write a client script to authenticate against it.

## Summary
Authentication is the foundational security layer for networked applications. By securely passing credentials like Basic Auth details or Bearer tokens via HTTP headers over HTTPS, clients can reliably prove their identity to servers.

## What You Should Know Before Moving On
- The difference between Authentication and Authorization.
- How to construct an `Authorization` header for Basic and Bearer auth.
- Why HTTPS is mandatory when transmitting credentials.
"""

exercises_content = """# Module 22: Authentication - Exercises

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
"""

solutions_content = """# Module 22: Authentication - Solutions

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
"""

impl_content = """import requests
import base64

def manual_basic_auth(username, password):
    \"\"\"Demonstrates how basic auth headers are constructed manually.\"\"\"
    credentials = f"{username}:{password}"
    # Base64 encode the string
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    return headers

def mock_request():
    headers = manual_basic_auth("admin", "secret")
    print("Generated Headers:", headers)
    # response = requests.get("https://api.example.com/protected", headers=headers)
    # return response

if __name__ == "__main__":
    mock_request()
"""

with open(os.path.join(module_dir, "README.md"), "w") as f:
    f.write(readme_content)

with open(os.path.join(module_dir, "exercises.py"), "w") as f:
    f.write(exercises_content)

with open(os.path.join(module_dir, "solutions.py"), "w") as f:
    f.write(solutions_content)

with open(os.path.join(module_dir, "auth_example.py"), "w") as f:
    f.write(impl_content)

print("Module 22 generated successfully.")
