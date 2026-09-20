"""
exercises.py
============
Level 6 Networking — Module 2: HTTP Protocols & Clients
4-Tier Progressive Exercises:
- Tier 1: Recall & Protocol Mechanics
- Tier 2: Understanding & Debugging (Malformed HTTP Request Formats)
- Tier 3: Application (Resilient HTTP Client with Exponential Backoff & Jitter)
- Tier 4: Challenge (Lightweight HTTP Reverse Proxy & Request Router)
"""

import time
import random
from typing import Dict, Any, Optional, Callable
import requests

print("=" * 70)
print("LEVEL 6 NETWORKING — MODULE 2: HTTP PROTOCOLS EXERCISES")
print("=" * 70)

# ============================================================================
# TIER 1: RECALL & PROTOCOL MECHANICS
# ============================================================================
"""
Questions:
1. Which HTTP methods are classified as 'safe'? Which are 'idempotent'?
   Why is POST neither safe nor idempotent?
2. Why does HTTP/1.1 strictly mandate the 'Host' header?
3. What is the difference between a 401 Unauthorized and a 403 Forbidden status?
4. What is Head-of-Line (HoL) blocking in HTTP/1.1, and how does HTTP/2 solve it?
5. What is the purpose of the 'Connection: keep-alive' header?
"""

# Demo for Tier 1: Inspecting HTTP response headers and status codes
def demo_tier1():
    print("\n--- TIER 1 DEMO: HTTP Status Code Inspection ---")
    status_codes = {
        200: ("OK", "Standard successful HTTP request"),
        201: ("Created", "Resource was successfully created"),
        400: ("Bad Request", "Malformed syntax or invalid request format"),
        404: ("Not Found", "Resource URI could not be located"),
        422: ("Unprocessable Entity", "Semantic validation failed (Pydantic standard)"),
        500: ("Internal Server Error", "Generic unhandled server crash"),
    }
    for code, (reason, desc) in status_codes.items():
        print(f"  HTTP {code} {reason:<22} -> {desc}")

demo_tier1()


# ============================================================================
# TIER 2: UNDERSTANDING & DEBUGGING
# ============================================================================
"""
The raw HTTP request generator below contains 4 critical protocol formatting bugs:
- Bug 1: Uses LF ('\\n') instead of CRLF ('\\r\\n') as line terminators.
- Bug 2: Missing the mandatory HTTP/1.1 'Host' header.
- Bug 3: Calculates Content-Length using string character count instead of encoded byte length.
- Bug 4: Missing the mandatory empty line ('\\r\\n') separating headers from payload body.
"""

buggy_raw_http_generator = """
def format_bad_post_request(path, host, json_str):
    # Bug 1: \\n instead of \\r\\n
    # Bug 2: missing Host: header
    # Bug 3: len(json_str) != len(json_str.encode('utf-8')) if unicode is present
    # Bug 4: no blank line before body
    raw = f"POST {path} HTTP/1.1\\n"
    raw += f"Content-Type: application/json\\n"
    raw += f"Content-Length: {len(json_str)}\\n"
    raw += json_str
    return raw
"""

# Exercise 2 Starter:
def format_correct_http_post(path: str, host: str, body_bytes: bytes) -> bytes:
    """
    TODO for Student:
    Format an RFC 9112 compliant HTTP/1.1 POST request:
    1. Status line with POST <path> HTTP/1.1\\r\\n
    2. Host: <host>\\r\\n
    3. Content-Type: application/json\\r\\n
    4. Content-Length: <byte_len>\\r\\n
    5. Connection: close\\r\\n
    6. Empty line: \\r\\n
    7. Raw body_bytes
    """
    pass


# ============================================================================
# TIER 3: APPLICATION — RESILIENT HTTP CLIENT WITH EXPONENTIAL BACKOFF
# ============================================================================
class ResilientHTTPClient:
    """
    An HTTP client with automatic retry logic, exponential backoff, and jitter
    to withstand transient network failures and 503 Service Unavailable errors.
    """

    def __init__(self, max_retries: int = 3, base_backoff: float = 0.1, max_backoff: float = 2.0):
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff
        self.session = requests.Session()

    def get_with_retry(self, url: str, **kwargs) -> requests.Response:
        """
        TODO for Student:
        Execute GET request with retry loop:
        - Retry on requests.RequestException or HTTP 5xx responses.
        - Calculate backoff: t = min(max_backoff, base_backoff * 2^(attempt) + uniform(0, base_backoff)).
        - Do not retry on 4xx client errors (e.g., 400, 401, 404).
        - If all retries fail, re-raise the final exception or return final response.
        """
        pass

    def close(self):
        self.session.close()


# ============================================================================
# TIER 4: CHALLENGE — HTTP REVERSE PROXY & ROUTER
# ============================================================================
class SimpleReverseProxy:
    """
    A lightweight reverse proxy routing requests to target backend servers:
    - Matches path prefix to target backend URL.
    - Appends 'X-Forwarded-For' header.
    - Measures round-trip forwarding latency in milliseconds.
    """

    def __init__(self, route_table: Dict[str, str]):
        self.route_table = route_table  # e.g., {"/api/v1": "http://127.0.0.1:8001"}
        self.session = requests.Session()

    def forward_request(self, client_ip: str, path: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """
        TODO for Student:
        1. Find matching prefix in route_table.
        2. If no route matches, return {"status_code": 502, "error": "Bad Gateway"}.
        3. Forward request to backend URL + remaining path.
        4. Track latency.
        5. Return dict with {"status_code": resp.status_code, "latency_ms": elapsed, "data": resp.content}.
        """
        pass


if __name__ == "__main__":
    print("\n[!] Module 2 exercise templates loaded.")
    print("Refer to networking/solutions/http_solutions.py for complete reference implementations.")
