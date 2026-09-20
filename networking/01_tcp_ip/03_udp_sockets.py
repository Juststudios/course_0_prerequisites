"""
03_udp_sockets.py
=================
Demonstration of connectionless UDP (User Datagram Protocol) socket programming.

Demonstrates:
- UDP socket creation (AF_INET, SOCK_DGRAM)
- Connectionless datagram exchange (sendto, recvfrom)
- Preservation of message boundaries (unlike TCP streams)
- Ephemeral port binding
- Simulating telemetry stream ingestion with loss tolerance
"""

import json
import socket
import threading
import time
from typing import Optional, Tuple, Dict, Any, List


class UDPServer:
    """
    A lightweight, connectionless UDP server suitable for high-throughput
    sensor telemetry and metric collection.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0, timeout: float = 1.0):
        self.host = host
        self.requested_port = port
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._bound_port: int = 0
        self._is_running = threading.Event()
        self.received_datagrams: List[Dict[str, Any]] = []

    @property
    def port(self) -> int:
        return self._bound_port

    def start(self) -> int:
        """Binds the UDP socket to host:port."""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(self.timeout)
        self._sock.bind((self.host, self.requested_port))
        self._bound_port = self._sock.getsockname()[1]
        self._is_running.set()
        return self._bound_port

    def serve_forever(self, max_packets: Optional[int] = None) -> None:
        """Main listening loop for incoming datagrams."""
        if not self._is_running.is_set():
            self.start()

        while self._is_running.is_set():
            if max_packets is not None and len(self.received_datagrams) >= max_packets:
                break
            try:
                # In UDP, recvfrom returns (data, sender_address)
                # Datagram boundaries are strictly preserved up to 65535 bytes
                data, addr = self._sock.recvfrom(65535)
                try:
                    payload = json.loads(data.decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    payload = {"raw": data.hex()}

                record = {"sender": addr, "payload": payload, "timestamp": time.time()}
                self.received_datagrams.append(record)

                # Send an optional acknowledgment or status reply back to sender
                ack = json.dumps({"status": "ACK", "seq": payload.get("seq", 0)}).encode("utf-8")
                self._sock.sendto(ack, addr)

            except socket.timeout:
                continue
            except OSError:
                break

    def stop(self) -> None:
        """Stops the UDP server and closes the socket."""
        self._is_running.clear()
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass


class UDPClient:
    """
    A lightweight UDP client for streaming metrics or sensor telemetry.
    """

    def __init__(self, target_host: str = "127.0.0.1", target_port: int = 8080, timeout: float = 2.0):
        self.target_host = target_host
        self.target_port = target_port
        self.timeout = timeout
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(self.timeout)

    def send_telemetry(self, sensor_id: str, value: float, seq: int) -> Optional[Dict[str, Any]]:
        """
        Sends a single telemetry datagram and optionally awaits an ACK.
        """
        packet = json.dumps({
            "sensor_id": sensor_id,
            "value": value,
            "seq": seq,
            "timestamp": time.time()
        }).encode("utf-8")

        self._sock.sendto(packet, (self.target_host, self.target_port))

        try:
            ack_data, _ = self._sock.recvfrom(1024)
            return json.loads(ack_data.decode("utf-8"))
        except (socket.timeout, json.JSONDecodeError):
            return None

    def close(self) -> None:
        self._sock.close()


def run_demo() -> None:
    print("=" * 60)
    print("UDP TELEMETRY DEMO")
    print("=" * 60)
    server = UDPServer(port=0)
    port = server.start()
    print(f"[*] UDP Server listening on 127.0.0.1:{port}")

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    client = UDPClient(target_host="127.0.0.1", target_port=port)
    print("[*] Streaming 5 telemetry packets over UDP...")
    for seq in range(1, 6):
        ack = client.send_telemetry(sensor_id="thermo_01", value=20.0 + seq * 0.5, seq=seq)
        print(f"  Sent seq={seq} -> Server ACK: {ack}")

    time.sleep(0.1)
    client.close()
    server.stop()
    print(f"[*] UDP Demo complete. Total datagrams received: {len(server.received_datagrams)}")


if __name__ == "__main__":
    run_demo()
