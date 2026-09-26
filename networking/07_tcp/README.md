# TCP (Transmission Control Protocol)

## What You Will Learn
You will learn why raw network packets are unreliable, and how TCP creates the illusion of a continuous, reliable pipe of data. You'll understand the "three-way handshake" and why connections take time to establish.

## Prerequisites
Module 04 (IP Addresses) and Module 05 (Ports).

## Key Terminology
| Term | Definition |
|------|------------|
| **Connection-Oriented** | A virtual link established between two machines before data is sent. |
| **Three-Way Handshake** | The SYN, SYN-ACK, ACK sequence used to start a connection. |
| **Packet Loss** | When data drops out over the network; TCP automatically detects and resends it. |
| **Socket** | The software endpoint of a network connection. |

## The Problem
If you send a movie file over the internet, it gets chopped into thousands of tiny packets. What happens if packet #42 gets lost? What if packet #99 arrives before packet #98? If developers had to manually write code to reorder packets and ask for missing ones every time they built an app, nothing would ever get done.

## How It Works
TCP sits on top of IP (the delivery mechanism). When you send data via TCP, the operating system kernel assigns sequence numbers to every packet. The receiving computer sends back "Acknowledgements" (ACKs). If the sender doesn't get an ACK fast enough, it assumes the packet was lost and resends it. 

## Intuition
Think of IP as the postal service, and TCP as sending a book by mailing one page at a time using Certified Mail. 
- You number the pages (Sequence numbers).
- The receiver texts you "Got page 1!" (Acknowledgements).
- If you don't get a text for page 2, you mail another copy of page 2 (Retransmission).
- The receiver waits until they have all the pages in order before reading the book.

## Technical Explanation
The TCP Three-Way Handshake:
1. **SYN (Synchronize):** Client says "I want to talk, my first sequence number is X."
2. **SYN-ACK:** Server says "Got it! I acknowledge X+1. My first sequence number is Y."
3. **ACK:** Client says "Got it! I acknowledge Y+1."
Now, the pipe is open.

## Example
When you type `https://google.com` into your browser, before any web page data is requested, your computer does a TCP handshake with Google's server on Port 443.

## Python Implementation
See `tcp_server.py`. Notice how `server.accept()` blocks (pauses) the program until a client completes the 3-way handshake!

## What Happens Underneath
Your Python code doesn't actually do the handshake! The Python `socket` library is just a wrapper around C-level OS system calls. The Linux kernel's networking stack handles the SYN/ACKs in the background.

## Common Mistakes
- **Assuming data arrives all at once:** `conn.recv(1024)` might return 10 bytes or 1024 bytes. You have to keep receiving in a loop until the message is complete.
- **Forgetting to close sockets:** Leads to "Too many open files" errors.
- **Address already in use:** Trying to restart a server too quickly while the OS is still cleaning up the old socket.

## Security Considerations
TCP itself is completely unencrypted. Anyone on the same WiFi network can read the raw text of your TCP packets using tools like Wireshark. This is why we need TLS (HTTPS).

## Real-World Applications
Web browsing (HTTP), Database connections (PostgreSQL), Email (SMTP), and SSH all run over TCP because they require perfect data integrity.

## AI-Agent Connection
When your AI agent calls the OpenAI API, it opens a TCP connection. If the connection drops mid-generation, TCP tries to recover it. If it fails, your agent crashes unless you wrote good retry logic.

## Exercises
See `exercises.py`.

## Challenge
Modify the server so it can handle 5 clients simultaneously using Python threads.

## Summary
TCP provides a reliable, ordered, error-checked stream of data between applications, hiding the messy reality of the internet.

## What You Should Know Before Moving On
You should understand that TCP requires a handshake, guarantees delivery, and is the foundation for almost everything else we will build, including HTTP.
