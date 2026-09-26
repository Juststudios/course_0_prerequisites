# Ports

## What You Will Learn
You will learn how a single computer with one IP address can run dozens of different network services (web, database, email) simultaneously without confusing the traffic.

## Prerequisites
Module 04 (IP Addresses).

## Key Terminology
| Term | Definition |
|------|------------|
| **Port** | A 16-bit number (0 to 65535) identifying a specific process or service on a machine. |
| **Socket** | The combination of an IP Address and a Port (e.g., `192.168.1.5:80`). |
| **Listening** | When a server application waits for incoming connections on a specific port. |
| **Ephemeral Port** | A temporary, random port assigned to a client making an outbound request. |

## The Problem
An IP address gets a packet to the correct computer. But a modern server might be running an HTTP web server, a PostgreSQL database, and an SSH daemon all at once. When a packet arrives, how does the OS know which application should receive it?

## How It Works
Ports solve this multiplexing problem. Every TCP and UDP packet includes a "Destination Port". When the packet arrives, the OS looks at the port number and hands the payload to whichever application is "listening" on that port.

## Intuition
If an IP address is the street address of an apartment building, the **Port** is the apartment number. 
- You want to talk to the Web Server? Go to Apartment 80.
- You want to talk to the Database? Go to Apartment 5432.

## Technical Explanation
Ports are 16-bit integers, giving 65,536 possible ports. 
- **0–1023:** Well-known ports (requires admin/root privileges to use). e.g., 80 (HTTP), 443 (HTTPS), 22 (SSH).
- **1024–49151:** Registered ports. e.g., 5432 (PostgreSQL), 6379 (Redis).
- **49152–65535:** Ephemeral ports. When your web browser makes a request, the OS assigns it a random ephemeral port so the server knows where to send the reply.

## Example
```text
http://localhost:8000
```
This tells the browser: "Connect to the local machine (`localhost`), and talk to the application listening on Port `8000`."

## Python Implementation
See `port_scanner.py` for a script that attempts to connect to a range of ports to see which ones have listening applications.

## What Happens Underneath
When an application calls `bind(port)`, the OS updates an internal table linking that port to the application's process ID (PID). If another application tries to bind to the same port, the OS throws an `Address already in use` error.

## Common Mistakes
- **Port Conflicts:** Trying to start two web servers on port 8000 at the same time.
- **Forgetting the port:** Trying to connect to a database on the default web port (80) instead of 5432.

## Security Considerations
Leaving unnecessary ports open to the public internet is the primary way hackers breach servers. Firewalls work by blocking traffic to specific ports (e.g., blocking port 22 to prevent SSH brute-forcing).

## Real-World Applications
Docker heavily relies on port mapping (e.g., mapping port 8080 on your laptop to port 80 inside the container) to prevent port conflicts when running multiple isolated services.

## AI-Agent Connection
Agent runtimes often connect to multiple services simultaneously:
- FastAPI Gateway: Port 8000
- PostgreSQL Database: Port 5432
- Redis Cache: Port 6379
- Local LLM (Ollama): Port 11434

## Exercises
See `exercises.py`.

## Challenge
Modify the port scanner to use `asyncio` to scan 100 ports concurrently.

## Summary
Ports allow a single IP address to host thousands of distinct services by routing packets to the correct application based on a 16-bit number.

## What You Should Know Before Moving On
You should know what a port is, why port conflicts happen, and be able to name the standard ports for HTTP (80) and HTTPS (443).
