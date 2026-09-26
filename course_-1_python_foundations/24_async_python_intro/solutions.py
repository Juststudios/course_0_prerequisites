"""
Module 24 Solutions: Introduction to Asynchronous Python
=======================================================

Reference solutions for all 4 exercise levels.
"""

import asyncio
from typing import Any, Callable, Coroutine, List


# ============================================================================
# Level 1: Recall Solution
# ============================================================================

async def async_add(a: int, b: int, delay: float = 0.01) -> int:
    """Awaits a non-blocking delay and returns a + b."""
    await asyncio.sleep(delay)
    return a + b


# ============================================================================
# Level 2: Modify Solution
# ============================================================================

async def async_retry(
    coro_func: Callable[[], Coroutine[Any, Any, str]],
    max_retries: int = 3,
    delay: float = 0.01,
) -> str:
    """Retries an async operation up to max_retries with non-blocking delays."""
    last_error: Exception = RuntimeError("No attempts executed")
    
    for attempt in range(1, max_retries + 1):
        try:
            result = await coro_func()
            return result
        except Exception as exc:
            last_error = exc
            if attempt < max_retries:
                await asyncio.sleep(delay)
                
    raise last_error


# ============================================================================
# Level 3: Build Solution
# ============================================================================

async def _stage_one_add_ten(n: int) -> int:
    await asyncio.sleep(0.005)
    return n + 10


async def _stage_two_multiply(n: int, factor: int) -> int:
    await asyncio.sleep(0.005)
    return n * factor


async def async_pipeline(values: List[int], factor: int) -> List[int]:
    """Processes each value sequentially through two async stages."""
    results: List[int] = []
    for val in values:
        intermediate = await _stage_one_add_ten(val)
        final_val = await _stage_two_multiply(intermediate, factor)
        results.append(final_val)
    return results


# ============================================================================
# Level 4: Debug Solution
# ============================================================================

async def collect_timestamps(count: int, interval: float = 0.01) -> List[int]:
    """Corrected implementation: properly awaits asyncio.sleep and returns list."""
    results: List[int] = []
    for i in range(count):
        await asyncio.sleep(interval)
        results.append(i)
    return results


# ============================================================================
# Verification Tests
# ============================================================================

async def run_async_tests() -> None:
    print("Running Module 24 Async Verification Tests...")
    
    # Level 1 test
    res_l1 = await async_add(15, 27, delay=0.01)
    assert res_l1 == 42, f"Expected 42, got {res_l1}"
    print("  [✓] Level 1 (Recall) passed.")
    
    # Level 2 test: succeeding after 2 failures
    attempts = 0
    async def flaky_call() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionResetError(f"Temporary network failure #{attempts}")
        return "Success from remote server"
        
    res_l2 = await async_retry(flaky_call, max_retries=4, delay=0.01)
    assert res_l2 == "Success from remote server"
    assert attempts == 3
    print("  [✓] Level 2 (Modify) passed.")
    
    # Level 3 test
    res_l3 = await async_pipeline([1, 2, 3], factor=2)
    assert res_l3 == [22, 24, 26], f"Expected [22, 24, 26], got {res_l3}"
    print("  [✓] Level 3 (Build) passed.")
    
    # Level 4 test
    res_l4 = await collect_timestamps(4, interval=0.005)
    assert res_l4 == [0, 1, 2, 3], f"Expected [0, 1, 2, 3], got {res_l4}"
    print("  [✓] Level 4 (Debug) passed.")
    
    print("All Module 24 exercise solutions verified successfully!\n")


def main() -> None:
    asyncio.run(run_async_tests())


if __name__ == "__main__":
    main()
