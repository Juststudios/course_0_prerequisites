"""
Module 25 Exercises: Asynchronous Concurrency in Python
=======================================================

Practice core asynchronous concurrency patterns:
- asyncio.gather for concurrent fan-out / fan-in.
- asyncio.Semaphore for concurrency throttling and rate limiting.
- asyncio.Queue for decoupled producer-consumer systems.
- Robust exception handling in concurrent execution.

Follow the instructions for each level. Replace `raise NotImplementedError`
with your solution.
"""

import asyncio
from typing import Any, Callable, Coroutine, List, Union


# ============================================================================
# Level 1: Recall
# ============================================================================

async def gather_concurrent_fetch(ids: List[int], delay: float = 0.01) -> List[int]:
    """
    Recall how to fan out concurrent coroutines with asyncio.gather.
    
    Requirements:
    1. Define an inner coroutine `_fetch(item_id: int) -> int` that awaits
       `asyncio.sleep(delay)` and returns `item_id * 10`.
    2. Launch all fetches concurrently across all numbers in `ids` using `asyncio.gather`.
    3. Return the collected list of integer results in the same order as `ids`.
    """
    # TODO: Implement concurrent fetch using asyncio.gather.
    raise NotImplementedError("Level 1: Implement gather_concurrent_fetch")


# ============================================================================
# Level 2: Modify
# ============================================================================

async def rate_limited_fetch(
    urls: List[str],
    max_concurrency: int = 2,
    delay: float = 0.01,
) -> List[str]:
    """
    Modify concurrent requests to respect a concurrency rate limit using asyncio.Semaphore.
    
    Requirements:
    1. Create an `asyncio.Semaphore(max_concurrency)`.
    2. For each URL in `urls`, run a worker that enters the semaphore context
       (`async with sem:`), awaits `asyncio.sleep(delay)`, and returns `f"Data from {url}"`.
    3. Run all requests concurrently with `asyncio.gather`.
    4. Return the list of fetched strings in their original order.
    """
    # TODO: Implement semaphore-governed concurrent fetch.
    raise NotImplementedError("Level 2: Implement rate_limited_fetch")


# ============================================================================
# Level 3: Build
# ============================================================================

async def producer_consumer_pipeline(
    items: List[str],
    num_workers: int = 2,
    delay: float = 0.005,
) -> List[str]:
    """
    Build a complete producer-consumer pipeline using asyncio.Queue.
    
    Requirements:
    1. Create an `asyncio.Queue` instance.
    2. Create a shared list `results: List[str] = []`.
    3. Define a worker coroutine `worker()`:
       - Loops indefinitely reading items from the queue with `await queue.get()`.
       - If item is `None` (sentinel shutdown signal), acknowledge with `queue.task_done()` and break.
       - Awaits `asyncio.sleep(delay)` to simulate processing.
       - Appends `f"{item}_processed"` to `results`.
       - Acknowledges item with `queue.task_done()`.
    4. Spawn `num_workers` worker tasks using `asyncio.create_task()`.
    5. Put each item from `items` into the queue with `await queue.put(item)`.
    6. Wait for all queue items to be processed using `await queue.join()`.
    7. Send sentinel `None` to each worker, and await all worker tasks to complete.
    8. Return `sorted(results)`.
    """
    # TODO: Build full producer-consumer queue pipeline.
    raise NotImplementedError("Level 3: Implement producer_consumer_pipeline")


# ============================================================================
# Level 4: Debug
# ============================================================================

async def safe_concurrent_runner(
    factories: List[Callable[[], Coroutine[Any, Any, str]]]
) -> List[Union[str, str]]:
    """
    DEBUG CHALLENGE:
    The following function is supposed to invoke a list of coroutine factory functions,
    run them concurrently, and safely return the results. If any coroutine raises
    an exception, instead of crashing the entire batch, it should convert the exception
    to an error string: `f"ERROR: {exc}"`.
    
    However, the buggy implementation has multiple flaws:
    1. It passes factory functions instead of calling them to produce coroutines.
    2. It calls `asyncio.gather(coros)` without unpacking `*coros`.
    3. It fails to use `return_exceptions=True`, causing uncaught errors to abort the batch.
    
    Fix the bugs and ensure all results/error strings are returned.
    """
    # BUGGY CODE:
    # coros = factories  # BUG 1: Didn't invoke factories to create coroutines!
    # raw_results = await asyncio.gather(coros)  # BUG 2: Missing * unpack and return_exceptions=True!
    # return raw_results

    # TODO: Fix the bugs and return results, mapping any Exception e to f"ERROR: {e}".
    raise NotImplementedError("Level 4: Debug safe_concurrent_runner")
