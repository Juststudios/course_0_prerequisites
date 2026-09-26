# Networking Fundamentals

## What You Will Learn
You will learn what a network actually is at a physical and logical level. You will understand how individual computers (nodes) connect to form local networks, and how those local networks connect to form the global internet.

## Prerequisites
Course -1 Python Foundations.

## Key Terminology
| Term | Definition |
|------|------------|
| **Node / Host** | Any device connected to a network (your laptop, a server, a smart fridge). |
| **Client** | A node that requests data (e.g., your web browser). |
| **Server** | A node that listens for requests and provides data. |
| **Packet** | A small chunk of data sent over a network. The internet does not send files; it sends packets. |
| **Protocol** | A strict set of rules for how nodes communicate. If computers don't speak the same protocol, they cannot talk. |

## The Problem
If you have two computers sitting next to each other, how do you transfer a file? You could use a USB drive, but what if they are in different countries? We need a standardized way to convert files into electrical signals, route them across the globe, and reassemble them without corruption.

## How It Works
Data is broken down into tiny chunks called packets. Each packet is wrapped with routing information (like an envelope with a To and From address). These packets are sent over physical wires or radio waves to routers, which act like post offices, forwarding the packets until they reach their destination.

## Intuition
Think of a network like a global postal system. 
- You are the **Client**.
- The business you are ordering from is the **Server**.
- The mail truck is the **Network**.
- The rules about how to format the address on the envelope is the **Protocol**.
- The letters themselves are the **Packets**.

## Technical Explanation
At the lowest level, networking is just voltage changes on a copper wire, pulses of light in a fiber optic cable, or radio frequencies (Wi-Fi). Network Interface Cards (NICs) translate digital bits (0s and 1s) into these physical signals.

## Example
When you ping `google.com`, your computer creates a tiny ICMP packet, sends it to your home router, which sends it to your ISP, which sends it to Google. Google receives it and sends a packet back.

## Python Implementation
See `networking_basics.py` for a simulation of a basic client-server message queue.

## What Happens Underneath
The operating system takes your data, wraps it in multiple layers of headers (TCP, IP, Ethernet), and hands it to the hardware network driver to be serialized into physical signals.

## Common Mistakes
- Confusing a "Client" and a "Server" (any computer can be both!).
- Assuming a network is a direct, dedicated wire between two computers.

## Security Considerations
Because packets travel through public infrastructure (routers owned by ISPs), anyone sitting between you and the server can intercept and read your packets unless they are encrypted.

## Real-World Applications
Everything from loading a web page to playing multiplayer games relies on these fundamental packet-switching concepts.

## AI-Agent Connection
Your AI agent acts as a **Client** when talking to the LLM (OpenAI/Anthropic), but acts as a **Server** when waiting for you to send it a message on Telegram or a Web UI. It must master both roles.

## Exercises
See `exercises.py`.

## Challenge
Write a Python script that pings 3 different websites and calculates the average latency.

## Summary
Networks are built by connecting nodes together and agreeing on strict protocols for how to chop data into packets and route them.

## What You Should Know Before Moving On
You should understand the difference between a client, a server, a packet, and a protocol.
