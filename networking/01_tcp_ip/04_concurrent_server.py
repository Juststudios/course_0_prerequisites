"""
04_concurrent_server.py
=======================
Multi-client concurrent TCP server demonstrating thread-safe connection pooling,
worker threading, and message broadcast.

Demonstrates:
- Multi-client connection concurrency
- Thread-safe tracking of active client sessions
- Length-prefixed framing across concurrent threads
- Broadcast messaging to all connected peers
- Clean server and client disconnection handling
"""

import socket
import struct
import threading
import time
from typing import Optional, Tuple, Set, Dict


class ConcurrentTCPServer:
    """
    A concurrent multi-client TCP server supporting concurrent bidirectional
    messaging and broadcast capabilities across active connections.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0, timeout: float = 0.5):
        self.host = host
        self.requested_port = port
        self.timeout = timeout
        self._server_sock: Optional[socket.socket] = None
        self._bound_port: int = 0
        self._is_running = threading.Event()

        # Thread-safe client registry
        self._lock = threading.Lock()
        self._clients: Dict[socket.socket, Tuple[str, int]] = {}
        self.total_connections = 0
        self.total_messages_received = 0

    @property
    def port(self) -> int:
        return self._bound_port

    @property
    def active_client_count(self) -> int:
        with self._lock:
            return len(self._clients)

    def start(self) -> int:
        """Initializes and binds the listening socket."""
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.settimeout(self.timeout)
        self._server_sock.bind((self.host, self.requested_port))
        self._bound_port = self._server_sock.getsockname()[1]
        self._server_sock.listen(128)
        self._is_running.set()
        return self._bound_port

    def broadcast(self, message: bytes, sender: Optional[socket.socket] = None) -> int:
        """
        Broadcasts a framed message to all connected clients except the optional sender.
        Returns the number of recipients successfully sent to.
        """
        frame = struct.pack("!I", len(message)) + message
        sent_count = 0
        with self._lock:
            active_socks = list(self._clients.keys())

        for client_sock in active_socks:
            if client_sock is sender:
                continue
            try:
                client_sock.sendall(frame)
                sent_count += 1
            except (ConnectionResetError, BrokenPipeError, OSError):
                # Disconnection handled in client worker thread
                pass
        return sent_count

    def _handle_client_thread(self, client_sock: socket.socket, client_addr: Tuple[str, int]) -> None:
        """Dedicated worker thread handling communications for a single client."""
        with self._lock:
            self._clients[client_sock] = client_addr
            self.total_connections += 1

        client_sock.settimeout(1.0)
        try:
            while self._is_running.is_set():
                # Read 4-byte frame length
                hdr = self._recv_exact(client_sock, 4)
                if not hdr or len(hdr) < 4:
                    break

                (length,) = struct.unpack("!I", hdr)
                payload = self._recv_exact(client_sock, length)
                if not payload or len(payload) < length:
                    break

                with self._lock:
                    self.total_messages_received += 1

                # If payload starts with "BROADCAST:", broadcast to other peers
                if payload.startswith(b"BROADCAST:"):
                    broadcast_body = payload[len(b"BROADCAST:"):]
                    self.broadcast(b"[Broadcast from " + str(client_addr[1]).encode() + b"]: " + broadcast_body, sender=client_sock)
                    # Echo back acknowledgment
                    reply = struct.pack("!I", 14) + b"BROADCAST_SENT"
                    client_sock.sendall(reply)
                else:
                    # Echo back to sender
                    reply = struct.pack("!I", len(payload)) + payload
                    client_sock.sendall(reply)

        except (socket.timeout, ConnectionResetError, BrokenPipeError):
            pass
        finally:
            with self._lock:
                if client_sock in self._clients:
                    del self._clients[client_sock]
            try:
                client_sock.close()
            except OSError:
                pass

    @staticmethod
    def _recv_exact(sock: socket.socket, n_bytes: int) -> Optional[bytes]:
        buf = bytearray()
        while len(buf) < n_bytes:
            try:
                chunk = sock.recv(n_bytes - len(buf))
                if not chunk:
                    return None
                buf.extend(chunk)
            except (socket.timeout, OSError):
                return None
        return bytes(buf)

    def serve_forever(self) -> None:
        """Main accept loop dispatching each accepted connection to a thread."""
        if not self._is_running.is_set():
            self.start()

        while self._is_running.is_set():
            try:
                client_sock, client_addr = self._server_sock.accept()
                worker = threading.Thread(
                    target=self._handle_client_thread,
                    args=(client_sock, client_addr),
                    daemon=True,
                )
                worker.start()
            except socket.timeout:
                continue
            except OSError:
                break

    def stop(self) -> None:
        """Stops accept loop and closes all client sockets and the listening socket."""
        self._is_running.clear()
        with self._lock:
            for sock in list(self._clients.keys()):
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    sock.close()
                except OSError:
                    pass
            self._clients.clear()

        if self._server_sock:
            try:
                self._server_sock.close()
            except OSError:
                pass


def run_demo() -> None:
    print("=" * 60)
    print("CONCURRENT TCP SERVER DEMO")
    print("=" * 60)
    server = ConcurrentTCPServer(port=0)
    port = server.start()
    print(f"[*] Concurrent Server listening on 127.0.0.1:{port}")

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Simulate 3 concurrent clients
    def client_worker(client_id: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
        msg = f"Client {client_id} Hello".encode()
        frame = struct.pack("!I", len(msg)) + msg
        sock.sendall(frame)

        # Read reply
        hdr = sock.recv(4)
        (length,) = struct.unpack("!I", hdr)
        reply = sock.recv(length)
        print(f"  Client {client_id} received reply: {reply.decode()}")
        time.sleep(0.05)
        sock.close()

    threads = [threading.Thread(target=client_worker, args=(i,)) for i in range(1, 4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    time.sleep(0.1)
    print(f"[*] Total connections handled: {server.total_connections}")
    server.stop()


if __name__ == "__main__":
    run_demo()
