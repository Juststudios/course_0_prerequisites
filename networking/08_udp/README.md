# UDP (User Datagram Protocol)

## What You Will Learn
You will learn about TCP's wilder, faster sibling. You will understand how connectionless communication works, why dropping packets is sometimes perfectly acceptable, and when to choose UDP over TCP.

## Prerequisites
Module 07 (TCP).

## Key Terminology
| Term | Definition |
|------|------------|
| **Connectionless** | Sending data without performing a handshake first. |
| **Datagram** | An independent, self-contained message sent over a network. |
| **Fire-and-Forget** | The design philosophy of UDP. Send the packet and assume it got there. |

## The Problem
TCP is reliable, but it is *slow*. The 3-way handshake takes time. ACKs take time. If a packet is lost, TCP pauses the entire stream to request the missing packet. What if you are on a live Zoom call? If you lose a frame of video from 3 seconds ago, you don't want the video to freeze while it retrieves the old frame—you just want to skip it and see the present moment!

## How It Works
UDP is incredibly simple. The OS takes your data, slaps a Destination IP and Port on it, and throws it onto the network. No handshakes, no sequence numbers, no acknowledgements, no retries. If the packet gets lost, it's gone forever. If packets arrive out of order, the OS hands them to your app out of order.

## Intuition
- **TCP** is a phone call. You dial, they say "Hello", you talk back and forth, you say "Goodbye", and hang up.
- **UDP** is throwing a paper airplane with a message on it into a crowd. You don't know if it hit the target, and you don't care.

## Technical Explanation
Because UDP lacks the heavy header overhead and state-tracking of TCP, it is highly efficient. The UDP header is only 8 bytes (compared to TCP's 20-60 bytes). 

## Example
If you play a fast-paced multiplayer game like Call of Duty, your movement coordinates are sent via UDP 60 times a second. If packet #42 is lost, the server doesn't care, because packet #43 arrives 16 milliseconds later with your updated position anyway.

## Python Implementation
See `udp_server.py` and `udp_client.py`. Notice there is no `server.listen()` or `server.accept()`. The server just calls `recvfrom()` and immediately starts reading packets from anyone who sends them.

## What Happens Underneath
The OS does almost no work for UDP. It just wraps the payload in an 8-byte header and passes it directly to the IP layer for routing.

## Common Mistakes
- **Assuming UDP guarantees delivery:** If you send a command like `DELETE_DATABASE` over UDP, and the packet is lost, the command just never happens.
- **Assuming packets arrive in order:** You might send A, B, C and the receiver gets C, A, B. 

## Security Considerations
UDP is heavily used in **DDoS (Distributed Denial of Service) Amplification Attacks**. Because there is no handshake, an attacker can easily forge (spoof) the Source IP. They send a tiny UDP request to a DNS server, forging the Source IP to be *your* IP, and the DNS server sends a massive response to *you*, flooding your connection.

## Real-World Applications
- Video streaming / VoIP (Zoom, Discord)
- Multiplayer Gaming
- DNS lookups (because doing a 3-way TCP handshake just to ask for an IP address is too slow)
- IoT sensor telemetry

## AI-Agent Connection
Most agent architectures use TCP (via HTTP). However, if your agent needs to process live, real-time audio streams (like a Voice AI), you will likely use WebRTC, which runs over UDP to minimize latency.

## Exercises
See `exercises.py`.

## Challenge
Write a UDP client that sends 100 numbered packets, and a server that tracks which numbers were lost in transit.

## Summary
UDP prioritizes speed and low latency over reliability, making it the protocol of choice for real-time applications where missing a piece of old data doesn't matter.

## What You Should Know Before Moving On
You should be able to confidently explain exactly when to choose TCP (when data integrity matters) vs UDP (when speed matters).
