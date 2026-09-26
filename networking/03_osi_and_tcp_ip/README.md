# OSI and TCP/IP Models

## What You Will Learn
You will learn the two primary mental models used to categorize network protocols: The theoretical OSI model, and the practical TCP/IP model that actually runs the internet.

## Prerequisites
Module 02 (How Data Moves).

## Key Terminology
| Term | Definition |
|------|------------|
| **OSI Model** | A 7-layer theoretical model of networking (Please Do Not Throw Sausage Pizza Away). |
| **TCP/IP Model** | A simpler 4-layer practical model that the modern internet is actually built on. |
| **Protocol Suite** | A collection of protocols designed to work together (like TCP and IP). |

## The Problem
With thousands of different networking technologies (Wi-Fi, Ethernet, Bluetooth, IP, TCP, UDP, HTTP, FTP), how do engineers organize them so they know which technologies interact with which? We need a classification system.

## How It Works
The models classify protocols into layers. 
- If you are building a web browser, you only care about the **Application Layer**.
- If you are building a router, you care about the **Network Layer**.
- If you are building a fiber-optic cable, you care about the **Physical Layer**.

## Intuition
The OSI model is like the Dewey Decimal System in a library. It's just a way of categorizing things so engineers can talk to each other without confusion.

## Technical Explanation
**The 7-Layer OSI Model:**
7. Application (HTTP, DNS)
6. Presentation (TLS encryption, JSON formatting)
5. Session (Maintaining connections)
4. Transport (TCP, UDP)
3. Network (IP, Routers)
2. Data Link (Ethernet, MAC addresses, Switches)
1. Physical (Cables, Radio waves)

**The 4-Layer TCP/IP Model (What actually matters):**
4. Application (Combines OSI 5, 6, 7)
3. Transport (OSI 4)
2. Internet (OSI 3)
1. Network Access (Combines OSI 1, 2)

## Example
When a network engineer says "We have a Layer 3 issue", they mean the problem is at the Network Layer (IP addressing or Routing), not a broken cable (Layer 1) or a crashed Python app (Layer 7).

## Python Implementation
See `osi_model.py` for a script that categorizes common protocols.

## What Happens Underneath
These models aren't literal software. You can't open a folder on your computer called "Layer 4". They are conceptual boundaries implemented within the OS networking stack.

## Common Mistakes
- Trying to force every protocol perfectly into an OSI layer (many modern protocols blur the lines).
- Memorizing the OSI model without understanding what the layers actually do.

## Security Considerations
Security must be applied at multiple layers. WPA3 secures Layer 2 (Wi-Fi). IPsec secures Layer 3. TLS secures Layer 6/7.

## Real-World Applications
When an AWS server goes down, engineers use these models to troubleshoot. "Is the app running? (Layer 7) Yes. Can we ping the IP? (Layer 3) No. Is the virtual cable connected? (Layer 1)."

## AI-Agent Connection
As an AI agent developer, you will spend 99% of your time at Layer 7 (Application - HTTP/JSON), relying on the operating system to handle Layers 1-4.

## Exercises
See `exercises.py`.

## Challenge
Categorize these technologies into their OSI layers: Bluetooth, HTTP, IPv6, TCP, JSON.

## Summary
The OSI and TCP/IP models provide a shared vocabulary for engineers to discuss and troubleshoot complex networks.

## What You Should Know Before Moving On
You should know the 4 layers of the TCP/IP model and be able to explain what "Layer 7" means.
