"""
02_tcp_client.py
================
Robust TCP Client implementation with chunked reception, timeouts,
framing handling, and context manager support.

Demonstrates:
- Client socket creation and connection
- Configurable connect and read timeouts
- Loop-based buffered reading to guarantee complete message assembly
- Length-prefix framing support
- Context manager protocol (__enter__, __exit__)
- Resilient error handling (socket.timeout, ConnectionRefusedError)
"""

import socket
import struct
import time
from typing import Optional, List


class TCPClient:
    """
    A robust TCP Client demonstrating connection management, framed send/receive,
    and timeout handling.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8080, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None

    def connect(self) -> None:
        """Establishes connection to the target server."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect((self.host, self.port))
            self._sock = sock
        except Exception:
            sock.close()
            self._sock = None
            raise

    def is_connected(self) -> bool:
        """Returns True if the socket exists and is not closed."""
        return self._sock is not None and self._sock.fileno() != -1

    def send_framed(self, data: bytes) -> None:
        """
        Sends data using 4-byte big-endian length-prefix framing.
        """
        if not self.is_connected():
            raise ConnectionError("Cannot send: client is not connected.")
        header = struct.pack("!I", len(data))
        self._sock.sendall(header + data)

    def recv_framed(self) -> bytes:
        """
        Reads a length-prefixed message from the socket.
        Guarantees complete message reception despite stream chunking.
        """
        if not self.is_connected():
            raise ConnectionError("Cannot receive: client is not connected.")

        # Read 4-byte length prefix
        header = self._recv_exact(4)
        if not header or len(header) < 4:
            raise ConnectionError("Server closed connection while waiting for frame header.")

        (length,) = struct.unpack("!I", header)
        if length == 0:
            return b""

        # Read payload
        payload = self._recv_exact(length)
        if not payload or len(payload) < length:
            raise ConnectionError(f"Server closed connection after {len(payload or b'')} of {length} bytes.")
        return payload

    def send_and_receive(self, data: bytes) -> bytes:
        """Convenience method to send a framed request and await framed response."""
        self.send_framed(data)
        return self.recv_framed()

    def _recv_exact(self, n_bytes: int) -> bytes:
        """Helper to read exactly n_bytes from the stream."""
        buffer = bytearray()
        while len(buffer) < n_bytes:
            chunk = self._sock.recv(n_bytes - len(buffer))
            if not chunk:
                break
            buffer.extend(chunk)
        return bytes(buffer)

    def close(self) -> None:
        """Closes the socket connection."""
        if self._sock:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                self._sock.close()
                self._sock = None

    def __enter__(self) -> "TCPClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


def run_demo() -> None:
    print("=" * 60)
    print("TCP CLIENT DEMO")
    print("=" * 60)
    import threading
    from pathlib import Path
    import sys

    import importlib.util
    server_path = Path(__file__).resolve().parent / "01_tcp_server.py"
    spec = importlib.util.spec_from_file_location("tcp_server_mod", server_path)
    tcp_server_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tcp_server_mod)

    server = tcp_server_mod.TCPEchoServer(port=0)
    bound_port = server.start()
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    print(f"[*] Started background test server on port {bound_port}")

    # Use client via context manager
    with TCPClient(host="127.0.0.1", port=bound_port) as client:
        test_messages = [
            b"Hello from TCPClient",
            b"Testing chunked reception",
            b"JSON telemetry payload: {'temperature': 23.5, 'pressure': 101.3}",
        ]
        for msg in test_messages:
            response = client.send_and_receive(msg)
            print(f"  Sent: {msg.decode()[:40]}... -> Echoed: {response.decode()[:40]}...")
            assert response == msg, "Echo mismatch!"

    server.stop()
    print("[*] TCP Client test completed successfully!")


if __name__ == "__main__":
    # Note: when executed directly, import with standard syntax
    import importlib.util
    from pathlib import Path
    import threading

    server_path = Path(__file__).resolve().parent / "01_tcp_server.py"
    spec = importlib.util.spec_from_file_location("tcp_server_mod", server_path)
    tcp_server_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tcp_server_mod)

    server = tcp_server_mod.TCPEchoServer(port=0)
    port = server.start()
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    with TCPClient(port=port) as client:
        res = client.send_and_receive(b"Verified TCPClient")
        print(f"Verified: {res.decode()}")

    server.stop()
