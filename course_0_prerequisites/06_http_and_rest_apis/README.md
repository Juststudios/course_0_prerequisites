# Module 06: HTTP, REST APIs, and Resilient Networking for AI Agents

## 1. Learning Objectives
By the end of this module, you will be able to:
- Construct robust asynchronous HTTP clients using modern libraries (`httpx` or `urllib`).
- Configure persistent connection pooling to eliminate TCP/TLS handshake overhead across LLM calls.
- Structure HTTP headers for security and observability (`Authorization: Bearer ...`, `User-Agent`, `X-Trace-ID`).
- Accurately interpret and handle HTTP status codes (200 OK, 400 Bad Request, 401 Unauthorized, 429 Rate Limited, 500 Server Error, 503 Unavailable).
- Implement exponential backoff retry algorithms with full jitter to recover from transient network drops and rate limits without triggering stampeding herd problems.

---

## 2. Why AI Agent Engineers Need This
Virtually every action in modern AI agent systems traverses the network:
- Sending inference prompts to OpenAI, Anthropic, or Hugging Face.
- Querying search engines (Google, Tavily, Bing).
- Calling internal microservices or executing webhooks.

Production networks are unreliable: connections drop, gateways timeout, and LLM providers frequently return HTTP 429 (Rate Limit Exceeded) during peak hours. An agent that crashes immediately upon receiving a single 429 or 503 is unusable. Production agent runtimes require resilient HTTP sessions with connection pooling and intelligent retry loops.

---

## 3. Structured Concept Breakdown

### Concept 1: HTTP Client Session & Connection Pooling
- **TERM**: HTTP Client Session & Connection Pooling
- **DEFINITION**: A persistent client object (`httpx.AsyncClient`) that manages a pool of underlying TCP and TLS socket connections, reusing them across sequential and concurrent requests.
- **INTUITION**: A direct dedicated phone hotline. Instead of hanging up and redialing the full international number and exchanging pleasantries every 10 seconds (TCP handshake + TLS negotiation), you keep the line open and immediately exchange messages.
- **WHY IT EXISTS**: Establishing a new TLS connection to an API server takes 100ms to 300ms of latency per request. Reusing established connections in a pool cuts round-trip time by up to 60%.
- **HOW IT WORKS**: The client maintains an internal queue of open socket descriptors. When a request finishes, the connection is returned to the pool rather than closed (`FIN`). The next request to the same host reuses that socket.
- **CODE**:
```python
import httpx

async def call_llm_api():
    # Persistent session reuses TCP/TLS connections
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            "https://api.example.com/v1/chat",
            json={"model": "gpt-4", "messages": [{"role": "user", "content": "Hi"}]}
        )
        return response.json()
```

---

### Concept 2: Request Headers & Authentication
- **TERM**: Request Headers
- **DEFINITION**: Key-value pairs transmitted at the beginning of an HTTP request that provide metadata about the payload format, client identity, authorization tokens, and tracing.
- **INTUITION**: The address label and customs declaration on a parcel. It tells the mail courier who sent the box, what credentials permit its entry, and what language is inside.
- **WHY IT EXISTS**: APIs reject unauthenticated requests. Setting `Authorization: Bearer <TOKEN>` provides identity. Setting `Content-Type: application/json` tells the server to parse the body as JSON. Setting `X-Request-ID` enables end-to-end distributed tracing.
- **HOW IT WORKS**: Headers are serialized as ASCII text lines separated by carriage return and line feed (`\r\n`) immediately preceding the request body.
- **CODE**:
```python
headers = {
    "Authorization": "Bearer sk-agent-secret-key",
    "Content-Type": "application/json",
    "User-Agent": "AutonomousAgentRuntime/1.0",
    "X-Trace-ID": "trace-uuid-12345"
}
```

---

### Concept 3: HTTP Status Codes
- **TERM**: HTTP Status Codes
- **DEFINITION**: Standardized 3-digit numerical responses indicating the status of the HTTP request.
- **INTUITION**: A traffic signal. Green (2xx) means proceed; yellow (4xx) means you made a mistake and must stop; red (5xx) means the road ahead is collapsed.
- **WHY IT EXISTS**: Agents must react differently depending on why a call failed:
  - `400 / 422`: Schema or prompt format invalid (self-correct prompt).
  - `401 / 403`: Invalid credentials (alert user immediately, do not retry).
  - `429`: Rate limit reached (back off and retry after delay).
  - `500 / 502 / 503`: Transient server error (retry with backoff).
- **HOW IT WORKS**: The first line of the HTTP response header contains the status code. The client checks `response.status_code` to branch logic.
- **CODE**:
```python
def handle_response_status(status_code: int):
    if status_code == 200:
        return "Success"
    elif status_code == 429:
        return "Rate Limited: Back off and retry."
    elif status_code in (500, 502, 503, 504):
        return "Server Error: Retryable."
    else:
        raise RuntimeError(f"Unrecoverable client error: {status_code}")
```

---

### Concept 4: Exponential Backoff with Jitter
- **TERM**: Exponential Backoff with Jitter
- **DEFINITION**: An algorithmic retry policy where the wait duration between failed attempts doubles exponentially ($t = \text{base} \times 2^{\text{attempt}}$) combined with a randomized offset ("jitter").
- **INTUITION**: Two people trying to enter a narrow doorway simultaneously. If both step back and wait exactly 1 second, they will collide again indefinitely. If both step back and wait a random fraction of a second, one slips through while the other waits.
- **WHY IT EXISTS**: When an API provider experiences a hiccup, thousands of client agents retry simultaneously. Without backoff and jitter, all agents retry at the exact same millisecond, hammering the provider and keeping it down ("stampeding herd" or "thundering herd" problem).
- **HOW IT WORKS**: Delay is calculated as:
  $$\text{delay} = \text{random.uniform}(0, \text{base\_delay} \times 2^{\text{attempt}})$$
  This spreads the load evenly across time.
- **CODE**:
```python
import random
import asyncio

async def retry_with_backoff(coro_fn, max_retries: int = 3, base_delay: float = 0.5):
    for attempt in range(max_retries):
        try:
            return await coro_fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            # Full Jitter Backoff
            delay = random.uniform(0, base_delay * (2 ** attempt))
            print(f"Attempt {attempt + 1} failed. Backing off for {delay:.2f}s...")
            await asyncio.sleep(delay)
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Retrying on 401/403 Errors
- **The Bug**: Writing a generic retry loop that catches all HTTP errors, including 401 Unauthorized or 403 Forbidden.
- **The Consequence**: If the user provides an invalid API key, the agent retries 5 times with backoff, freezing the UI for 30 seconds before finally delivering the error that was obvious on turn 1.
- **The Fix**: Check status codes before retrying; only retry on transient codes (`429`, `500`, `502`, `503`, `504`) and connection timeouts.

### Anti-Pattern 2: Missing Request Timeouts
- **The Bug**: Using `httpx.AsyncClient()` or `requests.get()` without setting an explicit `timeout`.
- **The Consequence**: A hanging remote server will cause the agent to hang indefinitely, keeping threads or task slots consumed until the entire agent cluster runs out of memory.
- **The Fix**: Always set explicit timeouts (`timeout=httpx.Timeout(10.0, connect=3.0)`).

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What HTTP status code signals "Too Many Requests"?
2. Why is "jitter" added to exponential backoff algorithms?
3. Which HTTP header indicates the MIME format of the request payload?

### Tier 2 (Debugging)
Find the flaw in this retry handler:
```python
def retry_request(url):
    for i in range(5):
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        time.sleep(1)  # What is wrong with fixed sleep without status checks?
```
*Hint*: If the response is 404 Not Found, sleeping 1s and retrying 5 times is completely pointless.

### Tier 3 (Application)
Write an async function `safe_post_json(url: str, payload: dict, auth_token: str, max_retries: int)` that sends a POST request with headers and retries up to `max_retries` times only on 429 and 503 using randomized exponential backoff.

### Tier 4 (Challenge)
Build a `ResilientLLMHTTPGateway` class that:
1. Manages an underlying `httpx.AsyncClient` session.
2. Intercepts `Retry-After` HTTP headers returned on 429 status codes and honors the server-requested wait time.
3. Records metrics on total requests, successful requests, retry counts, and average latency.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/06_http_and_rest_apis/rest_client.py
python3 course_0_prerequisites/06_http_and_rest_apis/resilient_session.py
```
