"""
03_requests_and_httpx.py
========================
Modern HTTP clients comparison: requests vs httpx (synchronous and asynchronous).

Demonstrates:
- requests.Session connection pooling and persistent headers
- Query parameters and JSON payloads
- Status code handling and raise_for_status()
- Timeout management and exception handling
- httpx.Client (sync) and httpx.AsyncClient (asyncio)
- High-throughput parallel requests using asyncio.gather
- Standalone runnable demo with local ephemeral server
"""

import asyncio
import threading
import time
from typing import List, Dict, Any
import requests
import httpx


def demonstrate_requests(base_url: str) -> None:
    """Demonstrates requests.Session and connection pooling."""
    print("\n--- 1. Synchronous HTTP with `requests` ---")

    # Using a Session maintains a connection pool and reuses TCP sockets
    with requests.Session() as session:
        session.headers.update({"User-Agent": "PearlNetworking/1.0", "X-Client-Type": "Worker"})

        # GET request with query params
        resp = session.get(f"{base_url}/api/items", params={"status": "active"}, timeout=3.0)
        resp.raise_for_status()  # Raises HTTPError if status is 4xx/5xx
        print(f"  GET /api/items -> Status: {resp.status_code}")
        data = resp.json()
        print(f"  Items found: {len(data.get('items', []))}")

        # POST request with JSON
        payload = {"name": "Hydraulic Pressure Transducer", "status": "active"}
        resp_post = session.post(f"{base_url}/api/items", json=payload, timeout=3.0)
        resp_post.raise_for_status()
        print(f"  POST /api/items -> Created item ID: {resp_post.json().get('id')}")

        # Handling 404 cleanly
        resp_404 = session.get(f"{base_url}/api/items/9999", timeout=3.0)
        if resp_404.status_code == 404:
            print(f"  GET non-existent item returned expected 404 Not Found")


def demonstrate_httpx_sync(base_url: str) -> None:
    """Demonstrates synchronous httpx.Client."""
    print("\n--- 2. Synchronous HTTP with `httpx.Client` ---")
    with httpx.Client(base_url=base_url, timeout=3.0) as client:
        resp = client.get("/health")
        print(f"  GET /health -> Status: {resp.status_code} | Body: {resp.json()}")


async def demonstrate_httpx_async(base_url: str) -> None:
    """Demonstrates high-throughput asynchronous HTTP with `httpx.AsyncClient`."""
    print("\n--- 3. Asynchronous Concurrent HTTP with `httpx.AsyncClient` ---")

    async with httpx.AsyncClient(base_url=base_url, timeout=5.0) as client:
        # Define an async fetch task
        async def fetch_item(item_id: int) -> Dict[str, Any]:
            res = await client.get(f"/api/items/{item_id}")
            if res.status_code == 200:
                return res.json()
            return {"id": item_id, "status": "not_found"}

        # Launch 5 concurrent fetch tasks simultaneously
        print("  Launching 5 concurrent asynchronous requests...")
        start_time = time.perf_counter()
        tasks = [fetch_item(i) for i in [1, 2, 3, 99, 100]]
        results = await asyncio.gather(*tasks)
        elapsed = (time.perf_counter() - start_time) * 1000

        print(f"  Completed {len(results)} concurrent async calls in {elapsed:.2f} ms")
        for item in results:
            print(f"    Item: {item}")


def run_demo() -> None:
    print("=" * 60)
    print("MODERN HTTP CLIENTS (REQUESTS & HTTPX) DEMO")
    print("=" * 60)

    from pathlib import Path
    import importlib.util

    # Start local PythonHTTPServer on ephemeral port
    server_path = Path(__file__).resolve().parent / "02_python_http_server.py"
    spec = importlib.util.spec_from_file_location("http_server_mod", server_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    server = mod.PythonHTTPServer(port=0)
    port = server.start()
    base_url = f"http://127.0.0.1:{port}"
    print(f"[*] Local test server active at {base_url}")

    try:
        demonstrate_requests(base_url)
        demonstrate_httpx_sync(base_url)
        asyncio.run(demonstrate_httpx_async(base_url))
    finally:
        server.stop()
        print("[*] Test server shutdown.")


if __name__ == "__main__":
    run_demo()
