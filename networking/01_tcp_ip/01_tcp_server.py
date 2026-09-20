"""
01_tcp_server.py
================
Foundational TCP Echo and Messaging Server using Python's Berkeley socket API.

Demonstrates:
- Socket creation (AF_INET, SOCK_STREAM)
- Socket options (SO_REUSEADDR)
- Binding to host and port (including ephemeral port 0)
- Listening with backlog queue
- Connection acceptance loop
- Message framing (length-prefix and delimiter-based)
- Graceful shutdown handling
"""

import socket
import struct
import threading
import time
from typing import Optional, Tuple


class TCPEchoServer:
    """
    A robust TCP Echo Server demonstrating socket primitives, length-prefixed
    message framing, and graceful shutdown handling.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0, timeout: float = 1.0):
        self.host = host
        self.requested_port = port
        self.timeout = timeout
        self._server_sock: Optional[socket.socket] = None
        self._is_running = threading.Event()
        self._bound_port: int = 0
        self.connections_handled = 0
        self.messages_echoed = 0

    @property
    def port(self) -> int:
        """Returns the actual bound port (crucial when port=0 is requested)."""
        return self._bound_port

    def start(self) -> int:
        """
        Creates, configures, binds, and starts listening on the socket.
        Returns the bound port.
        """
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow immediate reuse of the port in TIME_WAIT state
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Set a timeout so accept() doesn't block indefinitely during shutdown
        self._server_sock.settimeout(self.timeout)

        self._server_sock.bind((self.host, self.requested_port))
        self._bound_port = self._server_sock.getsockname()[1]
        self._server_sock.listen(128)
        self._is_running.set()
        return self._bound_port

    def handle_client(self, client_sock: socket.socket, client_addr: Tuple[str, int]) -> None:
        """
        Handles a single client connection using length-prefix framing.
        Protocol:
            [4 bytes: big-endian uint32 payload_length][payload bytes]
        """
        client_sock.settimeout(self.timeout)
        try:
            while self._is_running.is_set():
                # Step 1: Read 4-byte header
                header = self._recv_exact(client_sock, 4)
                if not header:
                    # Client closed connection cleanly
                    break

                (payload_len,) = struct.unpack("!I", header)
                if payload_len == 0:
                    continue

                # Step 2: Read payload of exactly payload_len bytes
                payload = self._recv_exact(client_sock, payload_len)
                if not payload:
                    break

                # Echo payload back with identical length-prefix framing
                response = struct.pack("!I", len(payload)) + payload
                client_sock.sendall(response)
                self.messages_echoed += 1

        except (socket.timeout, ConnectionResetError, BrokenPipeError):
            pass
        finally:
            client_sock.close()
            self.connections_handled += 1

    @staticmethod
    def _recv_exact(sock: socket.socket, n_bytes: int) -> Optional[bytes]:
        """
        Reads exactly n_bytes from a stream socket.
        Solves the TCP stream fragmentation problem.
        """
        data = bytearray()
        while len(data) < n_bytes:
            try:
                chunk = sock.recv(n_bytes - len(data))
                if not chunk:
                    # Connection closed before receiving expected bytes
                    return None if len(data) == 0 else bytes(data)
                data.extend(chunk)
            except (socket.timeout, OSError):
                return None
        return bytes(data)

    def serve_forever(self, max_connections: Optional[int] = None) -> None:
        """
        Main server accept loop. Runs until stop() is called or max_connections reached.
        """
        if not self._is_running.is_set():
            self.start()

        while self._is_running.is_set():
            if max_connections is not None and self.connections_handled >= max_connections:
                break
            try:
                client_sock, client_addr = self._server_sock.accept()
                self.handle_client(client_sock, client_addr)
            except socket.timeout:
                # Expected timeout to check if self._is_running is still set
                continue
            except OSError:
                # Socket closed during shutdown
                break

    def stop(self) -> None:
        """Signals the server loop to stop and cleans up socket descriptors."""
        self._is_running.clear()
        if self._server_sock:
            try:
                self._server_sock.close()
            except OSError:
                pass


def run_demo() -> None:
    print("=" * 60)
    print("TCP ECHO SERVER DEMO")
    print("=" * 60)
    server = TCPEchoServer(host="127.0.0.1", port=0)
    port = server.start()
    print(f"[*] Server listening on 127.0.0.1:{port}")

    # Start server in background thread
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    # Create a test client to verify communication
    print("[*] Connecting client to test server...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))

    messages = [b"Hello, TCP!", b"Testing length-prefix framing", b"Final packet"]
    for msg in messages:
        # Pack length + data
        packet = struct.pack("!I", len(msg)) + msg
        client.sendall(packet)

        # Receive length
        hdr = client.recv(4)
        (rlen,) = struct.unpack("!I", hdr)
        echoed = client.recv(rlen)
        print(f"  Sent: {msg.decode()} | Received: {echoed.decode()}")

    client.close()
    server.stop()
    print(f"[*] Server stopped cleanly. Handled: {server.connections_handled} connection(s).")


if __name__ == "__main__":
    run_demo()
