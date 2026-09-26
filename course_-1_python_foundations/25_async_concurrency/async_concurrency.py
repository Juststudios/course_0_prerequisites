"""
Module 25: Asynchronous Concurrency in Python
=============================================

This lesson builds on Module 24 (coroutine basics) to explore true asynchronous
concurrency using Python's asyncio framework.

While coroutines allow execution to pause during I/O waits, executing them
sequentially still causes total execution time to equal the sum of all individual
delays. Asynchronous concurrency allows multiple tasks to be in flight simultaneously
over a single OS thread.

Key Topics Covered:
-------------------
1. Creating background tasks with `asyncio.create_task()`.
2. Fanning out and aggregating results with `asyncio.gather()`.
3. Structured Concurrency using Python 3.11+ `asyncio.TaskGroup()`.
4. Enforcing deadlines with `asyncio.wait_for()` and timeout handling.
5. Controlling resource access and rate limits with `asyncio.Semaphore`.
6. Decoupled asynchronous worker queues with `asyncio.Queue`.
7. Real-world AI Agent application: Parallel multi-tool calling orchestrator.
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Section 1: Background Tasks with asyncio.create_task()
# ============================================================================

async def heartbeat_sensor(sensor_id: str, interval: float, ticks: int) -> List[str]:
    """Simulates an IoT sensor emitting periodic telemetry pulses."""
    readings = []
    for tick in range(1, ticks + 1):
        await asyncio.sleep(interval)
        reading = f"[{sensor_id}] tick={tick} at {time.strftime('%X')}"
        readings.append(reading)
    return readings


async def demonstrate_create_task() -> None:
    """
    Demonstrates scheduling coroutines as independent background tasks.
    
    When `create_task()` is called, the coroutine is wrapped in a Task and
    scheduled on the event loop immediately, allowing the caller to perform
    other work while the background task is running.
    """
    print("=" * 70)
    print("1. BACKGROUND TASKS (asyncio.create_task)")
    print("=" * 70)

    # Schedule background sensor task
    t0 = time.perf_counter()
    task = asyncio.create_task(heartbeat_sensor("ThermalSensorA", 0.05, 3))
    
    # Caller performs intermediate work while sensor runs in background
    print(f"Task scheduled (task done? {task.done()})")
    await asyncio.sleep(0.08)  # Let sensor run partially
    print(f"Main coroutine active... (task done? {task.done()})")
    
    # Await final result of the background task
    results = await task
    elapsed = time.perf_counter() - t0
    print(f"Background task finished in {elapsed:.2f}s with {len(results)} readings:")
    for r in results:
        print(f"   {r}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 2: Fan-Out and Fan-In with asyncio.gather()
# ============================================================================

async def query_knowledge_base(source: str, delay: float, should_fail: bool = False) -> Dict[str, Any]:
    """Simulates querying an external document repository or web search index."""
    await asyncio.sleep(delay)
    if should_fail:
        raise ConnectionError(f"Remote server unreachable: {source}")
    return {"source": source, "latency": delay, "status": "200_OK"}


async def demonstrate_gather() -> None:
    """
    Demonstrates fanning out multiple asynchronous requests concurrently.
    
    With `asyncio.gather(*coros)`, all coroutines run concurrently. The total
    execution time is governed by the slowest task rather than the sum of all tasks.
    """
    print("=" * 70)
    print("2. CONCURRENT FAN-OUT / FAN-IN (asyncio.gather)")
    print("=" * 70)

    sources = [
        ("VectorDB", 0.10),
        ("WebIndex", 0.12),
        ("SQLArchive", 0.08),
    ]

    t0 = time.perf_counter()
    coros = [query_knowledge_base(name, delay) for name, delay in sources]
    
    # Run all queries concurrently
    results = await asyncio.gather(*coros)
    elapsed = time.perf_counter() - t0

    print(f"All {len(results)} sources queried concurrently in {elapsed:.2f}s (max latency: 0.12s):")
    for res in results:
        print(f"   Source: {res['source']:<12} Latency: {res['latency']:.2f}s Status: {res['status']}")

    # Demonstrating gather with error handling (return_exceptions=True)
    print("\nDemonstrating resilient gather (return_exceptions=True):")
    resilient_coros = [
        query_knowledge_base("PrimaryAPI", 0.05, should_fail=False),
        query_knowledge_base("FlakyAPI", 0.06, should_fail=True),
        query_knowledge_base("BackupAPI", 0.04, should_fail=False),
    ]
    mixed_results = await asyncio.gather(*resilient_coros, return_exceptions=True)
    for idx, item in enumerate(mixed_results, start=1):
        if isinstance(item, Exception):
            print(f"   Task {idx}: Caught error: {type(item).__name__} -> {item}")
        else:
            print(f"   Task {idx}: Success: {item['source']}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 3: Structured Concurrency with asyncio.TaskGroup (Python 3.11+)
# ============================================================================

async def fetch_document(doc_id: int, latency: float) -> str:
    """Simulates fetching an individual document record."""
    await asyncio.sleep(latency)
    return f"Doc_{doc_id}_Content"


async def demonstrate_task_group() -> None:
    """
    Demonstrates structured concurrency via `asyncio.TaskGroup`.
    
    TaskGroup guarantees that all spawned tasks are properly joined before exiting
    the `async with` block. If any child task raises an exception, all other active
    tasks in the group are immediately cancelled, preventing leaked tasks.
    """
    print("=" * 70)
    print("3. STRUCTURED CONCURRENCY (asyncio.TaskGroup)")
    print("=" * 70)

    t0 = time.perf_counter()
    tasks = []

    async with asyncio.TaskGroup() as tg:
        for doc_id in range(101, 105):
            # Create tasks within the structured group context
            t = tg.create_task(fetch_document(doc_id, 0.06))
            tasks.append(t)
    
    # Upon exiting the block, all tasks are guaranteed complete and successful
    elapsed = time.perf_counter() - t0
    print(f"TaskGroup finished in {elapsed:.2f}s. Extracted results:")
    for t in tasks:
        print(f"   Result: {t.result()}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 4: Deadlines and Timeouts with asyncio.wait_for()
# ============================================================================

async def slow_remote_calculation(duration: float) -> str:
    """Simulates a complex mathematical or LLM inference task."""
    await asyncio.sleep(duration)
    return "Computation Complete"


async def demonstrate_timeouts() -> None:
    """
    Demonstrates enforcing execution deadlines using `asyncio.wait_for()`.
    
    If the operation exceeds the timeout limit, asyncio cancels the coroutine
    and raises `asyncio.TimeoutError`.
    """
    print("=" * 70)
    print("4. DEADLINES & TIMEOUTS (asyncio.wait_for)")
    print("=" * 70)

    # 1. Operation completing within deadline
    try:
        fast_res = await asyncio.wait_for(slow_remote_calculation(0.04), timeout=0.10)
        print(f"Fast calculation succeeded: {fast_res}")
    except asyncio.TimeoutError:
        print("Calculation timed out unexpectedly!")

    # 2. Operation exceeding deadline
    try:
        print("Starting slow calculation (requires 0.15s, timeout 0.05s)...")
        await asyncio.wait_for(slow_remote_calculation(0.15), timeout=0.05)
        print("Slow calculation completed (unexpected)!")
    except asyncio.TimeoutError:
        print("Caught asyncio.TimeoutError: Operation aborted because deadline was exceeded.")
    print("-" * 70 + "\n")


# ============================================================================
# Section 5: Rate Limiting with asyncio.Semaphore
# ============================================================================

async def call_rate_limited_api(
    client_id: int,
    semaphore: asyncio.Semaphore,
    active_counter: List[int],
) -> str:
    """Accesses a rate-limited external service protected by an asyncio semaphore."""
    async with semaphore:
        # Inside this context, at most semaphore._value tasks are concurrent
        active_counter[0] += 1
        current_active = active_counter[0]
        await asyncio.sleep(0.05)
        active_counter[0] -= 1
        return f"Client {client_id:02d} processed (peak concurrency observed: {current_active})"


async def demonstrate_semaphore() -> None:
    """
    Demonstrates limiting concurrent requests to prevent API rate limit bans.
    """
    print("=" * 70)
    print("5. RATE LIMITING WITH SEMAPHORE (asyncio.Semaphore)")
    print("=" * 70)

    max_concurrent = 2
    sem = asyncio.Semaphore(max_concurrent)
    active_counter = [0]
    num_requests = 6

    t0 = time.perf_counter()
    coros = [call_rate_limited_api(i, sem, active_counter) for i in range(1, num_requests + 1)]
    results = await asyncio.gather(*coros)
    elapsed = time.perf_counter() - t0

    print(f"Processed {num_requests} requests with max concurrency {max_concurrent} in {elapsed:.2f}s:")
    for res in results:
        print(f"   {res}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 6: Producer-Consumer Queues with asyncio.Queue
# ============================================================================

async def agent_task_producer(queue: asyncio.Queue, items: List[str]) -> None:
    """Produces incoming work items and places them into the queue."""
    for item in items:
        await asyncio.sleep(0.01)
        await queue.put(item)
        print(f"   [Producer] Queued item: '{item}'")


async def agent_task_worker(worker_id: int, queue: asyncio.Queue, collected: List[str]) -> None:
    """Consumes work items from the queue until sentinel None is received."""
    while True:
        item = await queue.get()
        if item is None:
            # Reached end-of-work signal; acknowledge and break
            queue.task_done()
            break
        
        # Simulate processing work item
        await asyncio.sleep(0.02)
        processed = f"Processed '{item}' by Worker-{worker_id}"
        collected.append(processed)
        queue.task_done()


async def demonstrate_queue() -> None:
    """
    Demonstrates decoupled asynchronous producer-consumer architecture using asyncio.Queue.
    """
    print("=" * 70)
    print("6. ASYNC PRODUCER-CONSUMER QUEUE (asyncio.Queue)")
    print("=" * 70)

    queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    collected_results: List[str] = []
    items_to_process = ["AnalyzeLogs", "RunTestA", "LintCode", "FormatMarkdown", "VerifyBuild"]

    num_workers = 2
    workers = [
        asyncio.create_task(agent_task_worker(w_id, queue, collected_results))
        for w_id in range(1, num_workers + 1)
    ]

    # Produce all items
    await agent_task_producer(queue, items_to_process)

    # Wait for all queued items to be processed
    await queue.join()

    # Dispatch sentinel shutdown tokens to each worker
    for _ in range(num_workers):
        await queue.put(None)
    await asyncio.gather(*workers)

    print(f"Queue empty and all workers shut down cleanly. Total items processed: {len(collected_results)}:")
    for r in collected_results:
        print(f"   {r}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 7: AI Agent Multi-Tool Calling Pipeline
# ============================================================================

async def execute_tool_call(tool_name: str, args: Dict[str, Any], latency: float) -> Dict[str, Any]:
    """Simulates an AI agent tool execution (calculator, search, database query)."""
    await asyncio.sleep(latency)
    return {
        "tool": tool_name,
        "args": args,
        "output": f"Executed {tool_name} successfully with parameters {args}",
    }


async def demonstrate_agent_tool_dispatch() -> None:
    """
    Demonstrates how modern autonomous agents execute parallel tool calls emitted by LLMs.
    """
    print("=" * 70)
    print("7. AI AGENT PARALLEL TOOL DISPATCH")
    print("=" * 70)

    # Simulated LLM tool invocation requests
    tool_requests = [
        ("web_search", {"query": "latest python 3.12 features"}, 0.08),
        ("calculator", {"expression": "2 ** 16"}, 0.03),
        ("code_linter", {"file": "main.py"}, 0.06),
        ("memory_lookup", {"key": "user_preference"}, 0.04),
    ]

    t0 = time.perf_counter()
    tool_coros = [execute_tool_call(name, args, lat) for name, args, lat in tool_requests]
    tool_results = await asyncio.gather(*tool_coros)
    total_time = time.perf_counter() - t0

    print(f"Agent dispatched {len(tool_requests)} tool calls in parallel ({total_time:.2f}s total):")
    for res in tool_results:
        print(f"   Tool: {res['tool']:<15} Result: {res['output']}")
    print("-" * 70 + "\n")


# ============================================================================
# Main Entry Point
# ============================================================================

async def main() -> None:
    print("Starting Module 25: Asynchronous Concurrency in Python\n")
    await demonstrate_create_task()
    await demonstrate_gather()
    await demonstrate_task_group()
    await demonstrate_timeouts()
    await demonstrate_semaphore()
    await demonstrate_queue()
    await demonstrate_agent_tool_dispatch()
    print("Module 25 demonstration completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
