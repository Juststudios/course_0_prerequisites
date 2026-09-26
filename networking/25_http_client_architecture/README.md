# HTTP Client Architecture

## What You Will Learn
In this module, you will learn how to design and architect robust HTTP clients. Instead of scattering `requests.get()` calls throughout your codebase, you will learn how to build modular, maintainable, and testable API wrapper classes.

## Prerequisites
- Familiarity with object-oriented programming in Python.
- Understanding of HTTP methods, headers, and authentication.
- Knowledge of error handling and retries.

## Key Terminology
- **API Wrapper:** A class or library that abstracts the raw HTTP calls to an API into native programming language methods.
- **Client Session:** A persistent connection context that holds shared configuration (like headers and cookies) across multiple requests.
- **Separation of Concerns:** A design principle dictating that code should be divided into distinct sections, each handling a specific piece of functionality.
- **Data Transfer Object (DTO):** An object used to encapsulate data and send it from one subsystem to another (often mapping JSON to Python dataclasses).

## The Problem
When developers start interacting with an API, they often write inline `requests.post()` calls directly inside their business logic. Over time, as authentication, logging, retries, and error handling are added, the business logic becomes tangled with networking code. Changing an API endpoint or adding a new header requires searching and updating dozens of files.

## How It Works
A well-architected HTTP client centralizes all network communication. It initializes a session, handles authentication, provides a unified error handling mechanism, and exposes clean, domain-specific methods (e.g., `get_user(id)`) instead of raw HTTP methods (e.g., `requests.get('/users/1')`).

## Intuition
Think of an HTTP Client Architecture like a translator at the United Nations. You (the business logic) speak Python. The API speaks HTTP and JSON. Instead of forcing your business logic to constantly hold a dictionary and translate every sentence, you hire a dedicated translator (the API Wrapper) who handles all the messy details of protocol, formatting, and delivery.

## Technical Explanation
A solid architecture typically involves:
1. **Base Client:** A class that wraps `requests.Session`. It handles the base URL, default headers (like Auth), retries, and timeout configurations. It implements a core `_request()` method that all other methods use.
2. **Endpoint Methods:** Methods on the client that map to specific API endpoints. They format parameters and URLs, call `_request()`, and parse the response.
3. **Model Parsing:** Converting the raw JSON dictionary returned by the API into structured Python objects (like Pydantic models or Dataclasses) for type safety.
4. **Custom Exceptions:** Defining domain-specific errors (e.g., `UserNotFoundError`) rather than letting raw `requests.exceptions.HTTPError` bubble up.

## Example
Instead of this:
```python
resp = requests.get(f"https://api.example.com/users/{user_id}", headers={"Auth": token})
user_name = resp.json()["name"]
```

You want this:
```python
client = ExampleApiClient(token="...")
user = client.get_user(user_id)
print(user.name)
```

## Python Implementation
```python
import requests
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class User:
    id: int
    name: str

class ApiError(Exception):
    pass

class BaseClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, timeout=10, **kwargs)
        
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise ApiError(f"API call failed: {e}")
            
        return response.json()

class UserClient(BaseClient):
    def get_user(self, user_id: int) -> User:
        data = self._request("GET", f"/users/{user_id}")
        return User(id=data["id"], name=data["name"])
```

## What Happens Underneath
By using `requests.Session`, the underlying `urllib3` connection pool keeps TCP connections alive (Keep-Alive). This drastically reduces latency for subsequent requests to the same host, as the TCP handshake and TLS negotiation are bypassed. The wrapper encapsulates this state, ensuring connections aren't wastefully created and destroyed.

## Common Mistakes
- **Not Using Sessions:** Using `requests.get()` instead of `session.get()` forces a new TCP connection every time.
- **Leaking HTTP Logic:** Returning the raw `requests.Response` object to the caller means the caller still has to know about HTTP status codes.
- **Hardcoding Base URLs:** Base URLs should be configurable via environment variables so you can easily switch between staging and production environments.

## Security Considerations
- The API wrapper is the central place to ensure secrets (like tokens) are securely injected and not logged.
- Centralized request logic allows you to easily implement request signing or header scrubbing for logging.

## Real-World Applications
- Almost every major SaaS company (Stripe, Twilio, AWS) provides SDKs built exactly on these principles.
- Internal microservice architectures use generated or hand-written API clients to communicate safely between services.

## AI-Agent Connection
When building AI tools, providing the LLM with a well-architected client interface (like `client.get_user(id)`) is far more reliable than asking the LLM to construct raw HTTP requests and handle JSON parsing itself. It abstracts away the fragility of network IO.

## Exercises
Complete the exercises in `exercises.py`.

## Challenge
Extend the `UserClient` in the Python implementation to include a `create_user(name: str)` method that sends a POST request, handles a 201 Created response, and returns the new `User` object.

## Summary
Architecting an HTTP client is about abstracting the messy details of network communication. By centralizing requests, using connection pools (Sessions), and returning typed objects instead of raw dictionaries, you create a robust, testable, and developer-friendly interface to any API.

## What You Should Know Before Moving On
- The benefits of using `requests.Session` over `requests.get`.
- How to separate HTTP plumbing from business logic.
- Why custom exceptions and data objects improve code maintainability.
