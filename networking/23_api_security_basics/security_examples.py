import time

class RateLimiter:
    """A simple Token Bucket rate limiter simulation."""
    def __init__(self, capacity, refill_rate_per_sec):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate_per_sec
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now

    def allow_request(self):
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

if __name__ == "__main__":
    limiter = RateLimiter(capacity=3, refill_rate_per_sec=1)
    
    for i in range(5):
        if limiter.allow_request():
            print(f"Request {i+1}: Allowed")
        else:
            print(f"Request {i+1}: Denied (429 Too Many Requests)")
        time.sleep(0.2)
