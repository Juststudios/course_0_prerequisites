"""
Module 25 Solutions: Asynchronous Concurrency in Python
=======================================================

Reference implementations for all 4 exercise levels.
"""

import asyncio
from typing import Any, Callable, Coroutine, List, Union


# ============================================================================
# Level 1: Recall Solution
# ============================================================================

async def gather_concurrent_fetch(ids: List[int], delay: float = 0.01) -> List[int]:
    """Fanns out concurrent fetch operations and gathers ordered results."""
    async def _fetch(item_id: int) -> int:
        await asyncio.sleep(delay)
        return item_id * 10

    coros = [_fetch(item_id) for item_id in ids]
    return await asyncio.gather(*coros)


# ============================================================================
# Level 2: Modify Solution
# ============================================================================

async def rate_limited_fetch(
    urls: List[str],
    max_concurrency: int = 2,
    delay: float = 0.01,
) -> List[str]:
    """Limits concurrent fetch requests using asyncio.Semaphore."""
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _fetch_url(url: str) -> str:
        async with semaphore:
            await asyncio.sleep(delay)
            return f"Data from {url}"

    coros = [_fetch_url(url) for url in urls]
    return await asyncio.gather(*coros)


# ============================================================================
# Level 3: Build Solution
# ============================================================================

async def producer_consumer_pipeline(
    items: List[str],
    num_workers: int = 2,
    delay: float = 0.005,
) -> List[str]:
    """Full asynchronous producer-consumer pipeline using asyncio.Queue."""
    queue: asyncio.Queue = asyncio.Queue()
    results: List[str] = []

    async def worker() -> None:
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            await asyncio.sleep(delay)
            results.append(f"{item}_processed")
            queue.task_done()

    # Spawn workers
    worker_tasks = [asyncio.create_task(worker()) for _ in range(num_workers)]

    # Produce all items
    for item in items:
        await queue.put(item)

    # Wait until all items have been processed
    await queue.join()

    # Send shutdown sentinel tokens to each worker
    for _ in range(num_workers):
        await queue.put(None)

    # Wait for workers to cleanly exit
    await asyncio.gather(*worker_tasks)

    return sorted(results)


# ============================================================================
# Level 4: Debug Solution
# ============================================================================

async def safe_concurrent_runner(
    factories: List[Callable[[], Coroutine[Any, Any, str]]]
) -> List[Union[str, str]]:
    """
    Fixed implementation: calls factories, unpacks into gather with return_exceptions=True,
    and maps caught exceptions to string representations.
    """
    coros = [fact() for fact in factories]
    raw_results = await asyncio.gather(*coros, return_exceptions=True)

    processed_results: List[str] = []
    for item in raw_results:
        if isinstance(item, Exception):
            processed_results.append(f"ERROR: {item}")
        else:
            processed_results.append(str(item))

    return processed_results


# ============================================================================
# Verification Tests
# ============================================================================

async def run_async_tests() -> None:
    print("Running Module 25 Verification Tests...")

    # Level 1 test
    l1_res = await gather_concurrent_fetch([1, 2, 3, 4], delay=0.01)
    assert l1_res == [10, 20, 30, 40], f"Level 1 failed: {l1_res}"
    print("  [✓] Level 1 (Recall: gather) passed.")

    # Level 2 test
    urls = ["api.agent.ai/a", "api.agent.ai/b", "api.agent.ai/c"]
    l2_res = await rate_limited_fetch(urls, max_concurrency=2, delay=0.01)
    assert l2_res == [f"Data from {u}" for u in urls], f"Level 2 failed: {l2_res}"
    print("  [✓] Level 2 (Modify: Semaphore) passed.")

    # Level 3 test
    items = ["task_x", "task_y", "task_z"]
    l3_res = await producer_consumer_pipeline(items, num_workers=2, delay=0.005)
    expected_l3 = sorted([f"{i}_processed" for i in items])
    assert l3_res == expected_l3, f"Level 3 failed: {l3_res}"
    print("  [✓] Level 3 (Build: Queue pipeline) passed.")

    # Level 4 test
    async def ok_task_1() -> str:
        return "Result A"

    async def failing_task() -> str:
        raise ValueError("Invalid parameters provided")

    async def ok_task_2() -> str:
        return "Result B"

    factories = [ok_task_1, failing_task, ok_task_2]
    l4_res = await safe_concurrent_runner(factories)
    assert l4_res[0] == "Result A"
    assert "ERROR: Invalid parameters provided" in l4_res[1]
    assert l4_res[2] == "Result B"
    print("  [✓] Level 4 (Debug: safe gather runner) passed.")

    print("All Module 25 exercise solutions verified successfully!\n")


def main() -> None:
    asyncio.run(run_async_tests())


if __name__ == "__main__":
    main()
