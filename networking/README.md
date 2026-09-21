# Level 6: Computer Networking Fundamentals & Systems Architecture

## Key Terminology
* **Client:** The program making the request.
* **Server:** The program answering the request.
* **HTTP:** The protocol for web communication.
* **Endpoint:** A specific URL where an API lives.



Welcome to **Level 6 Networking**. Modern software systems do not live in isolation. Whether deploying distributed machine learning microservices, streaming sensor telemetry from IoT edge devices, or building high-throughput cloud backends, engineers must understand how data traverses the physical and logical layers of modern computer networks.

This curriculum provides an applied, from-scratch foundation in computer networking designed specifically for engineers and machine learning practitioners.

---

## 1. Introduction: Why Networking Matters for Engineers & ML Practitioners

In modern computing, almost every significant application is a distributed system:
- **Model Inference & Serving**: ML models run in remote inference servers behind REST/gRPC gateways (e.g., Triton, TorchServe, FastAPI).
- **Distributed Training**: Large models are trained across multi-node GPU clusters coordinated via MPI, NCCL, and TCP/IP or InfiniBand interconnects.
- **Edge & IoT Telemetry**: Sensors stream millions of readings per second over UDP or MQTT to cloud ingestion pipelines.
- **Microservices & Cloud**: Containerized services interact over HTTP/1.1, HTTP/2, and HTTP/3 protocols with strict latency budgets (P95/P99 < 20ms).

Understanding socket primitives, protocol mechanics, buffer management, concurrency paradigms, and API architectures enables you to diagnose bottlenecks, prevent resource exhaustion (e.g., socket leaks, connection starvation), and build robust systems.

---

## 2. Fundamental Mental Models: Packet Switching & Encapsulation

### 2.1 Circuit Switching vs. Packet Switching
- **Circuit Switching** (traditional telephone network): A dedicated physical channel is reserved end-to-end for the duration of a session. Inefficient for bursty computer traffic.
- **Packet Switching** (the Internet): Data is chunked into discrete packets containing headers (metadata) and payload (data). Packets traverse independent routes across intermediate routers and switches, sharing bandwidth dynamically.

### 2.2 Encapsulation and Demultiplexing
As data flows down the protocol stack on the sender, each layer prepends a header (and sometimes appends a trailer). On the receiver, each layer strips its header and demultiplexes the payload to the next higher layer:

```
Sender (Encapsulation)                     Receiver (Demultiplexing)
┌────────────────────────────┐             ┌────────────────────────────┐
│ Application Data (Payload) │             │ Application Data (Payload) │
└─────────────┬──────────────┘             └─────────────▲──────────────┘
              │ Prepend HTTP/App header                  │
              ▼                                          │
┌────────────────────────────┐             ┌─────────────┴──────────────┐
│ TCP Header │  App Payload  │             │ TCP Header │  App Payload  │
└─────────────┬──────────────┘             └─────────────▲──────────────┘
              │ Prepend IP header (src/dst IP)           │ Demux via Port #
              ▼                                          │
┌────────────────────────────┐             ┌─────────────┴──────────────┐
│ IP Header  │  TCP Segment  │             │ IP Header  │  TCP Segment  │
└─────────────┬──────────────┘             └─────────────▲──────────────┘
              │ Prepend Frame header (src/dst MAC)       │ Demux via IP Protocol
              ▼                                          │
┌────────────────────────────┐             ┌─────────────┴──────────────┐
│ Ethernet   │   IP Packet   │   Frame     │ Ethernet   │   IP Packet   │
│ Header     │               │   Check     │ Header     │               │
└─────────────┬──────────────┴─────────┘   └─────────────▲──────────────┴───┘
              │ Physical Transmission                    │ Demux via EtherType
              ▼                                          │
═══════════════ Physical Medium (Bits over Copper/Fiber/Air) ═══════════════
```

---

## 3. The Layer Models: OSI 7-Layer vs. TCP/IP 4-Layer

Engineers frequently reference both models. The OSI (Open Systems Interconnection) reference model is conceptual; the TCP/IP stack is the practical protocol implementation used across the globe.

| OSI Layer | OSI Name | Functionality | TCP/IP Layer | Dominant Protocols | Data Unit |
|---|---|---|---|---|---|
| **7** | Application | Network processes to applications (user interface) | **Application** | HTTP, HTTPS, DNS, SSH, FTP, SMTP, gRPC | Message / Data |
| **6** | Presentation | Data representation, encryption, compression | | TLS/SSL, JSON, Protobuf, ASCII, JPEG | |
| **5** | Session | Interhost communication, session management | | Sockets, RPC, NetBIOS | |
| **4** | Transport | End-to-end connections, reliability, flow control | **Transport** | TCP, UDP, QUIC | Segment (TCP) / Datagram (UDP) |
| **3** | Network | Path determination, logical routing (IP addressing) | **Internet** | IPv4, IPv6, ICMP, BGP, OSPF | Packet |
| **2** | Data Link | Physical addressing (MAC), error detection on link | **Link** (Network Access) | Ethernet (802.3), Wi-Fi (802.11), ARP | Frame |
| **1** | Physical | Binary transmission across physical transmission medium | | Copper cables, Fiber optics, Radio waves | Bit |

---

## 4. Key Protocols in the Network Stack

- **IP (Internet Protocol - RFC 791 / RFC 8200)**: Unreliable, best-effort packet delivery across networks. Provides logical 32-bit (IPv4) or 128-bit (IPv6) addresses.
- **TCP (Transmission Control Protocol - RFC 9293)**: Connection-oriented, reliable, byte-stream protocol. Guarantees in-order delivery, retransmits lost packets, performs flow control (sliding window) and congestion control (CUBIC, BBR).
- **UDP (User Datagram Protocol - RFC 768)**: Connectionless, lightweight datagram protocol. Low latency, zero handshake, no retransmissions. Ideal for real-time video, gaming, DNS, and ML parameter server heartbeats.
- **TLS/SSL (Transport Layer Security - RFC 8446)**: Cryptographic protocol providing confidentiality, integrity, and mutual authentication over TCP.
- **HTTP/1.1 (RFC 9112)**: Textual request-response application protocol with persistent connections (Keep-Alive) and pipeline limitations (Head-of-Line blocking).
- **HTTP/2 (RFC 9113)**: Binary framing, multiplexing multiple streams over a single TCP connection, HPACK header compression.
- **HTTP/3 & QUIC (RFC 9000)**: Runs over UDP, eliminating TCP head-of-line blocking, zero-RTT connection resumption, native encryption.
- **WebSockets (RFC 6455)**: Full-duplex persistent bidirectional communication channel initiated via HTTP upgrade.
- **gRPC**: High-performance RPC framework using Protocol Buffers over HTTP/2, widely used for ML microservice mesh communication.

---

## 5. Transport Mechanics: Ports, Sockets, and Handshakes

### 5.1 Sockets and Port Numbers
A **Socket** is an OS abstraction representing an endpoint for communication, identified by a 5-tuple:
`{Protocol, Source IP, Source Port, Destination IP, Destination Port}`.

- **Well-known Ports (0–1023)**: Reserved for privileged system services (HTTP: 80, HTTPS: 443, SSH: 22, DNS: 53).
- **Registered Ports (1024–49151)**: Registered by software vendors (PostgreSQL: 5432, Redis: 6379, Uvicorn/FastAPI: 8000).
- **Dynamic / Ephemeral Ports (49152–65535)**: Allocated automatically by the OS kernel for client-side outgoing connections.
  *Testing Tip*: Specifying port `0` in `bind(('localhost', 0))` instructs the kernel to immediately assign a free ephemeral port, preventing address conflict errors during testing.

### 5.2 TCP 3-Way Handshake & 4-Way Teardown

```
Connection Establishment (3-Way Handshake)
Client                                    Server
  │                                         │ LISTEN
  │ ──── SYN (seq=x) ─────────────────────► │ SYN-RECEIVED
  │ ◄─── SYN-ACK (seq=y, ack=x+1) ───────── │
  │ ──── ACK (seq=x+1, ack=y+1) ──────────► │ ESTABLISHED
ESTABLISHED

Connection Teardown (4-Way Teardown)
Client                                    Server
  │ ──── FIN (seq=u) ─────────────────────► │ CLOSE-WAIT
FIN-WAIT-1                                  │
  │ ◄─── ACK (ack=u+1) ──────────────────── │
FIN-WAIT-2                                  │
  │ ◄─── FIN (seq=v) ────────────────────── │ LAST-ACK
TIME-WAIT ── ACK (ack=v+1) ───────────────► │ CLOSED
(wait 2MSL)
CLOSED
```

---

## 6. Application Layer: HTTP Semantics & REST Constraints

### 6.1 HTTP Request & Response Anatomy
Every HTTP/1.1 message consists of:
1. **Start Line**: Request Line (`METHOD /path HTTP/1.1`) or Status Line (`HTTP/1.1 200 OK`).
2. **Headers**: Key-value pairs separated by colons (`Content-Type: application/json`).
3. **Empty Line**: A mandatory `\r\n` demarcating header termination.
4. **Optional Body**: Binary or text payload (payload length defined by `Content-Length` or `Transfer-Encoding: chunked`).

### 6.2 The 6 REST Architectural Constraints (Roy Fielding)
1. **Client-Server Architecture**: Separation of user interface concerns from data storage concerns.
2. **Statelessness**: Every request from client to server must contain all information necessary to understand and process the request. No session state is held on the server.
3. **Cacheability**: Responses must implicitly or explicitly define themselves as cacheable or non-cacheable.
4. **Layered System**: Clients cannot ordinarily tell whether they are connected directly to the end server or to an intermediate (proxy, CDN, load balancer).
5. **Uniform Interface**: Identification of resources via URIs, manipulation through representations, self-descriptive messages, and hypermedia as the engine of application state (HATEOAS).
6. **Code-on-Demand (Optional)**: Servers can temporarily extend client functionality by transferring executable code (e.g., scripts).

---

## 7. Production Network Programming: Concurrency & Reliability

When writing network servers, you face the C10K / C100K problem: how to efficiently serve tens of thousands of concurrent connections.

- **Thread-per-Connection**: Traditional approach (`threading.Thread`). Simple mental model, but high OS thread stack memory overhead (~8MB per thread) and context switching latency.
- **Thread Pool**: Bounded worker pool (`concurrent.futures.ThreadPoolExecutor`). Prevents memory exhaustion by queuing requests when workers are busy.
- **Event-driven I/O Multiplexing**: Non-blocking sockets using OS primitives (`epoll` on Linux, `kqueue` on macOS/BSD). A single thread drives an event loop handling thousands of sockets concurrently (`asyncio`, `uvicorn`, `Node.js`, `Nginx`).
- **Reliability Patterns**:
  - **Timeouts**: Never issue an unbounded socket read or HTTP call without connection and read timeouts.
  - **Exponential Backoff with Jitter**: Avoid thundering herds by waiting $t = \text{base} \times 2^{\text{attempt}} + \text{uniform}(0, \text{jitter})$.
  - **Connection Pooling**: Reusing established TCP/TLS connections via `requests.Session()` or `httpx.Client()` saves handshake latency.

---

## 8. Networking for Machine Learning: Model Serving & Serialization

Deploying ML models into production requires understanding network serialization and inference performance:
- **Serialization Formats**:
  - `JSON`: Human-readable, ubiquitous, but high parsing overhead and large payload size.
  - `Protocol Buffers / FlatBuffers`: Compact binary format, typed schema, sub-millisecond parsing.
  - `Apache Arrow / Feather`: Zero-copy columnar memory format for large tensor/dataframe transfers.
- **Latency Budgets**:
  $$\text{Total Latency} = \text{DNS} + \text{TCP Handshake} + \text{TLS Negotiation} + \text{Upload Payload} + \text{Inference Time} + \text{Download Payload}$$
- **Batching & Micro-batching**: Trade individual request latency for higher overall throughput by aggregating incoming requests across a short time window (e.g., 2–5ms).

---

## 9. Curriculum Roadmap & Module Navigation

The Level 6 curriculum is structured into three progressive learning modules followed by reference solutions and an automated test suite:

```
networking/
├── 01_tcp_ip/                     # Module 1: TCP/IP & Low-Level Socket Mechanics
│   ├── README.md                  # Deep-dive theory: sockets, buffers, framing
│   ├── 01_tcp_server.py           # Single-client echo server with message framing
│   ├── 02_tcp_client.py           # Robust socket client with buffered reading
│   ├── 03_udp_sockets.py          # Connectionless UDP communication & telemetry
│   ├── 04_concurrent_server.py    # Multi-threaded concurrent TCP server
│   └── exercises.py               # 4-tier progressive exercises
│
├── 02_http_protocols/             # Module 2: HTTP Mechanics, Servers, & Clients
│   ├── README.md                  # HTTP/1.1 anatomy, verbs, headers, status codes
│   ├── 01_raw_http_client.py      # Raw socket-based HTTP client (no third-party libs)
│   ├── 02_python_http_server.py   # Standard library http.server REST-like server
│   ├── 03_requests_and_httpx.py   # Modern HTTP clients (sessions, async httpx)
│   └── exercises.py               # 4-tier progressive exercises
│
├── 03_rest_apis/                  # Module 3: REST Principles & ML Model Serving
│   ├── README.md                  # REST constraints, OpenAPI, model serving architecture
│   ├── 01_rest_principles.py      # Pure Python resource store & CRUD semantics
│   ├── 02_fastapi_endpoints.py    # Production FastAPI app with Pydantic validation
│   ├── 03_ml_model_serving.py     # Live REST API serving ML predictive model
│   └── exercises.py               # 4-tier progressive exercises
│
├── solutions/                     # Fully Worked Reference Solutions (0 TODOs)
│   ├── tcp_ip_solutions.py        # Solutions for Module 1 exercises
│   ├── http_solutions.py          # Solutions for Module 2 exercises
│   └── rest_api_solutions.py      # Solutions for Module 3 exercises
│
└── tests/                         # Automated Verification Suite
    ├── __init__.py
    ├── test_networking_structure.py  # Static validation (files, structure, 0 TODOs)
    └── test_networking_execution.py  # Live execution tests (ephemeral ports, TestClient)
```

### Getting Started
1. Install dependencies:
   ```bash
   pip install -r networking/requirements.txt
   ```
2. Run the automated test suite:
   ```bash
   pytest networking/tests/ -v
   ```
3. Begin with `networking/01_tcp_ip/README.md`.
