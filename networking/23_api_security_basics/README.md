# API Security Basics

## What You Will Learn
In this module, you will learn the foundational principles of API security beyond just authentication. You will explore common threats like Man-in-the-Middle (MitM) attacks, Injection, and Rate Limiting, and how to defend against them to build robust network services.

## Prerequisites
- Completion of Module 22: Authentication.
- Understanding of HTTP verbs, status codes, and headers.
- Basic knowledge of JSON and REST APIs.

## Key Terminology
- **HTTPS / TLS:** Transport Layer Security, which encrypts data in transit.
- **Man-in-the-Middle (MitM):** An attack where an adversary intercepts communication between a client and server.
- **Injection:** An attack where untrusted data is sent to an interpreter as part of a command or query.
- **Rate Limiting:** Restricting the number of requests a client can make in a given timeframe.
- **CORS (Cross-Origin Resource Sharing):** A security feature implemented by browsers to restrict how a web page can request resources from another domain.

## The Problem
APIs are the doors to your application's data and functionality. If left unsecured, attackers can overwhelm your servers (DDoS), steal sensitive information by listening on the network, or exploit poorly written code to manipulate your database. Simply adding a password is not enough.

## How It Works
API security relies on defense in depth:
1. **Encrypt Transit:** Using TLS (HTTPS) ensures that even if traffic is intercepted, it cannot be read or modified.
2. **Limit Exposure:** Rate limiting ensures that a single user cannot exhaust server resources.
3. **Validate Input:** Never trusting client input prevents injection attacks.
4. **Control Origin:** CORS headers tell the browser which domains are allowed to access the API.

## Intuition
Imagine a bank. Authentication is checking your ID at the door. API Security is ensuring that the armored truck transporting your money is bulletproof (HTTPS), making sure nobody can withdraw money faster than the tellers can process it (Rate Limiting), and checking that the withdrawal slips don't contain hidden instructions to empty the vault (Input Validation).

## Technical Explanation
- **HTTPS:** Operates at the Transport Layer. It uses public-key cryptography to establish a secure session key, which is then used for symmetric encryption of the HTTP traffic.
- **Rate Limiting:** Often implemented using algorithms like Token Bucket or Leaky Bucket. Servers track request counts per IP or API key and return a `429 Too Many Requests` status code when limits are exceeded.
- **Injection Defense:** Achieved through parameterized queries in databases, and strict schema validation for incoming JSON bodies.

## Example
A response from a rate-limited API might include specific headers:
```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1614553200

{
  "error": "Rate limit exceeded. Try again later."
}
```

## Python Implementation
```python
import requests
import time

def call_api_with_retry(url, headers):
    """A simple function to handle rate limiting responses."""
    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:
        print("Rate limit hit! Backing off...")
        # In a real app, read the X-RateLimit-Reset header
        time.sleep(5) 
        return requests.get(url, headers=headers)
        
    return response
```

## What Happens Underneath
1. **TLS Handshake:** Before HTTP data is sent, the client and server negotiate encryption algorithms and exchange keys.
2. **Middleware Execution:** As the request enters the server framework, security middleware executes. A rate limiter checks Redis/memory; a CORS middleware checks the `Origin` header.
3. **Controller Validation:** The application code validates the data types and lengths before interacting with the database.

## Common Mistakes
- **Disabling TLS Verification:** Writing `requests.get(url, verify=False)` completely defeats the purpose of HTTPS and opens you to MitM attacks.
- **Trusting Client Input:** Assuming that because your frontend validates a form, the API will only receive valid data. Attackers can bypass the frontend and hit the API directly.
- **Verbose Error Messages:** Returning database stack traces in 500 errors gives attackers valuable information about your backend structure.

## Security Considerations
- Validate EVERYTHING. Use libraries like Pydantic in Python to enforce strict schemas.
- Implement proper logging and monitoring to detect anomalous request patterns.
- Keep your dependencies and server software up to date to patch known vulnerabilities.

## Real-World Applications
- **Public APIs (Twitter, GitHub):** Heavily rely on rate limiting to ensure fair usage and prevent abuse.
- **Financial APIs (Plaid, Stripe):** Enforce strict TLS requirements and payload signing to guarantee data integrity.
- **Web Applications:** Use CORS to prevent malicious websites from making requests to APIs on behalf of a logged-in user.

## AI-Agent Connection
When writing AI agents that expose webhooks or interact with APIs, implementing rate-limiting prevents your agent from running up massive LLM bills due to an infinite loop or malicious abuse. Furthermore, validating all inputs before passing them to an LLM prevents Prompt Injection.

## Exercises
Complete the exercises in `exercises.py`.

## Challenge
Write a decorator in Python that implements a simple in-memory rate limiter, restricting a function to be called only 3 times per minute.

## Summary
API security requires a multi-layered approach. By enforcing HTTPS, implementing rate limiting, strictly validating inputs, and managing cross-origin requests, you can protect your systems from a wide array of common attacks.

## What You Should Know Before Moving On
- Why HTTPS is critical and how `verify=False` breaks it.
- How to interpret and handle a `429 Too Many Requests` response.
- The importance of input validation to prevent injection.
