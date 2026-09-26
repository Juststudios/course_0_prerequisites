# How Data Moves

## What You Will Learn
You will learn the conceptual model of how data travels from an application on one computer, down into physical wires, and back up into an application on another computer.

## Prerequisites
Module 01 (Networking Fundamentals).

## Key Terminology
| Term | Definition |
|------|------------|
| **Encapsulation** | Wrapping data in headers as it moves down the network stack. |
| **Decapsulation** | Unwrapping data as it moves up the network stack on the receiving end. |
| **Payload** | The actual useful data being sent (e.g., the JSON text). |
| **Header** | Meta-information attached to the payload (e.g., destination IP address). |

## The Problem
When you call `requests.get("http://api.com")` in Python, you are dealing with text. But the Wi-Fi card in your laptop only understands radio waves. How does the text get translated into radio waves in a way that the receiving server can understand?

## How It Works
The process is layered:
1. **Application Layer:** Python creates the HTTP text.
2. **Transport Layer:** The OS chops the text into TCP segments and adds port numbers.
3. **Network Layer:** The OS adds IP addresses (where is it going globally?).
4. **Link Layer:** The OS adds MAC addresses (how do I reach the router in my house?).
5. **Physical Layer:** The hardware converts it to electrical/radio signals.

## Intuition
Think of sending a physical product:
1. **Application:** You write a letter (The Data).
2. **Transport:** You put it in a box (TCP).
3. **Network:** You put a shipping label on the box (IP).
4. **Link:** You put the box in a mail truck (Ethernet/WiFi).
5. **Physical:** The truck drives on the highway (The Wires).

## Technical Explanation
As data moves down the stack, each layer prepends a header. 
`[Ethernet Header [IP Header [TCP Header [HTTP Data]]]]`
When the destination receives it, it strips the headers off one by one, verifying the data at each step, until the raw HTTP data is handed to the destination application.

## Example
If you send the word "HELLO" (5 bytes), the actual amount of data transmitted over the wire might be 60+ bytes because of all the TCP, IP, and Ethernet headers attached to it!

## Python Implementation
See `data_movement.py` for a conceptual simulation of encapsulation.

## What Happens Underneath
The OS kernel executes the TCP/IP stack. Python doesn't handle headers; it just hands the payload to the OS using a Socket, and the OS does all the encapsulation.

## Common Mistakes
- Thinking Python sends raw HTTP over the wire directly.
- Forgetting that headers add overhead (sending 1 byte of data still requires 40 bytes of headers).

## Security Considerations
If someone intercepts the packet at the Link layer, they can read the Payload unless the Application layer encrypted it first!

## Real-World Applications
This layered model is why you can swap from Wi-Fi to an Ethernet cable, and your Python HTTP script doesn't need to be rewritten. The Application layer doesn't care about the Link layer!

## AI-Agent Connection
When your agent sends a 2,000-token prompt to an LLM, the OS chops it into dozens of IP packets, encapsulates them, and fires them across the ocean.

## Exercises
See `exercises.py`.

## Challenge
Write a function that takes a string payload, and "encapsulates" it by prepending fake TCP and IP headers.

## Summary
Data moves by being systematically wrapped in headers (encapsulation) as it travels down to the hardware, and unwrapped (decapsulation) at the destination.

## What You Should Know Before Moving On
You should understand that networking is separated into layers so that applications don't have to worry about hardware.
