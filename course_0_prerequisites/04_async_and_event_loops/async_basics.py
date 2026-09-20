"""async_basics.py - Demonstrates coroutines, event loops, and sequential vs concurrent latency.

Key concepts demonstrated:
1. Defining and awaiting coroutines.
2. Comparing sequential await vs concurrent asyncio.gather.
3. Thread offloading for synchronous blocking functions via asyncio.to_thread.
"""

import asyncio
import time
from typing import List, Tuple


async def simulated_llm_inference(prompt: str, delay_seconds: float = 0.05) -> str:
    """Simulates an asynchronous LLM generation call."""
    await asyncio.sleep(delay_seconds)
    return f"Response to '{prompt}' [tokens={len(prompt.split()) * 3}]"


def blocking_cpu_task(n: int) -> int:
    """Simulates a blocking CPU-bound operation that would freeze the event loop."""
    time.sleep(0.05)
    return sum(i * i for i in range(n))


async def run_sequential(prompts: List[str]) -> Tuple[List[str], float]:
    """Runs a batch of prompts sequentially."""
    start = time.perf_counter()
    results = []
    for p in prompts:
        res = await simulated_llm_inference(p, delay_seconds=0.03)
        results.append(res)
    elapsed = time.perf_counter() - start
    return results, elapsed


async def run_concurrent(prompts: List[str]) -> Tuple[List[str], float]:
    """Runs a batch of prompts concurrently using asyncio.gather."""
    start = time.perf_counter()
    tasks = [simulated_llm_inference(p, delay_seconds=0.03) for p in prompts]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    return list(results), elapsed


async def main_async() -> None:
    print("=== Module 04: Async Basics & Event Loop Demo ===")

    prompts = [
        "Summarize article 1",
        "Summarize article 2",
        "Summarize article 3",
        "Summarize article 4",
    ]

    # 1. Compare Sequential vs Concurrent
    seq_results, seq_time = await run_sequential(prompts)
    print(f"Sequential Execution: {len(seq_results)} tasks took {seq_time:.3f}s")

    conc_results, conc_time = await run_concurrent(prompts)
    print(f"Concurrent Execution: {len(conc_results)} tasks took {conc_time:.3f}s")

    assert len(seq_results) == len(conc_results) == 4
    # Concurrent should be noticeably faster (roughly 4x speedup)
    speedup = seq_time / conc_time
    print(f"Concurrency Speedup factor: {speedup:.2f}x")
    assert conc_time < seq_time * 0.75, "Concurrent execution should be substantially faster than sequential"

    # 2. Test offloading blocking work via asyncio.to_thread
    start_thread = time.perf_counter()
    cpu_result = await asyncio.to_thread(blocking_cpu_task, 1000)
    thread_time = time.perf_counter() - start_thread
    assert cpu_result > 0
    print(f"[OK] asyncio.to_thread safely executed blocking CPU task in {thread_time:.3f}s")

    print("All tests in async_basics.py completed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main_async())
