# IP Addresses

## What You Will Learn
You will learn how every device on the internet is uniquely identified, the difference between public and private networks, and why `127.0.0.1` (localhost) is critical for local AI development.

## Prerequisites
Module 03 (OSI and TCP/IP).

## Key Terminology
| Term | Definition |
|------|------------|
| **IPv4 Address** | A 32-bit number (e.g., `192.168.1.5`) identifying a node on a network. |
| **IPv6 Address** | A 128-bit number introduced because we ran out of IPv4 addresses. |
| **Public IP** | An address reachable from anywhere on the global internet. |
| **Private IP** | An address only reachable within a local network (like your home Wi-Fi). |
| **Localhost** | A special address (`127.0.0.1`) that loops back to your own computer. |

## The Problem
If you want to send a letter, you need a unique mailing address. With billions of phones, servers, and smart devices connected to the internet, how do we ensure a packet of data reaches the exact correct device and doesn't get lost in the noise?

## How It Works
Internet Protocol (IP) addresses solve this. Every packet sent over the internet has a "Source IP" and a "Destination IP" stamped on its header. Routers read the Destination IP and forward the packet closer to its target. 

## Intuition
An IP address is literally just a phone number for a computer. 
- A **Public IP** is like a company's main phone line (anyone in the world can dial it).
- A **Private IP** is like an internal office extension (you can only dial it if you are already inside the building).
- **Localhost (`127.0.0.1`)** is like talking to yourself in the mirror.

## Technical Explanation
IPv4 addresses are 4 bytes (32 bits), usually written in "dotted decimal" format like `192.168.1.10`. Because 32 bits only allows for ~4.3 billion unique addresses, the internet invented Network Address Translation (NAT) so entire households can share one Public IP, while devices inside the house get Private IPs (usually starting with `192.168.x.x` or `10.x.x.x`).

## Example
If you run `ping 8.8.8.8` in your terminal, you are sending packets to Google's public DNS server. If you run `ping 127.0.0.1`, you are pinging your own machine.

## Python Implementation
See `ip_demo.py` for a script that uses Python's `socket` library to resolve your machine's local IP address and validate IPv4 strings.

## What Happens Underneath
When you send a packet to `127.0.0.1`, the OS kernel intercepts it before it ever reaches your physical Wi-Fi card and instantly loops it back up to the receiving application. This makes localhost communication incredibly fast and perfectly reliable.

## Common Mistakes
- **Binding a server to `127.0.0.1` and wondering why other computers can't reach it.** (You must bind to `0.0.0.0` to accept external connections).
- Hardcoding IP addresses in code instead of using domain names (IPs can change!).

## Security Considerations
If a server has a Public IP, it is constantly being scanned by automated bots across the globe looking for vulnerabilities. Never run a development database on a Public IP without a firewall.

## Real-World Applications
Every single time you open a web browser, play an online game, or send a text, IP addresses are routing the data.

## AI-Agent Connection
When building an agent, you will often run your LLM (like Ollama or vLLM) locally. Your agent will connect to it using `http://127.0.0.1:11434`. Understanding localhost is mandatory for local agent development.

## Exercises
See `exercises.py`.

## Challenge
Write a Python function that determines if an IP address is Public or Private based on its first octet.

## Summary
IP addresses are the global addressing system of the internet, with special blocks reserved for local networks and loopback testing.

## What You Should Know Before Moving On
You must understand the difference between `127.0.0.1`, a Private IP, and a Public IP.
