"""
Module 24 Exercises: Introduction to Asynchronous Python
=======================================================

Practice foundational asynchronous Python concepts: coroutines, awaiting,
error handling, and async iteration.

Follow the instructions for each level. Replace `raise NotImplementedError`
with your solution.
"""

import asyncio
from typing import Any, Callable, Coroutine, List


# ============================================================================
# Level 1: Recall
# ============================================================================

async def async_add(a: int, b: int, delay: float = 0.01) -> int:
    """
    Recall how to write and execute a basic coroutine.
    
    Requirements:
    1. Await `asyncio.sleep(delay)` to yield control to the event loop.
    2. Return the sum of `a` and `b`.
    """
    # TODO: Implement coroutine with non-blocking sleep and addition.
    raise NotImplementedError("Level 1: Implement async_add")


# ============================================================================
# Level 2: Modify
# ============================================================================

async def async_retry(
    coro_func: Callable[[], Coroutine[Any, Any, str]],
    max_retries: int = 3,
    delay: float = 0.01,
) -> str:
    """
    Modify an async caller to include retry logic.
    
    Requirements:
    1. Attempt to invoke and await `coro_func()`.
    2. If it raises an Exception, catch it. If attempts remain (less than max_retries),
       await `asyncio.sleep(delay)` and try again.
    3. If all `max_retries` attempts fail, re-raise the final exception encountered.
    4. Return the successful result string if any attempt succeeds.
    """
    # TODO: Modify call with retry loop and async sleep delay.
    raise NotImplementedError("Level 2: Implement async_retry")


# ============================================================================
# Level 3: Build
# ============================================================================

async def async_pipeline(values: List[int], factor: int) -> List[int]:
    """
    Build a two-stage sequential async transformation pipeline.
    
    Requirements:
    1. For each number in `values`:
       a. Stage 1: Coroutine adds 10 to the number (simulates validation/enrichment)
          after awaiting `asyncio.sleep(0.005)`.
       b. Stage 2: Coroutine multiplies the result by `factor` (simulates calculation)
          after awaiting `asyncio.sleep(0.005)`.
    2. Return the list of final processed numbers in their original order.
    
    Example:
        async_pipeline([1, 2, 3], factor=2)
        -> [(1+10)*2, (2+10)*2, (3+10)*2]
        -> [22, 24, 26]
    """
    # TODO: Build two-stage async processing pipeline.
    raise NotImplementedError("Level 3: Implement async_pipeline")


# ============================================================================
# Level 4: Debug
# ============================================================================

async def collect_timestamps(count: int, interval: float = 0.01) -> List[int]:
    """
    DEBUG CHALLENGE:
    The following coroutine is intended to collect `count` integer sequence numbers,
    pausing for `interval` seconds between each item.
    
    However, it contains serious bugs:
    1. It calls `asyncio.sleep` without `await` (creating unawaited coroutine warnings).
    2. It forgets to return the accumulated result list.
    
    Fix the implementation so it correctly awaits the sleep and returns the list.
    """
    # BUGGY CODE:
    # results = []
    # for i in range(count):
    #     asyncio.sleep(interval)  # BUG: Missing await!
    #     results.append(i)
    # # BUG: Missing return statement!

    # TODO: Fix the bugs and return the list of collected indices [0, 1, ..., count - 1].
    raise NotImplementedError("Level 4: Debug collect_timestamps")
