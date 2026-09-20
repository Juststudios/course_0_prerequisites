"""resilient_session.py - Demonstrates exponential backoff with jitter on transient HTTP errors.

Key concepts demonstrated:
1. Exponential backoff formula: delay = min(max_delay, base_delay * (2 ** attempt)) + jitter.
2. Handling HTTP 429 and 503 errors while failing fast on 400/401.
3. Automated simulation of recovering from temporary rate-limiting.
"""

import asyncio
import random
import time
from typing import Dict, Any, Callable, Awaitable


class TransientFaultSimulator:
    """Simulates an API endpoint that fails with 429/503 before succeeding."""

    def __init__(self, fail_count: int = 2, failure_code: int = 429) -> None:
        self.fail_count = fail_count
        self.failure_code = failure_code
        self.calls = 0

    async def call(self, prompt: str) -> Dict[str, Any]:
        self.calls += 1
        if self.calls <= self.fail_count:
            if self.failure_code == 429:
                raise RuntimeError("HTTP 429: Too Many Requests (Rate limit hit)")
            elif self.failure_code == 503:
                raise RuntimeError("HTTP 503: Service Unavailable")
        return {"status": 200, "prompt": prompt, "result": "Generated response successfully"}


async def execute_with_exponential_backoff(
    action: Callable[[], Awaitable[Dict[str, Any]]],
    max_retries: int = 4,
    base_delay: float = 0.02,
    max_delay: float = 0.5,
) -> Dict[str, Any]:
    """Retries an async callable using exponential backoff with full jitter."""
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            return await action()
        except RuntimeError as e:
            last_error = e
            err_msg = str(e)

            # Only retry transient errors
            if "429" not in err_msg and "503" not in err_msg:
                raise e

            if attempt == max_retries - 1:
                break

            # Calculate exponential backoff with jitter
            raw_backoff = min(max_delay, base_delay * (2 ** attempt))
            jittered_delay = random.uniform(0.0, raw_backoff)

            print(
                f"[RETRY] Attempt {attempt + 1} encountered: '{err_msg}'. "
                f"Backing off for {jittered_delay*1000:.1f}ms..."
            )
            await asyncio.sleep(jittered_delay)

    raise RuntimeError(f"Failed after {max_retries} attempts. Last error: {last_error}")


async def main() -> None:
    print("=== Module 06: Resilient Session & Exponential Backoff Demo ===")

    # 1. Test recovery from 2 transient 429 errors
    simulator = TransientFaultSimulator(fail_count=2, failure_code=429)

    start = time.perf_counter()
    response = await execute_with_exponential_backoff(
        lambda: simulator.call("Generate agent summary"),
        max_retries=4,
        base_delay=0.03
    )
    elapsed = time.perf_counter() - start

    assert response["status"] == 200
    assert simulator.calls == 3, f"Expected 3 calls (2 failures + 1 success), got {simulator.calls}"
    print(f"[OK] Successfully recovered from 429 rate limit in {elapsed:.3f}s. Calls: {simulator.calls}")

    # 2. Test non-retryable error (should fail immediately without retries)
    async def failing_action():
        raise RuntimeError("HTTP 401: Unauthorized API key")

    fail_sim_calls = 0
    async def counting_failing_action():
        nonlocal fail_sim_calls
        fail_sim_calls += 1
        await failing_action()

    try:
        await execute_with_exponential_backoff(counting_failing_action, max_retries=3)
        raise AssertionError("Should have raised error immediately")
    except RuntimeError as err:
        assert "401" in str(err)
        assert fail_sim_calls == 1, f"Non-retryable 401 should only be called once, got {fail_sim_calls}"
        print("[OK] Fast-fail on non-retryable 401 verified without wasted retries.")

    print("All tests in resilient_session.py passed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
