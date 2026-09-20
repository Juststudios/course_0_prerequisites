"""
exercises.py
============
Level 6 Networking — Module 1: TCP/IP & Socket Programming
4-Tier Progressive Exercises:
- Tier 1: Recall & Core Mechanics
- Tier 2: Understanding & Debugging
- Tier 3: Application (Heartbeat Health Monitor)
- Tier 4: Challenge (Topic-Based Pub/Sub TCP Broker)
"""

import socket
import struct
import threading
import time
from typing import Dict, List, Set, Optional, Tuple

print("=" * 70)
print("LEVEL 6 NETWORKING — MODULE 1: TCP/IP EXERCISES")
print("=" * 70)

# ============================================================================
# TIER 1: RECALL & CORE MECHANICS
# ============================================================================
"""
Questions:
1. What are the three TCP handshake segments, and what is the role of each?
2. Why is TCP considered a 'byte stream' rather than a 'message protocol'?
3. What causes the 'Address already in use' (EADDRINUSE) error on server restart,
   and which socket option prevents it?
4. What is the fundamental difference between socket.send() and socket.sendall()?
5. When should an engineer choose UDP over TCP for an ML telemetry system?
"""

# Demo for Tier 1: Inspecting socket family, type, and ephemeral binding
def demo_tier1():
    print("\n--- TIER 1 DEMO: Socket Primitives & Ephemeral Ports ---")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))  # Port 0 asks kernel for ephemeral port
    addr, port = s.getsockname()
    print(f"  Bound socket to interface {addr} on kernel-assigned port: {port}")
    s.close()

demo_tier1()


# ============================================================================
# TIER 2: UNDERSTANDING & DEBUGGING
# ============================================================================
"""
The function below contains 4 typical socket programming bugs:
- Bug 1: Lack of SO_REUSEADDR causes EADDRINUSE on immediate restart.
- Bug 2: sock.send() used instead of sendall(), risking partial write.
- Bug 3: sock.recv(1024) assumes entire message arrives in single chunk (no framing).
- Bug 4: Socket is leaked on exception because close() is not in a finally block.

Task: Review the buggy code and understand how the fixed version addresses each bug.
"""

buggy_server_code = """
def buggy_echo_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', port))  # Bug 1: No SO_REUSEADDR
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(1024)        # Bug 3: Assumes full message fits in one recv
    conn.send(data)               # Bug 2: send() instead of sendall()
    conn.close()
    s.close()                     # Bug 4: Leaks if exception occurs
"""

# Exercise 2 Starter:
def fixed_echo_exchange(host: str, port: int, payload: bytes) -> bytes:
    """
    TODO for Student:
    Implement a safe, single-message exchange between client and server:
    1. Set SO_REUSEADDR.
    2. Use 4-byte length-prefix framing (!I).
    3. Use sendall() for complete transmission.
    4. Read exact payload length in a loop.
    5. Cleanly close sockets in finally blocks.
    """
    # Student implements this or tests against reference solutions
    pass


# ============================================================================
# TIER 3: APPLICATION — HEARTBEAT HEALTH MONITOR
# ============================================================================
class HeartbeatServer:
    """
    Server that monitors heartbeat pings from connected clients.
    If a client fails to send a heartbeat within `timeout_seconds`,
    the server marks the client as DISCONNECTED/DEAD.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0, timeout_seconds: float = 2.0):
        self.host = host
        self.requested_port = port
        self.timeout_seconds = timeout_seconds
        self.port: int = 0
        self.client_last_seen: Dict[str, float] = {}
        self.dead_clients: Set[str] = set()
        self.is_running = False

    def start(self) -> int:
        """TODO: Initialize socket, bind, listen, record port, and return port."""
        pass

    def process_ping(self, client_id: str) -> str:
        """TODO: Update client_last_seen with current time and return 'PONG'."""
        pass

    def check_health(self) -> List[str]:
        """
        TODO: Compare (time.time() - last_seen) with timeout_seconds.
        Return list of client_ids newly detected as dead.
        """
        pass

    def stop(self):
        """TODO: Clean shutdown."""
        pass


class HeartbeatClient:
    """
    Client that connects to HeartbeatServer and regularly sends PING messages.
    """

    def __init__(self, server_host: str, server_port: int, client_id: str):
        self.server_host = server_host
        self.server_port = server_port
        self.client_id = client_id
        self.sock: Optional[socket.socket] = None

    def connect(self):
        """TODO: Connect socket to server."""
        pass

    def send_ping(self) -> str:
        """TODO: Send 'PING:<client_id>' and receive 'PONG' response."""
        pass

    def close(self):
        """TODO: Clean close."""
        pass


# ============================================================================
# TIER 4: CHALLENGE — TOPIC-BASED PUB/SUB TCP BROKER
# ============================================================================
class PubSubBroker:
    """
    A lightweight, in-memory Pub/Sub TCP broker.
    Protocol:
      SUB <topic>         -> Subscribes the client socket to <topic>. Response: 'OK:SUB'
      PUB <topic> <msg>   -> Publishes <msg> to all subscribers of <topic>. Response: 'OK:PUB <count>'
      UNSUB <topic>       -> Unsubscribes from <topic>. Response: 'OK:UNSUB'
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.requested_port = port
        self.port: int = 0
        self.subscriptions: Dict[str, Set[socket.socket]] = {}
        self.lock = threading.Lock()
        self.is_running = False

    def start(self) -> int:
        """TODO: Bind to port, start server accept loop."""
        pass

    def handle_command(self, client_sock: socket.socket, command_line: str) -> str:
        """
        TODO: Parse command line and execute SUB, PUB, or UNSUB.
        Return string response.
        """
        pass

    def stop(self):
        """TODO: Clean shutdown of all sockets."""
        pass


if __name__ == "__main__":
    print("\n[!] Module 1 exercise templates loaded.")
    print("Refer to networking/solutions/tcp_ip_solutions.py for complete reference implementations.")
