"""
02_python_http_server.py
========================
Production-style HTTP API server built with Python standard library http.server.
Demonstrates request routing, status codes, query parameter parsing, and JSON handling.

Demonstrates:
- http.server.HTTPServer and BaseHTTPRequestHandler
- do_GET and do_POST request handlers
- Parsing URL paths and query parameters via urllib.parse
- Reading POST body streams via self.rfile.read(content_length)
- Sending HTTP headers (Content-Type, Content-Length)
- In-memory thread-safe data store
- Ephemeral port 0 support
"""

import http.server
import json
import threading
import time
import urllib.parse
from typing import Dict, Any, Optional


class ItemDatabase:
    """Thread-safe in-memory item repository."""

    def __init__(self):
        self._lock = threading.Lock()
        self._items: Dict[int, Dict[str, Any]] = {
            1: {"id": 1, "name": "Temperature Sensor", "status": "active"},
            2: {"id": 2, "name": "Vibration Sensor", "status": "active"},
        }
        self._next_id = 3

    def get_all(self) -> list:
        with self._lock:
            return list(self._items.values())

    def get(self, item_id: int) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._items.get(item_id)

    def create(self, name: str, status: str = "active") -> Dict[str, Any]:
        with self._lock:
            item = {"id": self._next_id, "name": name, "status": status}
            self._items[self._next_id] = item
            self._next_id += 1
            return item


# Global database instance for request handler
DB = ItemDatabase()


class SimpleRESTRequestHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP request handler with REST-style JSON endpoints."""

    def _send_json_response(self, status_code: int, data: Any) -> None:
        """Helper to send JSON response with correct headers."""
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_error_json(self, status_code: int, message: str) -> None:
        self._send_json_response(status_code, {"error": message, "status": status_code})

    def log_message(self, format: str, *args: Any) -> None:
        """Silence default stderr request logging in test/demo runs."""
        pass

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if path == "/health":
            self._send_json_response(200, {"status": "ok", "timestamp": time.time()})
            return

        if path == "/api/items":
            items = DB.get_all()
            # Optional query filter: ?status=active
            if "status" in query_params:
                filter_status = query_params["status"][0]
                items = [item for item in items if item.get("status") == filter_status]
            self._send_json_response(200, {"items": items, "count": len(items)})
            return

        if path.startswith("/api/items/"):
            parts = path.strip("/").split("/")
            if len(parts) == 3 and parts[2].isdigit():
                item_id = int(parts[2])
                item = DB.get(item_id)
                if item:
                    self._send_json_response(200, item)
                else:
                    self._send_error_json(404, f"Item with id {item_id} not found")
                return

        self._send_error_json(404, f"Endpoint {path} not found")

    def do_POST(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/items":
            content_length_str = self.headers.get("Content-Length")
            if not content_length_str:
                self._send_error_json(400, "Missing Content-Length header")
                return

            try:
                length = int(content_length_str)
                body_bytes = self.rfile.read(length)
                payload = json.loads(body_bytes.decode("utf-8"))
            except (ValueError, json.JSONDecodeError):
                self._send_error_json(400, "Invalid JSON payload")
                return

            if "name" not in payload:
                self._send_error_json(422, "Field 'name' is required")
                return

            new_item = DB.create(name=payload["name"], status=payload.get("status", "active"))
            self._send_json_response(201, new_item)
            return

        self._send_error_json(404, f"Endpoint {path} not found")


class PythonHTTPServer:
    """Manages lifecycle of http.server.HTTPServer on an ephemeral port."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.server = http.server.HTTPServer((host, port), SimpleRESTRequestHandler)
        self.host, self.port = self.server.server_address
        self._thread: Optional[threading.Thread] = None

    def start(self) -> int:
        self._thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self._thread.start()
        return self.port

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        if self._thread:
            self._thread.join(timeout=1.0)


def run_demo() -> None:
    print("=" * 60)
    print("PYTHON HTTP.SERVER DEMO")
    print("=" * 60)
    import urllib.request

    server = PythonHTTPServer(port=0)
    port = server.start()
    base_url = f"http://127.0.0.1:{port}"
    print(f"[*] Native HTTP Server listening on {base_url}")

    # 1. GET /health
    with urllib.request.urlopen(f"{base_url}/health") as resp:
        print(f"  GET /health -> Status: {resp.status} | Data: {resp.read().decode()}")

    # 2. GET /api/items
    with urllib.request.urlopen(f"{base_url}/api/items") as resp:
        print(f"  GET /api/items -> Data: {resp.read().decode()}")

    # 3. POST /api/items
    req = urllib.request.Request(
        f"{base_url}/api/items",
        data=json.dumps({"name": "Acoustic Sensor", "status": "active"}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        print(f"  POST /api/items -> Status: {resp.status} | Created: {resp.read().decode()}")

    server.stop()
    print("[*] Server stopped cleanly.")


if __name__ == "__main__":
    run_demo()
