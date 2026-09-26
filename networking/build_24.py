import os

module_dir = "/home/settings/Documents/pearl/networking/24_retries_and_resilience"

readme_content = """# Retries and Resilience

## What You Will Learn
In this module, you will learn how to make your networked applications robust against transient failures. You will understand how to implement retries, exponential backoff, and jitter to ensure your system recovers gracefully from temporary network hiccups without overwhelming the servers.

## Prerequisites
- Completion of previous networking modules.
- Understanding of HTTP status codes (especially 5xx server errors).
- Basic Python programming.

## Key Terminology
- **Transient Failure:** A temporary error that might resolve itself if the request is retried (e.g., a momentary network drop).
- **Retry:** Attempting a failed operation again.
- **Backoff:** Waiting for a certain amount of time before retrying.
- **Exponential Backoff:** Increasing the wait time exponentially with each retry attempt.
- **Jitter:** Adding randomness to the backoff time to prevent a "thundering herd" problem.
- **Idempotency:** A property where making the same request multiple times has the same effect as making it once.

## The Problem
Networks are fundamentally unreliable. Packets drop, routers reboot, and servers temporarily overload. If your application crashes or fails a core workflow because of a single dropped HTTP request, it is brittle. However, simply retrying immediately and continuously can act like a self-inflicted DDoS attack, bringing down a struggling server.

## How It Works
When an HTTP client encounters a transient error (like a 503 Service Unavailable or a network timeout), it catches the exception. Instead of failing immediately, it waits for a short period and tries again. If it fails again, it waits longer (exponential backoff) and adds some randomness to the wait time (jitter).

## Intuition
Imagine calling a busy restaurant to make a reservation. If you get a busy signal and redial instantly and repeatedly, you and everyone else doing the same thing will jam the phone lines. If instead you wait 1 minute, then 2 minutes, then 4 minutes, and add a few random seconds so you aren't calling at the exact same time as someone else, you give the restaurant time to handle existing calls.

## Technical Explanation
A robust retry strategy typically looks like this:
1. Identify if the error is retryable. Network timeouts, connection resets, and 5xx HTTP status codes are usually retryable. 4xx codes (like 400 Bad Request or 401 Unauthorized) usually are NOT retryable because the request itself is flawed.
2. If retryable, wait `base_delay * (2 ^ attempt)`.
3. Add a random variation: `wait = wait + random(0, wait * jitter_factor)`.
4. Retry the request.
5. Stop after a maximum number of attempts or a maximum total duration.

**Crucial Warning:** Only retry operations that are *idempotent* (like GET requests or PUT requests). Retrying a non-idempotent operation (like a POST request that charges a credit card) without specific idempotency keys can result in double-charging!

## Example
If you set a base delay of 1 second and a max of 3 retries:
- Attempt 1: Fails. Wait 1s + jitter.
- Attempt 2: Fails. Wait 2s + jitter.
- Attempt 3: Fails. Wait 4s + jitter.
- Attempt 4: Fails. Abort and raise error.

## Python Implementation
```python
import time
import random
import requests
from requests.exceptions import RequestException

def request_with_retry(url, max_retries=3, base_delay=1):
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, timeout=5)
            # Raise an HTTPError for bad responses (4xx, 5xx)
            response.raise_for_status()
            return response
        except RequestException as e:
            # Check if we should retry (e.g. 5xx errors or connection errors)
            # In a robust implementation, we'd specifically check the status code
            if attempt == max_retries:
                print(f"Max retries reached. Failing: {e}")
                raise
            
            # Calculate exponential backoff with jitter
            delay = (base_delay * (2 ** attempt)) 
            jitter = random.uniform(0, 0.1 * delay) # 10% jitter
            sleep_time = delay + jitter
            
            print(f"Attempt {attempt + 1} failed. Retrying in {sleep_time:.2f}s...")
            time.sleep(sleep_time)

# requests.packages.urllib3.util.retry.Retry is often better for production!
```

## What Happens Underneath
When a retry loop executes, the calling thread blocks during the `time.sleep()`. In asynchronous systems, `asyncio.sleep()` is used to yield control back to the event loop, allowing other tasks to run while waiting. The underlying TCP socket is typically torn down and recreated for the new attempt, though connection pooling libraries might try to reuse an open connection if the failure was at the HTTP layer rather than the transport layer.

## Common Mistakes
- **Retrying Everything:** Retrying a 404 Not Found or a 400 Bad Request wastes time. Retrying a non-idempotent POST can cause data corruption or duplicate transactions.
- **No Backoff:** "Spin-looping" (retrying immediately) will quickly exhaust CPU or network resources and overwhelm the server.
- **Missing Jitter:** In a distributed system, if thousands of clients experience a failure simultaneously and use the exact same backoff formula, they will all retry at the exact same moment, causing a "thundering herd."

## Security Considerations
- Retries can amplify the impact of an application bug into a Denial of Service (DoS) attack against your own infrastructure.
- Malicious actors can observe retry behavior to understand system timeouts and thresholds.

## Real-World Applications
- **Microservices:** Service-to-service communication relies heavily on retries to handle temporary network partitions or container restarts.
- **Cloud SDKs:** AWS (Boto3) and Google Cloud SDKs have built-in exponential backoff and retry logic for almost all API calls.
- **Mobile Apps:** Dealing with spotty cell service requires robust retry queues for background data syncing.

## AI-Agent Connection
AI agents making LLM API calls must handle rate limits (429) and server overloads (503). Implementing exponential backoff allows the agent to patiently wait for the API to recover instead of crashing or hallucinating an error state.

## Exercises
Complete the exercises in `exercises.py`.

## Challenge
Use the `tenacity` Python library to implement a retry decorator that retries only on `requests.exceptions.Timeout`, with an exponential backoff maxing out at 10 seconds.

## Summary
Resilience in networking acknowledges that failures will happen. By implementing intelligent retry mechanisms with exponential backoff and jitter, you transform fatal errors into brief delays, creating robust, production-grade applications.

## What You Should Know Before Moving On
- What a transient error is.
- Why you must only retry idempotent operations.
- The formula and rationale for exponential backoff and jitter.
"""

exercises_content = """# Module 24: Retries and Resilience - Exercises

# Tier 1: Recall
# 1. What do we call the technique of adding randomness to a wait time to prevent the "thundering herd" problem?
# TODO: Write your answer as a string.
randomness_technique = ""

# 2. Is a 400 Bad Request typically considered a transient, retryable error? (True/False)
# TODO: Write your answer as a boolean.
is_400_retryable = None


# Tier 2: Modify
import time

def simple_retry(func):
    # TODO: Modify this function so that it implements a basic backoff.
    # On the first failure, wait 1 second. On the second, wait 2 seconds. On the third, wait 3 seconds.
    # Currently it waits 1 second every time.
    for attempt in range(3):
        try:
            return func()
        except Exception:
            time.sleep(1)
    return func()


# Tier 3: Build
import random

def calc_backoff_with_jitter(attempt, base_delay=2):
    # TODO: Build a function that calculates the sleep time.
    # The exponential part should be: base_delay * (2 ^ attempt)
    # Then, add a random jitter between 0 and 1.0 seconds.
    # Return the final float value.
    pass


# Tier 4: Debug
def idempotent_retry(request_func, method):
    # TODO: This retry logic is dangerous. It retries EVERYTHING.
    # Fix it so it ONLY retries if the HTTP method is considered idempotent
    # (For this exercise, consider GET, PUT, and DELETE as idempotent, but NOT POST).
    
    # Buggy code:
    for _ in range(3):
        try:
            return request_func(method)
        except Exception:
            pass
    return request_func(method)
"""

solutions_content = """# Module 24: Retries and Resilience - Solutions

# Tier 1: Recall
randomness_technique = "jitter"
is_400_retryable = False

# Tier 2: Modify
import time

def simple_retry(func):
    for attempt in range(3):
        try:
            return func()
        except Exception:
            # Fix: Wait `attempt + 1` seconds
            time.sleep(attempt + 1)
    return func()

# Tier 3: Build
import random

def calc_backoff_with_jitter(attempt, base_delay=2):
    exponential_backoff = base_delay * (2 ** attempt)
    jitter = random.uniform(0, 1.0)
    return exponential_backoff + jitter

# Tier 4: Debug
def idempotent_retry(request_func, method):
    idempotent_methods = ["GET", "PUT", "DELETE"]
    
    # Fix: Check if method is idempotent before retrying
    if method.upper() not in idempotent_methods:
        return request_func(method)
        
    for _ in range(3):
        try:
            return request_func(method)
        except Exception:
            pass
    return request_func(method)
"""

impl_content = """import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_resilient_session():
    \"\"\"
    Creates a requests Session that automatically handles retries,
    exponential backoff, and connection pooling. This is the recommended
    way to handle retries in production Python applications.
    \"\"\"
    session = requests.Session()
    
    # Define the retry strategy
    retry_strategy = Retry(
        total=3, # Total number of retries
        backoff_factor=1, # wait 1, 2, 4 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504], # Status codes to retry on
        allowed_methods=["HEAD", "GET", "OPTIONS", "PUT", "DELETE"] # Idempotent methods
    )
    
    # Create an adapter with the strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # Mount it for both http and https
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

if __name__ == "__main__":
    session = create_resilient_session()
    print("Session created. If you use session.get('http://httpbin.org/status/503'), it will retry automatically.")
    
    # Uncomment to test (it will take a few seconds as it backs off)
    # try:
    #     response = session.get("http://httpbin.org/status/503")
    # except requests.exceptions.RetryError as e:
    #     print("Failed after all retries.")
"""

with open(os.path.join(module_dir, "README.md"), "w") as f:
    f.write(readme_content)

with open(os.path.join(module_dir, "exercises.py"), "w") as f:
    f.write(exercises_content)

with open(os.path.join(module_dir, "solutions.py"), "w") as f:
    f.write(solutions_content)

with open(os.path.join(module_dir, "resilient_client.py"), "w") as f:
    f.write(impl_content)

print("Module 24 generated successfully.")
