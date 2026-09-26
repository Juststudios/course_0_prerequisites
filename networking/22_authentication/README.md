# Authentication

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
