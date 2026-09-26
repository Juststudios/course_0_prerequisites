import os

module_dir = "/home/settings/Documents/pearl/networking/25_http_client_architecture"

readme_content = """# HTTP Client Architecture

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
"""

exercises_content = """# Module 25: HTTP Client Architecture - Exercises

# Tier 1: Recall
# 1. What object in the `requests` library allows you to persist settings (like headers) and TCP connections across multiple requests?
# TODO: Write your answer as a string.
persistent_object = ""

# 2. What does DTO stand for?
# TODO: Write your answer as a string.
dto_meaning = ""


# Tier 2: Modify
class SimpleClient:
    def __init__(self, token):
        self.token = token
        
    def get_data(self):
        # TODO: Modify this method to use a requests Session instead of making a one-off request.
        # You will need to add a Session to the __init__ method.
        import requests
        return requests.get("https://api.example.com/data", headers={"Auth": self.token})


# Tier 3: Build
class GitHubRepoClient:
    # TODO: Build a client that initializes a requests.Session with a base URL of "https://api.github.com".
    # Add a method `get_repo(owner, repo_name)` that makes a GET request to `/repos/{owner}/{repo_name}`
    # and returns the JSON dictionary.
    pass


# Tier 4: Debug
class BuggyApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        import requests
        self.session = requests.Session()

    def make_request(self, endpoint):
        # TODO: This method has a bug that will cause URL formation errors (e.g. missing slashes or double slashes).
        # Fix the URL joining logic to be robust regardless of whether base_url ends with a slash or endpoint begins with one.
        
        # Buggy code:
        url = self.base_url + endpoint
        return self.session.get(url).json()
"""

solutions_content = """# Module 25: HTTP Client Architecture - Solutions

# Tier 1: Recall
persistent_object = "Session"
dto_meaning = "Data Transfer Object"

# Tier 2: Modify
import requests

class SimpleClient:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Auth": self.token})
        
    def get_data(self):
        # Fix: Use the initialized session
        return self.session.get("https://api.example.com/data")

# Tier 3: Build
class GitHubRepoClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github.v3+json"})

    def get_repo(self, owner, repo_name):
        url = f"{self.base_url}/repos/{owner}/{repo_name}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

# Tier 4: Debug
class BuggyApiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/') # Clean trailing slashes
        import requests
        self.session = requests.Session()

    def make_request(self, endpoint):
        # Fix: Clean leading slashes to ensure consistent joining
        clean_endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{clean_endpoint}"
        return self.session.get(url).json()
"""

impl_content = """import requests
from typing import Optional

class BaseClient:
    \"\"\"A robust base client handling sessions, timeouts, and errors.\"\"\"
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def request(self, method: str, path: str, params: Optional[dict] = None, json_data: Optional[dict] = None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        
        # Centralized timeout config
        response = self.session.request(
            method, 
            url, 
            params=params, 
            json=json_data,
            timeout=(3.0, 10.0) # 3s connect timeout, 10s read timeout
        )
        
        response.raise_for_status()
        return response.json()

class TodoClient(BaseClient):
    \"\"\"Specific implementation for a Todo API.\"\"\"
    def get_todo(self, todo_id: int):
        return self.request("GET", f"/todos/{todo_id}")
        
    def create_todo(self, title: str, completed: bool = False):
        return self.request("POST", "/todos", json_data={"title": title, "completed": completed})

if __name__ == "__main__":
    # Example usage against jsonplaceholder
    client = TodoClient(base_url="https://jsonplaceholder.typicode.com", api_key="dummy_key")
    
    print("Fetching todo 1...")
    todo = client.get_todo(1)
    print(todo)
"""

with open(os.path.join(module_dir, "README.md"), "w") as f:
    f.write(readme_content)

with open(os.path.join(module_dir, "exercises.py"), "w") as f:
    f.write(exercises_content)

with open(os.path.join(module_dir, "solutions.py"), "w") as f:
    f.write(solutions_content)

with open(os.path.join(module_dir, "api_client.py"), "w") as f:
    f.write(impl_content)

print("Module 25 generated successfully.")
