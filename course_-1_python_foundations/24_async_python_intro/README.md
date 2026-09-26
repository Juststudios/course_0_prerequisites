# Topic: Introduction to Asynchronous Python

## What You Will Learn
In this module, you will learn:
- The fundamental difference between synchronous (blocking) and asynchronous (non-blocking) execution.
- Why network and I/O operations waste immense amounts of CPU time in synchronous programs.
- How Python achieves single-threaded cooperative multitasking using an Event Loop.
- How to define coroutine functions with `async def` and pause them with `await`.
- Why calling a coroutine function does not immediately run it, but creates a coroutine object.
- The role of `asyncio.run()` as the primary entry point to an async application.
- The critical difference between non-blocking `asyncio.sleep()` and blocking `time.sleep()`.
- How autonomous AI agents use async functions to interact with remote LLM APIs, stream tokens, and handle multi-agent message routing without stalling.

## Prerequisites
Before tackling this module, you should be familiar with:
- Module 08: Functions, arguments, and return values.
- Module 10: Exception handling (`try`, `except`).
- Module 17: Generators and the `yield` keyword (conceptual cousin of `await`).

## The Problem
Imagine a synchronous program that fetches data from three remote web APIs:
```python
import time

def fetch_data(source_name, delay):
    print(f"Fetching {source_name}...")
    time.sleep(delay)  # Simulates waiting for network packets
    print(f"Received {source_name}!")
    return f"{source_name}_data"

def main():
    start = time.time()
    res1 = fetch_data("API_1", 2)
    res2 = fetch_data("API_2", 2)
    res3 = fetch_data("API_3", 2)
    print(f"Total time: {time.time() - start:.2f} seconds")
```
When you run this code, it takes **6 seconds**.
During those 6 seconds, your computer's blazing-fast multi-gigahertz CPU sits at 0% utilization, completely frozen, doing nothing but waiting for electricity to traverse fiber-optic cables across the internet.

If your program is an AI agent serving a user chat interface, the entire interface freezes while waiting for the LLM. If another message arrives, it gets ignored. Synchronous I/O wastes time and destroys responsiveness.

## Key Terminology
- **Synchronous (Blocking) Code**: Execution where each operation must finish completely before the next line of code starts. While waiting for I/O, the program halts.
- **Asynchronous (Non-blocking) Code**: Execution where long-running I/O operations yield control back to an orchestrator (the event loop), allowing other tasks to make progress while waiting.
- **Coroutine**: A specialized Python function defined with `async def` that can pause its execution at `await` points and resume later where it left off, retaining all local state.
- **Event Loop**: The central engine in `asyncio` that manages and distributes execution time among all active coroutines, waking them up when their I/O events complete.
- **`await`**: The Python keyword that pauses the current coroutine until the awaited operation completes, returning control to the event loop.
- **Coroutine Object**: The object returned when invoking an `async def` function directly without `await`.
- **I/O-Bound**: A workload whose bottleneck is input/output operations (disk, network, database) rather than CPU calculations.

## Intuition
Think of a busy chef in a restaurant kitchen:
- **Synchronous Cooking**: The chef puts bread in the toaster for 3 minutes. The chef stands motionless, staring at the toaster for 3 full minutes. Only when the toast pops up does the chef begin cracking eggs.
- **Asynchronous Cooking**: The chef puts bread in the toaster and sets a timer (`await toaster`). Instead of standing idle, the chef immediately turns to the stove to whisk eggs. When the toaster timer dings (an event loop signal), the chef pauses the eggs, retrieves the toast, and continues cooking.

A single chef (a single CPU thread) completes breakfast in 3 minutes instead of 6 minutes through cooperative scheduling.

## Concept
Python's `asyncio` module provides single-threaded concurrency. It does not run multiple instructions simultaneously on different CPU cores (that is multiprocessing). Instead, it runs on a single thread and switches between tasks whenever a task is waiting for an external event (like a network response).

The building blocks:
1. **`async def`**: Declares a coroutine function.
2. **`await <awaitable>`**: Can only be used inside an `async def` function. It pauses the current coroutine and hands control to the event loop.
3. **`asyncio.run(coro)`**: Creates an event loop, runs the passed coroutine to completion, and cleans up the loop.

## Syntax
```python
import asyncio

# 1. Define a coroutine function
async def greet(name: str, delay: float) -> str:
    print(f"Starting greeting for {name}...")
    # 2. Non-blocking sleep yields control to the event loop
    await asyncio.sleep(delay)
    print(f"Finished greeting for {name}!")
    return f"Hello, {name}!"

# 3. Main async entrypoint
async def main() -> None:
    # 4. Awaiting another coroutine
    message = await greet("Alice", 1.0)
    print(f"Result: {message}")

# 5. Launch the event loop from synchronous code
if __name__ == "__main__":
    asyncio.run(main())
```

## Example
Here is a complete comparison between blocking code and non-blocking coroutines:

```python
import asyncio
import time

async def simulate_api_call(service_name: str, latency: float) -> dict:
    """Simulates an asynchronous network call to an external service."""
    print(f"[{time.strftime('%X')}] Requesting {service_name}...")
    await asyncio.sleep(latency)  # Non-blocking pause
    print(f"[{time.strftime('%X')}] Received response from {service_name}!")
    return {"service": service_name, "status": 200}

async def fetch_sequential() -> None:
    """Demonstrates sequential coroutine awaiting."""
    t0 = time.perf_counter()
    r1 = await simulate_api_call("AuthService", 0.5)
    r2 = await simulate_api_call("DatabaseService", 0.5)
    elapsed = time.perf_counter() - t0
    print(f"Total sequential time: {elapsed:.2f}s")

if __name__ == "__main__":
    asyncio.run(fetch_sequential())
```

## Line-by-Line Explanation
1. `import asyncio, time`: Imports the `asyncio` standard library along with `time` for measuring execution duration.
2. `async def simulate_api_call(...)`: The `async def` keyword informs Python that this is a coroutine function.
3. `await asyncio.sleep(latency)`: Suspends the coroutine for `latency` seconds. Crucially, the Python thread is not blocked; it is free to process other events in the loop.
4. `return {"service": service_name, "status": 200}`: Coroutines return values just like normal functions. When awaited, the return value is unpacked into the caller.
5. `async def fetch_sequential()`: A higher-level coroutine orchestrating the calls.
6. `r1 = await simulate_api_call(...)`: Execution in `fetch_sequential` pauses until `simulate_api_call` resolves and yields its dictionary.
7. `asyncio.run(fetch_sequential())`: Boots the Python event loop, schedules `fetch_sequential`, runs until it finishes, and tears down the event loop.

## What Python Is Doing
Under the hood, coroutines in Python are built upon generators:
1. When you define `async def func():`, Python flags the function code object with `CO_COROUTINE`.
2. When you call `func()`, Python does NOT execute the function body. Instead, it instantiates and returns a `coroutine` object (which implements `.send()`, `.throw()`, and `.close()`).
3. When an expression `await coro` is evaluated, Python calls the coroutine's internal `__await__()` method, yielding control to the event loop.
4. The event loop maintains a queue of ready-to-run tasks. While your coroutine is waiting for `asyncio.sleep()`, the event loop registers a timer in the OS selector (e.g. `epoll` on Linux, `kqueue` on macOS).
5. When the OS signals that the timer or socket has data ready, the event loop resumes the paused coroutine by calling `.send(value)`, continuing right after the `await` statement.

## Common Mistakes
1. **Calling a Coroutine Without `await`**:
   ```python
   async def fetch():
       return 42
   x = fetch()  # BUG! x is a coroutine object, not 42!
   # RuntimeWarning: coroutine 'fetch' was never awaited
   ```
2. **Using Blocking Calls in Coroutines**:
   Calling `time.sleep(5)` or `requests.get(...)` inside an async function blocks the entire OS thread, completely freezing all other concurrent coroutines. Always use `await asyncio.sleep(...)` or an async HTTP library (like `aiohttp` or `httpx`).
3. **Using `await` Outside `async def`**:
   `await` is a syntax error if placed inside a regular `def` function.
4. **Calling `asyncio.run()` Inside a Running Event Loop**:
   `asyncio.run()` cannot be called when an event loop is already active (such as inside Jupyter notebooks or within another coroutine).

## Real-World Uses
- **High-Performance Web Servers**: Frameworks like FastAPI and Starlette handle tens of thousands of simultaneous HTTP connections per second using `asyncio`.
- **Database Connection Pools**: Async database drivers (like `asyncpg` or `aiomysql`) allow servers to query databases without tying up worker threads.
- **WebSocket & Chat Applications**: Keeping thousands of idle client sockets open without consuming gigabytes of thread stack memory.

## Connection to AI Agents
Asynchronous programming is the backbone of modern AI agent architectures:
- **LLM Streaming**: When querying OpenAI, Anthropic, or local Ollama models, an agent streams responses token-by-token using async generators (`async for token in stream`).
- **Parallel Tool Execution**: An agent deciding to search Wikipedia and check weather simultaneously can trigger both tools concurrently without waiting sequentially.
- **Heartbeats and Timeouts**: Agents maintain background timers and heartbeat monitors that trigger if a tool or subagent becomes unresponsive.

## Practice
1. Write a coroutine `slow_square(n: int) -> int` that sleeps for 0.1 seconds and returns `n * n`.
2. In `main()`, await `slow_square(5)` and print the result.
3. Run `main()` with `asyncio.run(main())`.

## Challenge
Can you build an asynchronous pipeline where one coroutine produces messages with delays, another coroutine consumes and formats them, and the system gracefully completes? (We will build this in `exercises.py`!)

## Summary
- Asynchronous Python allows high-concurrency I/O without the overhead of threads or processes.
- Coroutine functions are defined with `async def` and executed via `await`.
- The event loop is the single-threaded scheduler that manages coroutines.
- Never use blocking functions (like `time.sleep`) inside coroutines.

## What You Should Know Before Moving On
- How to define a coroutine with `async def` and invoke it with `await`.
- How to start an async program using `asyncio.run()`.
- What causes `RuntimeWarning: coroutine was never awaited`.
- Why AI agents rely on async programming for streaming and non-blocking I/O.
