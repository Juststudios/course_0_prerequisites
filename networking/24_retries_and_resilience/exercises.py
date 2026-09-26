# Module 24: Retries and Resilience - Exercises

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
