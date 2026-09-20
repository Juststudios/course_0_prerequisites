"""
tcp_ip_solutions.py
===================
Complete reference solutions for Level 6 Networking — Module 1 (TCP/IP).
Contains 0 TODOs. Fully implemented and verified.
"""

import socket
import struct
import threading
import time
from typing import Dict, List, Set, Optional, Tuple

print("=" * 70)
print("SOLUTIONS: LEVEL 6 NETWORKING — MODULE 1 (TCP/IP)")
print("=" * 70)

# ============================================================================
# SOLUTION TIER 1: RECALL & CORE CONCEPTS
# ============================================================================
RECALL_ANSWERS = {
    "1_handshake_segments": (
        "1. SYN (Synchronize): Client sends initial sequence number (ISN_c) to request connection. "
        "2. SYN-ACK: Server acknowledges ISN_c+1 and sends its own sequence number (ISN_s). "
        "3. ACK: Client acknowledges ISN_s+1, moving both sockets to ESTABLISHED state."
    ),
    "2_byte_stream": (
        "TCP provides a continuous byte stream with no message boundaries. Packets may be segmented, "
        "merged, or fragmented by intermediate MTUs and OS socket buffers. Applications must implement "
        "framing (e.g. length-prefix or delimiters) to reconstruct distinct messages."
    ),
    "3_address_already_in_use": (
        "When a TCP connection closes, the initiating endpoint enters TIME_WAIT for 2MSL (~60s) to "
        "ensure lingering duplicate segments dissipate. Re-binding immediately fails with EADDRINUSE. "
        "Setting socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) bypasses this restriction."
    ),
    "4_send_vs_sendall": (
        "socket.send() is a non-blocking system call that may send only a portion of the byte buffer "
        "and returns the integer count sent. socket.sendall() is a high-level wrapper that repeatedly "
        "calls send() until all bytes are transmitted or an error occurs."
    ),
    "5_udp_vs_tcp_in_ml": (
        "UDP is preferred for high-frequency telemetry, heartbeats, or real-time streaming where low "
        "latency and minimal overhead matter more than 100% packet arrival (a lost ping is superseded "
        "by the next ping)."
    ),
}

# ============================================================================
# SOLUTION TIER 2: FIXED ECHO EXCHANGE
# ============================================================================
def fixed_echo_exchange(host: str, port: int, payload: bytes) -> bytes:
    """
    Executes a clean, framed exchange with a TCP server:
    1. Sets SO_REUSEADDR
    2. Sends length-prefixed packet (!I)
    3. Reads exact framed response
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(3.0)
    try:
        sock.connect((host, port))
        # Pack length header and payload
        header = struct.pack("!I", len(payload))
        sock.sendall(header + payload)

        # Read 4-byte response header
        raw_len = bytearray()
        while len(raw_len) < 4:
            chunk = sock.recv(4 - len(raw_len))
            if not chunk:
                raise ConnectionError("Server closed connection prematurely")
            raw_len.extend(chunk)

        (resp_len,) = struct.unpack("!I", raw_len)

        # Read exact response payload
        received = bytearray()
        while len(received) < resp_len:
            chunk = sock.recv(resp_len - len(received))
            if not chunk:
                raise ConnectionError("Server closed connection during payload read")
            received.extend(chunk)

        return bytes(received)
    finally:
        sock.close()


# ============================================================================
# SOLUTION TIER 3: APPLICATION — HEARTBEAT MONITOR
# ============================================================================
class HeartbeatServer:
    """Server that monitors heartbeat pings and detects dead clients."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0, timeout_seconds: float = 1.0):
        self.host = host
        self.requested_port = port
        self.timeout_seconds = timeout_seconds
        self.port: int = 0
        self.client_last_seen: Dict[str, float] = {}
        self.dead_clients: Set[str] = set()
        self.lock = threading.Lock()
        self._server_sock: Optional[socket.socket] = None
        self._is_running = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> int:
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.settimeout(0.5)
        self._server_sock.bind((self.host, self.requested_port))
        self.port = self._server_sock.getsockname()[1]
        self._server_sock.listen(16)
        self._is_running.set()

        self._thread = threading.Thread(target=self._serve_loop, daemon=True)
        self._thread.start()
        return self.port

    def _serve_loop(self):
        while self._is_running.is_set():
            try:
                conn, _ = self._server_sock.accept()
                worker = threading.Thread(target=self._handle_client, args=(conn,), daemon=True)
                worker.start()
            except (socket.timeout, OSError):
                continue

    def _handle_client(self, conn: socket.socket):
        conn.settimeout(1.0)
        try:
            while self._is_running.is_set():
                data = conn.recv(1024)
                if not data:
                    break
                text = data.decode("utf-8").strip()
                if text.startswith("PING:"):
                    client_id = text.split(":", 1)[1]
                    reply = self.process_ping(client_id)
                    conn.sendall(reply.encode("utf-8") + b"\n")
        except (socket.timeout, ConnectionResetError, BrokenPipeError):
            pass
        finally:
            conn.close()

    def process_ping(self, client_id: str) -> str:
        with self.lock:
            self.client_last_seen[client_id] = time.time()
            if client_id in self.dead_clients:
                self.dead_clients.remove(client_id)
        return "PONG"

    def check_health(self) -> List[str]:
        now = time.time()
        newly_dead = []
        with self.lock:
            for cid, last_time in self.client_last_seen.items():
                if now - last_time > self.timeout_seconds:
                    if cid not in self.dead_clients:
                        self.dead_clients.add(cid)
                        newly_dead.append(cid)
        return newly_dead

    def stop(self):
        self._is_running.clear()
        if self._server_sock:
            try:
                self._server_sock.close()
            except OSError:
                pass


class HeartbeatClient:
    """Client sending heartbeat pings to the server."""

    def __init__(self, server_host: str, server_port: int, client_id: str):
        self.server_host = server_host
        self.server_port = server_port
        self.client_id = client_id
        self.sock: Optional[socket.socket] = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2.0)
        self.sock.connect((self.server_host, self.server_port))

    def send_ping(self) -> str:
        if not self.sock:
            self.connect()
        msg = f"PING:{self.client_id}\n".encode("utf-8")
        self.sock.sendall(msg)
        resp = self.sock.recv(1024).decode("utf-8").strip()
        return resp

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None


# ============================================================================
# SOLUTION TIER 4: CHALLENGE — TOPIC-BASED PUB/SUB TCP BROKER
# ============================================================================
class PubSubBroker:
    """
    In-memory Topic-based Pub/Sub TCP Broker.
    Commands:
      SUB <topic>
      PUB <topic> <message>
      UNSUB <topic>
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.requested_port = port
        self.port: int = 0
        self.subscriptions: Dict[str, Set[socket.socket]] = {}
        self.lock = threading.Lock()
        self._server_sock: Optional[socket.socket] = None
        self._is_running = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> int:
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.settimeout(0.5)
        self._server_sock.bind((self.host, self.requested_port))
        self.port = self._server_sock.getsockname()[1]
        self._server_sock.listen(32)
        self._is_running.set()

        self._thread = threading.Thread(target=self._serve_loop, daemon=True)
        self._thread.start()
        return self.port

    def _serve_loop(self):
        while self._is_running.is_set():
            try:
                conn, _ = self._server_sock.accept()
                worker = threading.Thread(target=self._handle_client, args=(conn,), daemon=True)
                worker.start()
            except (socket.timeout, OSError):
                continue

    def _handle_client(self, conn: socket.socket):
        conn.settimeout(1.0)
        try:
            while self._is_running.is_set():
                data = conn.recv(4096)
                if not data:
                    break
                lines = data.decode("utf-8").strip().splitlines()
                for line in lines:
                    if line:
                        reply = self.handle_command(conn, line)
                        conn.sendall(reply.encode("utf-8") + b"\n")
        except (socket.timeout, ConnectionResetError, BrokenPipeError):
            pass
        finally:
            self._unsubscribe_all(conn)
            try:
                conn.close()
            except OSError:
                pass

    def handle_command(self, client_sock: socket.socket, command_line: str) -> str:
        parts = command_line.strip().split(" ", 2)
        if not parts:
            return "ERR:EMPTY_COMMAND"
        cmd = parts[0].upper()

        with self.lock:
            if cmd == "SUB" and len(parts) >= 2:
                topic = parts[1]
                if topic not in self.subscriptions:
                    self.subscriptions[topic] = set()
                self.subscriptions[topic].add(client_sock)
                return f"OK:SUB {topic}"

            elif cmd == "UNSUB" and len(parts) >= 2:
                topic = parts[1]
                if topic in self.subscriptions and client_sock in self.subscriptions[topic]:
                    self.subscriptions[topic].remove(client_sock)
                return f"OK:UNSUB {topic}"

            elif cmd == "PUB" and len(parts) >= 3:
                topic = parts[1]
                msg = parts[2]
                subscribers = list(self.subscriptions.get(topic, []))
                delivered = 0
                broadcast_packet = f"MSG {topic} {msg}\n".encode("utf-8")
                for sub_sock in subscribers:
                    try:
                        sub_sock.sendall(broadcast_packet)
                        delivered += 1
                    except OSError:
                        pass
                return f"OK:PUB {delivered}"

        return "ERR:UNKNOWN_COMMAND"

    def _unsubscribe_all(self, client_sock: socket.socket):
        with self.lock:
            for topic_set in self.subscriptions.values():
                topic_set.discard(client_sock)

    def stop(self):
        self._is_running.clear()
        if self._server_sock:
            try:
                self._server_sock.close()
            except OSError:
                pass


def verify_solutions():
    print("[*] Verifying Module 1 Solutions...")
    # 1. Verify Heartbeat
    hb_server = HeartbeatServer(port=0, timeout_seconds=0.3)
    port = hb_server.start()
    client = HeartbeatClient("127.0.0.1", port, "sensor_alpha")
    reply = client.send_ping()
    assert reply == "PONG", f"Expected PONG, got {reply}"
    time.sleep(0.5)
    dead = hb_server.check_health()
    assert "sensor_alpha" in dead, f"Expected sensor_alpha in dead list, got {dead}"
    client.close()
    hb_server.stop()
    print("  [+] Heartbeat Health Monitor Solution: PASS")

    # 2. Verify PubSubBroker
    broker = PubSubBroker(port=0)
    b_port = broker.start()

    sub_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sub_client.connect(("127.0.0.1", b_port))
    sub_client.sendall(b"SUB telemetry/vibration\n")
    sub_reply = sub_client.recv(1024).decode()
    assert "OK:SUB" in sub_reply

    pub_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pub_client.connect(("127.0.0.1", b_port))
    pub_client.sendall(b"PUB telemetry/vibration 4.2_RMS\n")
    pub_reply = pub_client.recv(1024).decode()
    assert "OK:PUB 1" in pub_reply

    broadcast_msg = sub_client.recv(1024).decode()
    assert "MSG telemetry/vibration 4.2_RMS" in broadcast_msg

    sub_client.close()
    pub_client.close()
    broker.stop()
    print("  [+] PubSubBroker Solution: PASS")
    print("[*] All Module 1 Solutions verified successfully.")


if __name__ == "__main__":
    verify_solutions()
