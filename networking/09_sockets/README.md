# Sockets (The Code Interface)

## What You Will Learn
You will learn how to actually write code that interacts with the network. You will move from the theory of TCP/UDP into writing raw Python socket code.

## Prerequisites
Module 07 (TCP) and Module 08 (UDP).

## Key Terminology
| Term | Definition |
|------|------------|
| **Socket** | An abstraction provided by the OS that allows programs to send/receive data over a network, treating the network like a file. |
| **Bind** | Attaching a socket to a specific local IP and Port. |
| **Listen** | Telling the OS to queue up incoming TCP connections for this socket. |
| **Accept** | Pulling the next incoming TCP connection off the OS queue. |

## The Problem
How does a user-space program (like your Python script) actually tell the operating system's network card to send voltage pulses over an Ethernet cable? The OS needs a safe, standardized API to expose network hardware to programmers.

## How It Works
The Socket API (originally developed at UC Berkeley in 1983) is the universal solution. A socket is just a file descriptor. To your Python code, writing to a TCP socket looks exactly the same as writing text to a file on your hard drive. The OS handles all the magic of converting that "file write" into network packets.

## Intuition
A socket is like a pneumatic tube at a bank drive-through. 
- You build the tube (`socket()`).
- You connect it to the teller (`connect()`).
- You put a message in the capsule and send it (`send()`).
- You wait for a capsule to come back (`recv()`).

## Technical Explanation
The typical TCP Server lifecycle:
1. `s = socket(AF_INET, SOCK_STREAM)` (Create an IPv4 TCP socket)
2. `s.bind(('0.0.0.0', 8080))` (Claim port 8080)
3. `s.listen()` (Start queuing connections)
4. `conn, addr = s.accept()` (Block until a client connects; returns a NEW socket specifically for this client)
5. `conn.recv()` / `conn.send()` (Communicate)
6. `conn.close()` (Hang up)

## Example
If you try to read from a socket, and no data has arrived yet, your Python script will completely freeze (block) on the `recv()` line until data arrives. This is why async programming (Course 0) is so important!

## Python Implementation
See `socket_demo.py` for a fully functional, heavily commented TCP Echo server.

## What Happens Underneath
When you call `recv(1024)`, Python asks the OS kernel for data. If the kernel's network buffer is empty, the OS puts your Python thread to sleep. When the network card receives a packet via hardware interrupts, the kernel wakes your Python thread up and hands it the data.

## Common Mistakes
- **Assuming `send()` sends everything:** `send()` returns the number of bytes actually sent. If the OS buffer is full, it might only send half your message! You must use a loop or `sendall()`.
- **String vs Bytes:** Sockets don't understand Python strings. You must `.encode('utf-8')` before sending and `.decode('utf-8')` after receiving.

## Security Considerations
Raw sockets have no encryption. If you build a chat app using raw sockets, anyone on the network can read the chat. You must wrap the socket in the `ssl` module to create a secure TLS socket.

## Real-World Applications
Every web server (Gunicorn, Uvicorn, Nginx), database driver (psycopg2, asyncpg), and HTTP client (requests, httpx) is built on top of this exact Socket API.

## AI-Agent Connection
Agent frameworks rarely use raw sockets directly. They use higher-level libraries like HTTPX or WebSockets. However, when you get a `ConnectionResetError` or a `TimeoutError` from an LLM API, that error is being thrown directly by the underlying Socket!

## Exercises
See `exercises.py`.

## Challenge
Modify the `socket_demo.py` server to handle multiple clients simultaneously using `select()` or threading.

## Summary
Sockets are the fundamental OS-level API that bridges high-level application code (like Python) with the low-level complexities of the network hardware.

## What You Should Know Before Moving On
You should be able to write a basic TCP client and server from memory, and understand the difference between `bind()`, `listen()`, and `accept()`.
