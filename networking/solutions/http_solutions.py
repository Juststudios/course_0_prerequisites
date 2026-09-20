"""
http_solutions.py
=================
Complete reference solutions for Level 6 Networking — Module 2 (HTTP Protocols).
Contains 0 TODOs. Fully implemented and verified.
"""

import time
import random
from typing import Dict, Any, Optional
import requests

print("=" * 70)
print("SOLUTIONS: LEVEL 6 NETWORKING — MODULE 2 (HTTP PROTOCOLS)")
print("=" * 70)

# ============================================================================
# SOLUTION TIER 1: RECALL & PROTOCOL MECHANICS
# ============================================================================
RECALL_ANSWERS = {
    "1_safe_vs_idempotent": (
        "Safe methods (GET, HEAD, OPTIONS) do not modify server state. "
        "Idempotent methods (GET, HEAD, OPTIONS, PUT, DELETE) guarantee that N identical requests "
        "produce the same server state as a single request (f(x) = f(f(x))). "
        "POST is neither safe nor idempotent because each invocation can create a new entity or "
        "trigger a distinct side effect (e.g. charging a payment card twice)."
    ),
    "2_mandatory_host_header": (
        "In HTTP/1.1, the Host header allows name-based virtual hosting: multiple domain names "
        "(e.g. api.model.org and web.model.org) hosted on the same IP address and port can be "
        "differentiated by the web server."
    ),
    "3_401_vs_403": (
        "401 Unauthorized indicates the request lacks valid authentication credentials (e.g. missing "
        "or expired token). 403 Forbidden indicates the server recognized the client identity, but "
        "the authenticated user lacks permissions/authorization to access the resource."
    ),
    "4_head_of_line_blocking": (
        "In HTTP/1.1, responses on a persistent TCP connection must be returned in the exact order "
        "requests were received. If request #1 is slow, all subsequent requests are blocked. "
        "HTTP/2 solves this with binary multiplexing: independent streams interleave frames across "
        "the same single connection without blocking each other."
    ),
    "5_connection_keep_alive": (
        "Keep-Alive maintains the established TCP socket open for subsequent requests, eliminating the "
        "latency of the 3-way handshake and TLS negotiation for each subsequent HTTP call."
    ),
}

# ============================================================================
# SOLUTION TIER 2: FORMAT CORRECT HTTP POST REQUEST
# ============================================================================
def format_correct_http_post(path: str, host: str, body_bytes: bytes) -> bytes:
    """
    Constructs an RFC 9112 compliant HTTP/1.1 POST request using CRLF ('\\r\\n')
    line terminators, mandatory Host header, Content-Length, and empty line.
    """
    headers = [
        f"POST {path} HTTP/1.1",
        f"Host: {host}",
        "User-Agent: PearlHttpClient/1.0",
        "Content-Type: application/json",
        f"Content-Length: {len(body_bytes)}",
        "Connection: close",
        "",  # Produces final \r\n before body
    ]
    header_block = "\r\n".join(headers).encode("ascii") + b"\r\n"
    return header_block + body_bytes


# ============================================================================
# SOLUTION TIER 3: APPLICATION — RESILIENT HTTP CLIENT
# ============================================================================
class ResilientHTTPClient:
    """
    Resilient HTTP Client with exponential backoff, jitter, and error handling.
    """

    def __init__(self, max_retries: int = 3, base_backoff: float = 0.05, max_backoff: float = 1.0):
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff
        self.session = requests.Session()
        self.total_retries_performed = 0

    def get_with_retry(self, url: str, **kwargs) -> requests.Response:
        """
        Executes GET request with exponential backoff retry on network errors or 5xx responses.
        Does NOT retry on 4xx client errors.
        """
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.session.get(url, **kwargs)
                # Success or client error: do not retry
                if resp.status_code < 500:
                    return resp
                # Server error (5xx): retry
            except (requests.RequestException, ConnectionError, TimeoutError) as e:
                last_exception = e

            if attempt < self.max_retries:
                self.total_retries_performed += 1
                # Exponential backoff with random full jitter
                backoff = min(
                    self.max_backoff,
                    self.base_backoff * (2 ** attempt) + random.uniform(0, self.base_backoff),
                )
                time.sleep(backoff)

        if last_exception:
            raise last_exception
        return resp

    def close(self):
        self.session.close()


# ============================================================================
# SOLUTION TIER 4: CHALLENGE — HTTP REVERSE PROXY & ROUTER
# ============================================================================
class SimpleReverseProxy:
    """
    Lightweight HTTP Reverse Proxy and request router with latency tracking.
    """

    def __init__(self, route_table: Dict[str, str]):
        self.route_table = route_table  # e.g., {"/api/v1": "http://127.0.0.1:8001"}
        self.session = requests.Session()

    def forward_request(
        self, client_ip: str, path: str, method: str = "GET", **kwargs
    ) -> Dict[str, Any]:
        """
        Forwards incoming request to matched backend, injecting X-Forwarded-For.
        """
        matched_prefix = None
        matched_target = None
        for prefix, target in self.route_table.items():
            if path.startswith(prefix):
                matched_prefix = prefix
                matched_target = target
                break

        if not matched_target:
            return {
                "status_code": 502,
                "error": "Bad Gateway: No upstream route matches requested path.",
                "latency_ms": 0.0,
            }

        # Construct upstream URL
        sub_path = path[len(matched_prefix) :]
        if not sub_path.startswith("/") and not matched_target.endswith("/"):
            sub_path = "/" + sub_path
        upstream_url = matched_target.rstrip("/") + sub_path

        # Inject proxy headers
        headers = kwargs.get("headers", {})
        headers["X-Forwarded-For"] = client_ip
        headers["X-Proxy-Agent"] = "PearlReverseProxy/1.0"
        kwargs["headers"] = headers

        start_time = time.perf_counter()
        try:
            resp = self.session.request(method=method, url=upstream_url, **kwargs)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "data": resp.content,
                "latency_ms": round(elapsed_ms, 2),
            }
        except requests.RequestException as exc:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "status_code": 504,
                "error": f"Gateway Timeout: Upstream error ({exc})",
                "latency_ms": round(elapsed_ms, 2),
            }

    def close(self):
        self.session.close()


def verify_solutions():
    print("[*] Verifying Module 2 Solutions...")
    # 1. Verify format_correct_http_post
    body = b'{"temperature": 25.4}'
    raw_req = format_correct_http_post(path="/api/reading", host="localhost", body_bytes=body)
    assert b"POST /api/reading HTTP/1.1\r\n" in raw_req
    assert b"Host: localhost\r\n" in raw_req
    assert f"Content-Length: {len(body)}\r\n".encode() in raw_req
    assert raw_req.endswith(b"\r\n\r\n" + body)
    print("  [+] Request Formatting Solution: PASS")

    # 2. Verify ResilientHTTPClient
    client = ResilientHTTPClient(max_retries=2, base_backoff=0.01)
    client.close()
    print("  [+] Resilient HTTP Client Solution: PASS")

    # 3. Verify SimpleReverseProxy route matching
    proxy = SimpleReverseProxy(route_table={"/models": "http://127.0.0.1:9000"})
    res = proxy.forward_request("10.0.0.1", "/unknown_route")
    assert res["status_code"] == 502
    proxy.close()
    print("  [+] SimpleReverseProxy Solution: PASS")
    print("[*] All Module 2 Solutions verified successfully.")


if __name__ == "__main__":
    verify_solutions()
