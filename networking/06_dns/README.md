# DNS (Domain Name System)

## What You Will Learn
You will learn how human-readable website names (like `google.com`) are translated into machine-readable IP addresses, and how this heavily distributed system powers the entire internet.

## Prerequisites
Module 04 (IP Addresses).

## Key Terminology
| Term | Definition |
|------|------------|
| **DNS** | Domain Name System. The phonebook of the internet. |
| **A Record** | Maps a domain name to an IPv4 address. |
| **CNAME Record** | Maps a domain name to another domain name (an alias). |
| **Resolver** | The server your computer asks to look up a domain name (usually provided by your ISP or Google/Cloudflare). |

## The Problem
Humans are terrible at remembering random strings of numbers. If you had to type `142.250.190.46` every time you wanted to search Google, the internet would be unusable. Furthermore, if Google changes their server IP, every user in the world would have to memorize the new number.

## How It Works
DNS provides an abstraction layer. You type `api.openai.com`. Your computer asks a DNS server, "What is the IP for this?" The DNS server responds with `162.159.140.232`. Your computer then makes the TCP connection directly to that IP. 

## Intuition
It is literally the Contacts app on your phone. You don't memorize your friend's 10-digit phone number. You just tap their name, and your phone looks up the number behind the scenes and dials it.

## Technical Explanation
DNS is a hierarchical, distributed database. 
1. Your computer checks its local cache.
2. If not found, it asks the Resolver (e.g., `8.8.8.8`).
3. The Resolver asks the Root Servers (who controls `.com`?).
4. It then asks the TLD servers (who controls `openai.com`?).
5. Finally, it asks the Authoritative Nameserver, which returns the exact IP.

## Example
Command line: `nslookup github.com` or `dig github.com` will return the A records (IP addresses) associated with GitHub.

## Python Implementation
See `dns_lookup.py` for a script using the `socket.gethostbyname()` function to programmatically resolve domains.

## What Happens Underneath
Your OS sends a UDP packet to port 53 of your configured DNS server containing the query. It waits for a UDP response. Because UDP isn't guaranteed, if the packet is lost, the OS will quietly retry a few times before failing.

## Common Mistakes
- **DNS Caching issues:** Changing an IP address on your server but wondering why your browser still goes to the old one (your OS caches DNS records for hours!).
- **Assuming DNS is instant:** A DNS lookup can take 20–100ms, which adds latency to API calls.

## Security Considerations
- **DNS Spoofing:** A hacker intercepts your DNS request and returns the IP of a fake banking website. 
- **DNS over HTTPS (DoH):** Modern browsers encrypt DNS queries so ISPs can't see which websites you are visiting.

## Real-World Applications
Load balancing! A high-traffic domain like `google.com` will return multiple different IP addresses so that user traffic is spread across hundreds of different servers globally.

## AI-Agent Connection
When your agent makes an API call to `api.anthropic.com`, the very first thing Python does under the hood is block the thread for 50ms to do a DNS lookup. If the DNS server goes down, your agent fails with a `socket.gaierror`, even if Anthropic's servers are perfectly healthy!

## Exercises
See `exercises.py`.

## Challenge
Use the `dnspython` library to query the TXT records of `google.com`.

## Summary
DNS translates human-readable domain names into IP addresses, providing a critical abstraction layer that allows servers to change IPs without breaking client applications.

## What You Should Know Before Moving On
You should understand that every HTTP request to a domain name requires a hidden DNS lookup first.
