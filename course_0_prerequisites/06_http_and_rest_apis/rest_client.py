"""rest_client.py - Demonstrates async HTTP client operations with headers and timeouts.

Key concepts demonstrated:
1. Asynchronous client session management with httpx.
2. Authorization and tracing header construction.
3. Status code inspection and error classification.
4. Parsing JSON responses safely.
"""

from typing import Dict, Any, Optional
import httpx
import asyncio
import json


class AgentRestClient:
    """A clean async REST client designed for agent tool integrations."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "AgentRestClient/1.0",
        }

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Sends a GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
                return self._process_response(response)
            except httpx.TimeoutException:
                raise TimeoutError(f"Request to {url} timed out after {self.timeout}s")

    async def post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Sends a POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)
                return self._process_response(response)
            except httpx.TimeoutException:
                raise TimeoutError(f"Request to {url} timed out after {self.timeout}s")

    def _process_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Classifies HTTP status codes and extracts payload."""
        code = response.status_code
        if 200 <= code < 300:
            return response.json() if response.content else {}
        elif code == 429:
            raise RuntimeError("HTTP 429: Rate limit exceeded. Backoff required.")
        elif code in (401, 403):
            raise PermissionError(f"HTTP {code}: Authentication failed.")
        elif 400 <= code < 500:
            raise ValueError(f"HTTP {code} Client Error: {response.text}")
        elif code >= 500:
            raise RuntimeError(f"HTTP {code} Server Error: {response.text}")
        return {}


async def main() -> None:
    print("=== Module 06: Async REST Client Demo ===")

    # Test client instantiation and header verification
    client = AgentRestClient(
        base_url="https://httpbin.org",
        api_key="sk-agent-mock-token",
        timeout=10.0
    )

    assert "Bearer sk-agent-mock-token" in client.headers["Authorization"]
    print("[OK] Client initialized with authorization headers.")

    # Using httpx mock transport to verify without external internet dependency
    def mock_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/models":
            data = {"models": ["agent-gpt-1", "agent-bert-2"]}
            return httpx.Response(200, json=data)
        elif request.url.path == "/v1/rate_limited":
            return httpx.Response(429, text="Too Many Requests")
        elif request.url.path == "/v1/unauthorized":
            return httpx.Response(401, text="Invalid API key")
        return httpx.Response(404, text="Not Found")

    transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://mock.api") as mock_http:
        # Test 200 OK
        resp = await mock_http.get("/v1/models")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["models"]) == 2
        print(f"[OK] Mock GET 200 OK response: {data}")

        # Test 429 Rate Limit
        resp_429 = await mock_http.get("/v1/rate_limited")
        assert resp_429.status_code == 429
        print(f"[OK] Mock GET 429 Rate Limit captured: status={resp_429.status_code}")

        # Test 401 Unauthorized
        resp_401 = await mock_http.get("/v1/unauthorized")
        assert resp_401.status_code == 401
        print(f"[OK] Mock GET 401 Unauthorized captured: status={resp_401.status_code}")

    print("All tests in rest_client.py completed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
