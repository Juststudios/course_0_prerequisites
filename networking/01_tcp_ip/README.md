# Module 1: TCP/IP & Socket Programming

## 1. Overview & Transport Layer Roles

The Transport Layer is responsible for logical communication between application processes running on different hosts. While the Network Layer (IP) provides host-to-host delivery, the Transport Layer extends this to process-to-process delivery using **port numbers**.

In this module, you will learn the foundational concepts and system calls that power all internet communication:
- Low-level Berkeley sockets API (`socket`, `bind`, `listen`, `accept`, `connect`, `sendall`, `recv`, `close`).
- The TCP stream abstraction vs. UDP datagrams.
- Message framing (solving the "packet fragmentation / concatenation" problem).
- Socket configuration options (`SO_REUSEADDR`, `TCP_NODELAY`).
- Concurrency architectures for network servers.

---

## 2. OSI vs. TCP/IP: The Transport Perspective

At the Transport Layer:
- **TCP (Transmission Control Protocol - RFC 9293)** provides reliable, ordered, error-checked, flow-controlled, and congestion-controlled byte streams.
- **UDP (User Datagram Protocol - RFC 768)** provides lightweight, connectionless, unreliable datagram delivery with zero handshake latency.

```
+--------------------------------------------------------------------+
|                         Application Layer                          |
|             (HTTP, SSH, DNS, gRPC, Custom Binary)                  |
+---------------------------------+----------------------------------+
                                  |
                +-----------------+-----------------+
                |                                   |
+---------------v------------------+  +-------------v----------------+
|               TCP                |  |             UDP              |
|  - Connection-oriented           |  |  - Connectionless           |
|  - Reliable byte stream          |  |  - Unreliable datagram       |
|  - 3-way handshake               |  |  - No handshake              |
|  - Flow & Congestion Control     |  |  - Fire and forget           |
|  - Headers: 20-60 bytes          |  |  - Headers: 8 bytes          |
+---------------+------------------+  +-------------+----------------+
                |                                   |
                +-----------------+-----------------+
                                  |
+---------------------------------v----------------------------------+
|                            IP Layer                                |
|                 (Routing, IPv4 / IPv6 Packets)                     |
+--------------------------------------------------------------------+
```

---

## 3. TCP 3-Way Handshake & 4-Way Teardown

Before any application bytes can be exchanged over TCP, a full duplex connection must be established via the 3-Way Handshake:

```
Client                                     Server
  │                                          │  1. socket() -> bind() -> listen()
  │                                          │     (Server enters LISTEN state)
  │  1. connect()                            │
  │     Sends [SYN, Seq=x]                   │
  │  ───────────────────────────────────────►│  2. accept() unblocks
  │     (Client enters SYN_SENT)             │     Sends [SYN-ACK, Seq=y, Ack=x+1]
  │                                          │     (Server enters SYN_RCVD)
  │  3. Sends [ACK, Seq=x+1, Ack=y+1]        │
  │     (Client enters ESTABLISHED)          │
  │  ───────────────────────────────────────►│  Connection ESTABLISHED
  │                                          │
```

### Connection Teardown (4-Way Handshake)
TCP connections are bidirectional (two independent simplex streams). Each direction must be closed independently:
1. `Client -> Server`: `FIN (seq=u)` (Client will send no more data; enters `FIN_WAIT_1`).
2. `Server -> Client`: `ACK (ack=u+1)` (Server acknowledges client close; enters `CLOSE_WAIT`; Client enters `FIN_WAIT_2`).
3. `Server -> Client`: `FIN (seq=v)` (Server finishes sending remaining data and closes its half; enters `LAST_ACK`).
4. `Client -> Server`: `ACK (ack=v+1)` (Client acknowledges server close; enters `TIME_WAIT` for 2MSL ~ 60s before fully closing).

---

## 4. Berkeley Socket Programming Primitives

In Python, the `socket` standard library provides direct access to OS-level socket system calls:

```python
import socket

# 1. Create socket (IPv4, TCP stream)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Set socket options (Allow immediate reuse of local address in TIME_WAIT)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. Bind to interface and port (port 0 = let OS pick an available ephemeral port)
sock.bind(('127.0.0.1', 8080))

# 4. Listen for incoming connections (backlog queue size)
sock.listen(128)

# 5. Accept connection (blocks until client connects, returns new socket + address)
client_sock, client_addr = sock.accept()

# 6. Read and Write data
data = client_sock.recv(4096)        # Read up to 4096 bytes
client_sock.sendall(b"Hello World") # Guaranteed to send all bytes

# 7. Close connections
client_sock.close()
sock.close()
```

---

## 5. The Stream Framing Problem

A critical mental model: **TCP is a byte stream, not a message protocol**.
TCP has no concept of "messages", "packets", or boundaries. If a client executes:
```python
sock.sendall(b"Message 1")
sock.sendall(b"Message 2")
```
The server might receive this in a single `recv()` call (`b"Message 1Message 2"`), or across three `recv()` calls (`b"Mess"`, `b"age 1Mes"`, `b"sage 2"`).

### Standard Framing Solutions
1. **Delimiter-based Framing**: Separate messages with a unique sentinel (e.g., `\n`, `\r\n\r\n`, or `\0`). Simple for ASCII protocols, requires escaping if delimiter appears in payload.
2. **Length-Prefix Framing**: Prepend each message with a fixed-width binary header specifying the payload byte length (e.g., a 4-byte big-endian unsigned integer `!I` via `struct.pack`). Robust for arbitrary binary payloads.
3. **Fixed-Size Framing**: Every message is exactly $N$ bytes long, padded with zeros if necessary.

---

## 6. TCP vs. UDP: Comprehensive Comparison

| Feature | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|---|---|---|
| **Connection** | Connection-oriented (Handshake required) | Connectionless (No handshake) |
| **Reliability** | Guaranteed delivery (Retransmission) | Best effort (Packets may be dropped) |
| **Ordering** | Guaranteed in-order arrival | Packets may arrive out of order |
| **Boundary** | Continuous byte stream (No message boundary) | Preserves discrete datagram boundaries |
| **Flow Control** | Yes (Receiver sliding window) | No (Receiver buffer can overrun) |
| **Congestion Control** | Yes (Slow start, congestion avoidance) | No (Applications must implement) |
| **Header Overhead** | 20 to 60 bytes | 8 bytes |
| **Ideal Use Cases** | Web (HTTP), File transfer, SSH, DB queries | Video streaming, DNS, VoIP, Online games, Sensor telemetry |

---

## 7. Crucial Socket Options

- **`SO_REUSEADDR`**: Allows a socket to bind to an address/port that is currently in `TIME_WAIT` state. Essential for network servers to restart without waiting 1–2 minutes.
  ```python
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  ```
- **`TCP_NODELAY`**: Disables Nagle's algorithm. Nagle's algorithm buffers small outgoing packets to minimize TCP header overhead, which introduces up to 200ms latency for interactive protocols or real-time ML inference queries.
  ```python
  sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
  ```
- **Socket Timeouts**: Prevents `recv()` or `accept()` from hanging indefinitely when a client freezes or drops offline.
  ```python
  sock.settimeout(5.0)  # 5 second timeout
  ```

---

## 8. Server Concurrency Architectures

1. **Iterative Server**: Handles one client to completion before calling `accept()` for the next. Extremely simple, but blocks all other clients during long requests.
2. **Multi-Threaded Server**: Spawns a new `threading.Thread` for every accepted client socket. Straightforward to write, but thread creation overhead and memory limits scale poorly beyond ~1,000 clients.
3. **Thread Pool Server**: Uses a bounded `concurrent.futures.ThreadPoolExecutor` to service accepted connections, shielding the server from thread exhaustion.
4. **Asynchronous / Non-blocking Server**: Uses OS multiplexing (`select`, `poll`, `epoll`, `asyncio`) on non-blocking sockets. A single event loop thread can manage 50,000+ active connections with minimal memory overhead.

---

## 9. Common Pitfalls & How to Avoid Them

1. **The `send()` vs. `sendall()` Trap**: `sock.send()` is not guaranteed to send all bytes! It returns the number of bytes actually written. Always use `sock.sendall()`, or implement a loop tracking bytes sent.
2. **The Partial `recv()` Assumption**: Assuming `recv(1024)` returns the entire message. In reality, `recv()` returns whatever bytes are currently in the OS buffer (from 1 byte up to the buffer limit). Always read until your framing condition is satisfied.
3. **Address In Use Error (`EADDRINUSE`)**: Occurs when restarting a server whose previous port is in `TIME_WAIT`. Always set `SO_REUSEADDR`.
4. **Socket Leaks**: Forgetting to close client sockets in `finally` blocks, exhausting available file descriptors (`ulimit -n`). Always use context managers or structured `try...finally: sock.close()`.
