# Topic: Asynchronous Concurrency in Python

## What You Will Learn
In this module, you will learn:
- How to transition from sequential coroutine execution to true asynchronous concurrency.
- How `asyncio.create_task()` schedules background coroutines on the event loop immediately.
- How to fan out multiple concurrent operations and collect their results with `asyncio.gather()`.
- How modern Python 3.11+ Structured Concurrency works with `asyncio.TaskGroup`.
- How to enforce execution deadlines and handle timeouts using `asyncio.wait_for` and `asyncio.timeout`.
- How to limit concurrent load and prevent rate limit exhaustion using `asyncio.Semaphore`.
- How to build decoupled Producer-Consumer systems using asynchronous message queues (`asyncio.Queue`).
- How multi-agent AI architectures manage concurrent subagents, tool calls, and event streams.

## Prerequisites
Before tackling this module, you should be familiar with:
- Module 24: Introduction to Asynchronous Python (`async def`, `await`, `asyncio.run()`, event loop fundamentals).
- Module 06: Collections (lists, dictionaries, tuples).
- Module 10: Exception handling (`try/except/finally`).

## The Problem
In Module 24, we saw how `await` pauses execution until a coroutine completes.
However, if you write:
```python
result1 = await fetch("agent1", delay=2)
result2 = await fetch("agent2", delay=2)
result3 = await fetch("agent3", delay=2)
```
These calls still run **one after another (in series)**! The total execution time is still 2 + 2 + 2 = **6 seconds**.
Even though they are non-blocking, we didn't start `agent2` until `agent1` was completely finished.

If an AI agent needs to query three search engines, inspect two documents, and check a database, running them in series wastes user time. We need a way to launch all operations **concurrently** so they run in parallel during their I/O waits, completing all three tasks in just **2 seconds**.

## Key Terminology
- **Concurrency**: Managing multiple computations at the same time by interleaving their execution periods over a single thread.
- **`asyncio.Task`**: A wrapper around a coroutine that registers it with the event loop to run immediately in the background.
- **Fan-Out / Fan-In**: A design pattern where a single coordinator broadcasts work to multiple concurrent tasks (fan-out) and then waits to aggregate all results (fan-in).
- **`asyncio.gather`**: A utility function that runs multiple awaitables concurrently and returns a list of results in the order they were supplied.
- **`asyncio.TaskGroup`**: Introduced in Python 3.11, a structured concurrency context manager that cleanly groups tasks, cancels remaining siblings if one fails, and guarantees all tasks exit before the block finishes.
- **`asyncio.Semaphore`**: A synchronization primitive that limits the number of concurrent tasks accessing a shared resource (such as an LLM API rate limit).
- **`asyncio.Queue`**: A thread-safe, coroutine-friendly FIFO (First-In, First-Out) data structure used to coordinate producers and consumers.
- **Timeout**: An enforced time boundary that cancels a pending task if it does not produce a result within a specified deadline.

## Intuition
Imagine a team leader in an office:
- **Sequential Approach**: The leader tells Intern Alice to research a topic. The leader stands by Alice's desk for an hour. Once Alice delivers the paper, the leader walks over to Intern Bob and tells him to research a second topic, waiting another hour. Total time: 2 hours.
- **Concurrent Approach (`gather` / `TaskGroup`)**: The leader hands assignments to Alice and Bob simultaneously ("Both of you go to work now!"). The leader sits back. Both interns work simultaneously. In one hour, both papers arrive. Total time: 1 hour.

## Concept
Concurrency in `asyncio` revolves around **Tasks**.
When you call `task = asyncio.create_task(coro())`:
1. The coroutine is wrapped into a `Task` object.
2. The task is immediately added to the event loop's active execution queue.
3. The calling code can proceed immediately without waiting!

To wait for multiple tasks to finish:
- **`asyncio.gather(*tasks)`**: Gathers results into a list. Can optionally capture exceptions without aborting other tasks using `return_exceptions=True`.
- **`asyncio.TaskGroup()`**: The modern, safe standard. If any task inside the group raises an uncaught exception, all remaining running tasks in the group are immediately cancelled, preventing "orphan tasks" or leaked background jobs.

To throttle execution:
- **`asyncio.Semaphore(value)`**: Acts like a bouncer at a club. Only `value` tasks can enter the `async with semaphore:` block at once; all others queue up politely.

## Syntax
```python
import asyncio

async def fetch_item(item_id: int, duration: float) -> str:
    await asyncio.sleep(duration)
    return f"Item {item_id} fetched"

# 1. Concurrent execution with asyncio.gather
async def demo_gather():
    results = await asyncio.gather(
        fetch_item(1, 0.2),
        fetch_item(2, 0.2),
        fetch_item(3, 0.2),
    )
    # Total time is ~0.2s, not 0.6s!
    return results

# 2. Modern Structured Concurrency with TaskGroup (Python 3.11+)
async def demo_task_group():
    results = []
    async with asyncio.TaskGroup() as tg:
        # Create tasks inside the structured scope
        task1 = tg.create_task(fetch_item(10, 0.1))
        task2 = tg.create_task(fetch_item(20, 0.1))
    # When exiting the context manager, both tasks are guaranteed complete!
    return [task1.result(), task2.result()]

# 3. Limiting Concurrency with Semaphore
sem = asyncio.Semaphore(2)  # Max 2 concurrent tasks

async def rate_limited_call(call_id: int):
    async with sem:
        # Only 2 tasks will execute this block simultaneously
        return await fetch_item(call_id, 0.1)
```

## Example
Here is a complete, executable demonstration contrasting sequential vs concurrent execution times and demonstrating `asyncio.gather`:

```python
import asyncio
import time

async def simulate_worker(worker_id: int, latency: float) -> str:
    print(f"[{time.strftime('%X')}] Worker {worker_id} started (needs {latency}s)...")
    await asyncio.sleep(latency)
    print(f"[{time.strftime('%X')}] Worker {worker_id} completed!")
    return f"Worker_{worker_id}_Result"

async def run_comparison():
    durations = [0.2, 0.2, 0.2]
    
    # 1. Sequential execution
    print("--- Sequential Execution ---")
    t0 = time.perf_counter()
    seq_results = []
    for i, d in enumerate(durations, start=1):
        seq_results.append(await simulate_worker(i, d))
    seq_time = time.perf_counter() - t0
    print(f"Sequential Duration: {seq_time:.2f}s\n")
    
    # 2. Concurrent execution with gather
    print("--- Concurrent Execution (gather) ---")
    t0 = time.perf_counter()
    coros = [simulate_worker(i, d) for i, d in enumerate(durations, start=1)]
    concurrent_results = await asyncio.gather(*coros)
    conc_time = time.perf_counter() - t0
    print(f"Concurrent Duration: {conc_time:.2f}s")
    print(f"Speedup: {seq_time / conc_time:.1f}x")

if __name__ == "__main__":
    asyncio.run(run_comparison())
```

## Line-by-Line Explanation
1. `coros = [simulate_worker(i, d) for i, d in enumerate(...)]`: Creates three coroutine objects without awaiting them yet.
2. `concurrent_results = await asyncio.gather(*coros)`: Unpacks the coroutines into `asyncio.gather()`. The event loop registers all three coroutines immediately.
3. During the 0.2-second sleep, all three workers are asleep simultaneously. The event loop wakes them all up at virtually the same instant.
4. `concurrent_results`: A list containing the three return values, maintaining the exact positional order of the inputs.
5. The elapsed time is ~0.2s instead of ~0.6s—a 3x speedup!

## What Python Is Doing
When `asyncio.gather(*coros)` runs:
1. It wraps each coroutine in an `asyncio.Task` (if not already a task) and submits them to the active event loop.
2. It registers callbacks on each task so that when a task completes or fails, an internal counter is decremented.
3. The event loop's I/O multiplexer sets timers for all three tasks.
4. If one task throws an exception and `return_exceptions=False`, `gather` immediately propagates the exception. If `return_exceptions=True`, it catches the exception and places the exception instance in the resulting list at that task's index.

## Common Mistakes
1. **Unbounded Concurrency**: Firing 10,000 tasks simultaneously with `asyncio.gather(*[call(i) for i in range(10000)])`. This can exhaust file descriptors, crash sockets, or trigger IP bans from API providers. Always throttle with `asyncio.Semaphore`.
2. **Forgetting to Unpack `*args` in `gather`**: Calling `asyncio.gather(task_list)` instead of `asyncio.gather(*task_list)`. Passing a raw list passes 1 argument (the list), which causes a TypeError.
3. **Fire-and-Forget Task Garbage Collection**: Creating a task with `asyncio.create_task(coro())` and saving no reference to it. Python's garbage collector may discard the task before it finishes! Always retain a reference in a set or list.
4. **Ignoring TaskGroup Cancellation Semantics**: In `TaskGroup`, if one task fails, all sibling tasks are cancelled with `asyncio.CancelledError`. If you catch exceptions inside individual tasks, the group won't abort.

## Real-World Uses
- **Web Crawlers**: Scraping hundreds of URLs concurrently while respecting per-domain rate limits.
- **Telemetry Aggregation**: Querying status endpoints across a cluster of 50 microservices simultaneously.
- **Chatbot Gateways**: Handling hundreds of active user sessions concurrently on a single server.

## Connection to AI Agents
Multi-agent systems and complex agent runtimes depend heavily on async concurrency:
- **Parallel Subagent Swarms**: An orchestrator agent breaks a user request into subtasks and dispatches them to specialized worker subagents running concurrently via `asyncio.gather`.
- **Parallel Tool Calling**: Modern LLMs support multi-tool calling (e.g. calling `web_search`, `calculator`, and `fetch_weather` in a single response). The agent executes all tool calls concurrently.
- **Rate-Limiting LLM Calls**: Autonomous agents use `asyncio.Semaphore(N)` to avoid exceeding TPM/RPM (Tokens/Requests Per Minute) limits enforced by cloud LLM APIs.
- **Agent Message Queues**: Background worker loops listen to `asyncio.Queue` for incoming user interruptions, cancellation tokens, or tool completions.

## Practice
1. Create a coroutine `fetch(id: int) -> int` that sleeps for 0.1s and returns `id * 10`.
2. Use `asyncio.gather` to run 5 fetches concurrently.
3. Verify that the total runtime is approximately 0.1s, not 0.5s.

## Challenge
Can you implement a concurrent worker pool using `asyncio.Queue` and a fixed number of worker coroutines that process tasks until a sentinel `None` is encountered? (We will build this in `exercises.py`!)

## Summary
- `asyncio.gather` and `asyncio.TaskGroup` enable running multiple coroutines concurrently.
- Concurrency reduces total execution time from the sum of delays to the maximum delay among tasks.
- `asyncio.Semaphore` prevents overwhelming external systems by capping concurrent requests.
- `asyncio.Queue` provides decoupled, asynchronous message passing between producers and consumers.

## What You Should Know Before Moving On
- How to run coroutines concurrently using `asyncio.gather(*coros)`.
- How to use `asyncio.TaskGroup` for safe, structured concurrency.
- How to limit concurrent load using `asyncio.Semaphore`.
- How `asyncio.Queue` coordinates asynchronous worker pipelines.
