# Module 24: Retries and Resilience - Solutions

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
