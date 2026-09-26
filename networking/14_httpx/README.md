# HTTPX (Modern Python Clients)

## What You Will Learn
You will learn how to use `httpx`, the modern standard for synchronous and asynchronous HTTP in Python, and why it replaces the older `requests` library.

## Prerequisites
Module 10 (Raw HTTP) and Course 0 (Async).

## Key Terminology
| Term | Definition |
|------|------------|
| **Client/Session** | An object that holds TCP connections open so you don't have to reconnect every time. |
| **Connection Pooling** | Reusing the same underlying TCP/TLS socket for multiple HTTP requests. |
| **Timeout** | The maximum time you will wait for the server to reply before giving up. |

## The Problem
Writing raw TCP sockets (like we did in Module 10) is horrible for production. You have to manually parse headers, handle redirects, manage cookies, and negotiate TLS encryption. We need an abstraction.

## How It Works
`httpx` abstracts away the TCP sockets. You just call `httpx.post(url, json=data)` and it automatically calculates the `Content-Length`, serializes the JSON, establishes the TCP handshake, negotiates TLS, and parses the response back into a Python dictionary.

## Intuition
If raw sockets are like building a car from spare parts, `httpx` is like calling an Uber. You just tell it where you want to go.

## Technical Explanation
The most critical feature of `httpx.Client()` is **Connection Pooling**. If you make 10 requests to OpenAI sequentially without a Client, Python opens and closes 10 different TCP/TLS connections (which adds ~150ms of overhead to *every* request). If you use a `Client`, it does the handshake once, and sends all 10 requests over the same open pipe.

## Example
```python
with httpx.Client() as client:
    resp = client.get("https://api.github.com")
```

## Python Implementation
See `httpx_client.py` for a demonstration of connection pooling vs raw requests.

## What Happens Underneath
`httpx` relies on `httpcore`, which relies on `anyio`, which ultimately talks to the OS sockets. It hides a massive state machine that handles TLS handshakes and chunked encoding.

## Common Mistakes
- **Not using a Client/Session:** Making hundreds of `httpx.get()` calls in a loop destroys performance.
- **Ignoring Timeouts:** The default timeout is often 5 seconds. If the LLM takes 10 seconds to generate a response, your app will crash.

## Security Considerations
Never disable SSL verification (`verify=False`) in production, or you are vulnerable to Man-in-the-Middle attacks.

## Real-World Applications
Every modern Python backend uses `httpx` (or `aiohttp`) to talk to other microservices.

## AI-Agent Connection
This is how your agent talks to OpenAI, Anthropic, and external tool APIs. Properly configuring the `httpx.AsyncClient` with high timeouts (e.g., 60 seconds) is mandatory for LLM calls.

## Exercises
See `exercises.py`.

## Challenge
Write a script that times the difference between 10 unpooled requests and 10 pooled requests to the same server.

## Summary
`httpx` provides a robust, modern, async-compatible interface over the raw HTTP protocol.

## What You Should Know Before Moving On
You should know why `httpx.Client()` is vastly superior to `httpx.get()`.
