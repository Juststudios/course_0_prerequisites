# Module 2: HTTP Protocols & Web Mechanics

## 1. HTTP as the Lingua Franca of Distributed Systems

Hypertext Transfer Protocol (HTTP) is an application-layer request-response protocol running over TCP (and recently QUIC/UDP). While originally designed for fetching static HTML documents, HTTP is now the universal application transport for:
- RESTful web services and JSON microservices
- Machine learning model inference gateways
- Telemetry reporting and health monitoring endpoints
- Large-scale cloud data ingestion APIs

---

## 2. HTTP/1.1 Protocol Grammar & Mechanics (RFC 9112)

HTTP/1.1 is a human-readable, plain-text protocol. Every message is delimited strictly by carriage return and line feed bytes: `\r\n` (`CRLF`).

```
+--------------------------------------------------------------------+
| Start Line (Request line or Status line)                           | \r\n
+--------------------------------------------------------------------+
| Header-Name: Header-Value                                          | \r\n
| Header-Name: Header-Value                                          | \r\n
| ...                                                                | \r\n
+--------------------------------------------------------------------+
| [Mandatory Empty Line indicating header completion]                | \r\n
+--------------------------------------------------------------------+
| Optional Body (Binary payload, JSON, HTML, etc.)                   |
+--------------------------------------------------------------------+
```

---

## 3. Request Anatomy

A complete HTTP/1.1 request formatted over a TCP socket:

```http
POST /api/v1/predict HTTP/1.1\r\n
Host: api.example.com\r\n
User-Agent: PearlTelemetryClient/1.0\r\n
Content-Type: application/json\r\n
Content-Length: 38\r\n
Connection: keep-alive\r\n
\r\n
{"features": [1.4, 2.8, 0.5, 3.1]}
```

Key Components:
1. **Method**: Indicates the desired action (`GET`, `POST`, etc.).
2. **Request Target (URI)**: The path and optional query string (`/api/v1/predict?verbose=true`).
3. **HTTP Version**: `HTTP/1.1`.
4. **Mandatory `Host` Header**: Required in HTTP/1.1 to enable virtual hosting (multiple domains sharing one IP).
5. **`Content-Length`**: Byte length of the request body (crucial for receiver framing).

---

## 4. Response Anatomy & Status Code Taxonomy

A complete HTTP/1.1 response:

```http
HTTP/1.1 200 OK\r\n
Date: Wed, 17 Sep 2026 15:00:00 GMT\r\n
Server: Uvicorn/0.28.0\r\n
Content-Type: application/json\r\n
Content-Length: 42\r\n
\r\n
{"prediction": "fault_detected", "prob": 0.94}
```

### Status Code Categories:
- **1xx (Informational)**: Request received, continuing process (e.g., `101 Switching Protocols` for WebSockets).
- **2xx (Successful)**: Action successfully received, understood, and accepted:
  - `200 OK`: Standard success.
  - `201 Created`: Resource created (common after `POST`).
  - `204 No Content`: Successful action with empty response body (common after `DELETE`).
- **3xx (Redirection)**: Further action must be taken:
  - `301 Moved Permanently`: Permanent redirect (cached by client).
  - `302 Found`: Temporary redirect.
  - `304 Not Modified`: Cached response is still valid (conditional `If-None-Match`).
- **4xx (Client Error)**: Request contains bad syntax or cannot be fulfilled:
  - `400 Bad Request`: Malformed syntax or invalid payload.
  - `401 Unauthorized`: Authentication required or invalid credentials.
  - `403 Forbidden`: Authenticated, but lacking permission.
  - `404 Not Found`: Target resource does not exist.
  - `422 Unprocessable Entity`: Valid syntax, but semantic validation failed (Pydantic standard).
  - `429 Too Many Requests`: Rate limit exceeded.
- **5xx (Server Error)**: Server failed to fulfill an apparently valid request:
  - `500 Internal Server Error`: Unhandled server exception.
  - `502 Bad Gateway`: Upstream server returned invalid response.
  - `503 Service Unavailable`: Server overloaded or undergoing maintenance.
  - `504 Gateway Timeout`: Upstream server timed out.

---

## 5. HTTP Methods: Safe vs. Idempotent

| Method | Safe? (No state change) | Idempotent? ($f(x) = f(f(x))$) | Typical CRUD Mapping |
|---|---|---|---|
| `GET` | **Yes** | **Yes** | Read resource |
| `HEAD` | **Yes** | **Yes** | Read headers only |
| `OPTIONS` | **Yes** | **Yes** | Query supported methods |
| `POST` | **No** | **No** | Create resource / invoke RPC |
| `PUT` | **No** | **Yes** | Complete replacement of resource |
| `PATCH` | **No** | **No** (can be designed so) | Partial modification of resource |
| `DELETE` | **No** | **Yes** | Remove resource |

**Why Idempotence Matters for Network Engineers**:
If a network timeout occurs during a `GET`, `PUT`, or `DELETE`, the client can safely retry the request automatically without risk of duplicate side effects. If a timeout occurs during a `POST` (e.g. payment or credit charge), blind retries risk duplicate transactions!

---

## 6. Connection Management: Keep-Alive & Head-of-Line Blocking

In HTTP/1.0, a new TCP connection was established and torn down for every single asset.
- In **HTTP/1.1**, connections are persistent (`Connection: keep-alive`) by default. Multiple requests and responses can be sequentially exchanged over a single TCP socket.
- **Head-of-Line (HoL) Blocking**: In HTTP/1.1, responses must be sent strictly in the order requests were received. If the first request involves a slow database query, all subsequent pipelined requests are blocked.

---

## 7. HTTP/2 and HTTP/3 Innovations

- **HTTP/2 (2015)**:
  - Replaces ASCII text with binary framing (`HEADERS`, `DATA` frames).
  - **Multiplexing**: Interleaves multiple independent request/response streams concurrently over a single TCP socket, eliminating HTTP application-level HoL blocking.
  - **HPACK**: State-based header compression reducing bandwidth overhead.
- **HTTP/3 & QUIC (2022)**:
  - Moves from TCP to UDP.
  - Eliminates TCP transport-level HoL blocking (packet loss in one stream does not pause other streams).
  - Fast 0-RTT connection establishment.

---

## 8. Python HTTP Client Ecosystem

1. **`urllib.request` (Standard Library)**: Zero external dependencies, but verbose API and no automatic connection pooling.
2. **`requests` (The Gold Standard Synchronous Client)**: Beautiful, intuitive API, automatic connection pooling (`urllib3.PoolManager`), session management, and robust JSON handling.
3. **`httpx` (Next-Generation Client)**: Feature-complete `requests` compatible API with native `asyncio` support (`httpx.AsyncClient`) and HTTP/2 support.

---

## 9. Security & HTTPS (TLS/SSL)

HTTPS wraps the cleartext HTTP conversation inside a TLS (Transport Layer Security) tunnel:
1. **Confidentiality**: Symmetric encryption (e.g., AES-GCM, ChaCha20) prevents eavesdropping.
2. **Integrity**: Cryptographic MACs prevent packet tampering.
3. **Authentication**: X.509 Public Key Certificates signed by Certificate Authorities (CAs) verify the server identity.
