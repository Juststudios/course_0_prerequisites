# HTTP From the Ground Up

## What You Will Learn
You will learn exactly what an HTTP request looks like over the wire before libraries like `requests` or `httpx` hide it from you. 

## Prerequisites
Module 09 (Sockets).

## Key Terminology
| Term | Definition |
|------|------------|
| **HTTP** | Hypertext Transfer Protocol. The language of the web. |
| **Request Line** | The first line of an HTTP request (e.g., `GET / HTTP/1.1`). |
| **Header** | Key-value pairs providing metadata (e.g., `Host: api.com`). |
| **Body** | The actual payload (like a JSON string) sent after the headers. |

## The Problem
When you call `httpx.post()`, it feels like magic. But if you don't understand that HTTP is just plain text sent over a TCP socket, you won't be able to debug issues like "Missing Content-Length header" or understand how Server-Sent Events work.

## How It Works
HTTP is entirely text-based. A client opens a TCP socket, sends a specifically formatted string of text ending with a double newline `\r\n\r\n`, and waits for the server to send text back.

## Intuition
HTTP is just a highly formalized text message. 
"Hey Server, give me the file at /index.html. I am using Chrome. Here is my secret cookie token."

## Technical Explanation
An HTTP Request looks exactly like this:
```http
POST /v1/chat/completions HTTP/1.1
Host: api.openai.com
Content-Type: application/json
Authorization: Bearer sk-...
Content-Length: 27

{"model": "gpt-4", "messages": []}
```
Notice the blank line between the headers and the JSON body. That blank line tells the server "Headers are done, the body is starting."

## Example
If you forget the `Content-Length` header, the server won't know when to stop reading the TCP socket, and your request will just hang indefinitely!

## Python Implementation
See `raw_http_demo.py` where we build an HTTP request completely from scratch using raw Python sockets (no `httpx` allowed!).

## What Happens Underneath
Your Python string is encoded to bytes, sent via `socket.sendall()`, chopped into TCP segments by the OS, and routed via IP to the server.

## Common Mistakes
- **Forgetting `\r\n`:** HTTP strictly requires Carriage Return + Line Feed. Just `\n` will break strict servers.
- **Wrong Content-Length:** If you say the length is 10 but send 20 bytes, the server drops the rest.

## Security Considerations
Raw HTTP is sent in plain text. Anyone on your WiFi can read the Authorization header and steal your API keys.

## Real-World Applications
Every REST API, every website, and every AI model provider communicates using this exact text format.

## AI-Agent Connection
Agent runtimes send massive JSON bodies (your chat history) in the HTTP body.

## Exercises
See `exercises.py`.

## Challenge
Modify `raw_http_demo.py` to send a POST request with a JSON body to a mock server.

## Summary
HTTP is not magic; it is just a formatted text string sent over a TCP socket.

## What You Should Know Before Moving On
You should be able to write an HTTP GET request by hand on a whiteboard.
