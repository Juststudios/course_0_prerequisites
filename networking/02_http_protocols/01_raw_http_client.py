"""
01_raw_http_client.py
=====================
A from-scratch HTTP/1.1 client implemented entirely on raw TCP sockets (no requests,
no urllib). Demonstrates exact protocol serialization, headers framing, and response parsing.

Demonstrates:
- Constructing RFC 9112 compliant HTTP/1.1 request bytes
- Sending over raw AF_INET, SOCK_STREAM TCP socket
- Reading and parsing status lines (HTTP/1.1 200 OK)
- Parsing key-value headers into dictionaries
- Reading content bodies delimited by Content-Length or Connection: close
- Self-contained local server test harness using ephemeral port 0
"""

import socket
import threading
import time
from typing import Dict, Tuple, Optional, Any


class HTTPResponse:
    """Represents a parsed HTTP response."""

    def __init__(self, status_code: int, status_message: str, headers: Dict[str, str], body: bytes):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers
        self.body = body

    @property
    def text(self) -> str:
        """Decodes body as UTF-8 string."""
        return self.body.decode("utf-8", errors="replace")

    def __repr__(self) -> str:
        return f"<HTTPResponse [{self.status_code} {self.status_message}] len={len(self.body)}>"


class RawHTTPClient:
    """
    HTTP/1.1 client operating directly over raw Berkeley TCP sockets.
    """

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def request(
        self,
        method: str,
        host: str,
        port: int,
        path: str = "/",
        headers: Optional[Dict[str, str]] = None,
        body: bytes = b"",
    ) -> HTTPResponse:
        """
        Executes a complete HTTP request over a raw TCP socket.
        """
        if headers is None:
            headers = {}

        # Ensure mandatory HTTP/1.1 headers
        req_headers = {
            "Host": f"{host}:{port}",
            "User-Agent": "RawHTTPClient/1.0",
            "Connection": "close",  # Instruct server to close after response to simplify reading
            "Accept": "*/*",
        }
        req_headers.update(headers)

        if body and "Content-Length" not in req_headers:
            req_headers["Content-Length"] = str(len(body))

        # 1. Format request line and headers
        request_lines = [f"{method.upper()} {path} HTTP/1.1"]
        for key, val in req_headers.items():
            request_lines.append(f"{key}: {val}")
        request_lines.append("")  # Empty line demarcating end of headers

        header_bytes = "\r\n".join(request_lines).encode("ascii") + b"\r\n"
        full_request_data = header_bytes + body

        # 2. Connect via TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect((host, port))
            # 3. Transmit request
            sock.sendall(full_request_data)

            # 4. Read response until socket closes or headers+body are fully read
            raw_response = bytearray()
            while True:
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    raw_response.extend(chunk)
                except socket.timeout:
                    break
        finally:
            sock.close()

        # 5. Parse raw response
        return self._parse_response(bytes(raw_response))

    def get(self, host: str, port: int, path: str = "/", headers: Optional[Dict[str, str]] = None) -> HTTPResponse:
        return self.request("GET", host, port, path, headers=headers)

    def post(
        self, host: str, port: int, path: str = "/", headers: Optional[Dict[str, str]] = None, body: bytes = b""
    ) -> HTTPResponse:
        return self.request("POST", host, port, path, headers=headers, body=body)

    @staticmethod
    def _parse_response(data: bytes) -> HTTPResponse:
        """
        Parses raw bytes into an HTTPResponse object.
        """
        if not data:
            raise ConnectionError("Empty response received from server.")

        # Split headers and body at CRLF CRLF
        header_end = data.find(b"\r\n\r\n")
        if header_end == -1:
            header_end = data.find(b"\n\n")
            delimiter_len = 2
        else:
            delimiter_len = 4

        if header_end == -1:
            raw_headers = data
            body = b""
        else:
            raw_headers = data[:header_end]
            body = data[header_end + delimiter_len :]

        lines = raw_headers.decode("iso-8859-1").splitlines()
        if not lines:
            raise ValueError("Malformed HTTP response: no status line.")

        # Parse status line: HTTP/1.1 200 OK
        status_line_parts = lines[0].split(" ", 2)
        if len(status_line_parts) < 2:
            raise ValueError(f"Malformed status line: {lines[0]}")

        status_code = int(status_line_parts[1])
        status_message = status_line_parts[2] if len(status_line_parts) > 2 else ""

        # Parse headers
        headers: Dict[str, str] = {}
        for line in lines[1:]:
            if ":" in line:
                name, val = line.split(":", 1)
                headers[name.strip().lower()] = val.strip()

        # Handle Content-Length truncation if specified
        if "content-length" in headers:
            try:
                expected_len = int(headers["content-length"])
                body = body[:expected_len]
            except ValueError:
                pass

        return HTTPResponse(status_code, status_message, headers, body)


# ============================================================================
# Self-Contained Local Demonstration Harness
# ============================================================================
def _run_mock_http_server(port_container: list, stop_event: threading.Event):
    """Simple raw TCP server that speaks HTTP/1.1 on an ephemeral port."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("127.0.0.1", 0))
    server_sock.listen(5)
    server_sock.settimeout(0.5)
    port_container.append(server_sock.getsockname()[1])

    while not stop_event.is_set():
        try:
            client, _ = server_sock.accept()
            req = client.recv(4096).decode("utf-8", errors="replace")
            # Simple routing
            if "GET /health" in req:
                body = b'{"status": "healthy", "service": "telemetry_gateway"}'
                resp = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: application/json\r\n"
                    b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                    b"Connection: close\r\n\r\n" + body
                )
            elif "POST /echo" in req:
                body_start = req.find("\r\n\r\n") + 4
                post_body = req[body_start:].encode("utf-8")
                resp = (
                    b"HTTP/1.1 201 Created\r\n"
                    b"Content-Type: text/plain\r\n"
                    b"Content-Length: " + str(len(post_body)).encode() + b"\r\n"
                    b"Connection: close\r\n\r\n" + post_body
                )
            else:
                body = b"Not Found"
                resp = (
                    b"HTTP/1.1 404 Not Found\r\n"
                    b"Content-Length: 9\r\n"
                    b"Connection: close\r\n\r\nNot Found"
                )
            client.sendall(resp)
            client.close()
        except socket.timeout:
            continue
        except OSError:
            break
    server_sock.close()


def run_demo() -> None:
    print("=" * 60)
    print("RAW HTTP/1.1 CLIENT OVER TCP DEMO")
    print("=" * 60)

    port_holder = []
    stop_event = threading.Event()
    t = threading.Thread(target=_run_mock_http_server, args=(port_holder, stop_event), daemon=True)
    t.start()
    time.sleep(0.1)

    port = port_holder[0]
    print(f"[*] Mock HTTP server listening on port {port}")

    client = RawHTTPClient()

    # 1. Test GET /health
    print("[*] Executing GET /health via raw TCP socket...")
    resp = client.get(host="127.0.0.1", port=port, path="/health")
    print(f"  Response: {resp}")
    print(f"  Status: {resp.status_code} {resp.status_message}")
    print(f"  Content-Type: {resp.headers.get('content-type')}")
    print(f"  Body: {resp.text}")
    assert resp.status_code == 200

    # 2. Test POST /echo
    print("[*] Executing POST /echo with payload...")
    payload = b"Hello from Raw Socket HTTP Client!"
    resp2 = client.post(host="127.0.0.1", port=port, path="/echo", body=payload)
    print(f"  Response: {resp2}")
    print(f"  Body: {resp2.text}")
    assert resp2.status_code == 201
    assert resp2.body == payload

    stop_event.set()
    t.join(timeout=1.0)
    print("[*] Raw HTTP Client demonstration completed successfully!")


if __name__ == "__main__":
    run_demo()
