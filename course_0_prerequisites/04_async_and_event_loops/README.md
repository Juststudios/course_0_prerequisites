# Module 04: Asynchronous Programming, Event Loops, and Concurrent Agent Execution

## 1. Learning Objectives
By the end of this module, you will be able to:
- Explain the distinction between cooperative multitasking (coroutines/event loops) and preemptive multithreading.
- Run and orchestrate coroutines using `asyncio.run`, `asyncio.create_task`, and `asyncio.gather`.
- Measure latency improvements when executing multiple agent tool calls concurrently versus sequentially.
- Protect agent runs against hung network requests using `asyncio.wait_for` and `asyncio.timeout`.
- Implement rate-limiting and resource bounds using `asyncio.Semaphore`.
- Safely offload blocking, CPU-heavy, or legacy synchronous libraries to worker threads using `asyncio.to_thread`.

---

## 2. Why AI Agent Engineers Need This
Autonomous agents spend greater than 90% of their wall-clock execution time blocked on external I/O:
- Waiting for LLM completions over HTTP (2 to 15 seconds).
- Querying vector databases or full-text search indexes (100ms to 2 seconds).
- Fetching web pages or running API queries.

If an agent executes 5 search queries sequentially, the user waits $5 \times 1\text{s} = 5\text{s}$. If executed concurrently via `asyncio.gather`, all 5 complete in $\sim 1\text{s}$. Furthermore, web servers running agent swarms (like FastAPI) rely on a single-threaded asynchronous event loop to serve hundreds of concurrent users without the memory overhead of spawning hundreds of OS threads.

---

## 3. Structured Concept Breakdown

### Concept 1: Coroutine
- **TERM**: Coroutine
- **DEFINITION**: A special Python function declared with `async def` that can suspend its execution at `await` points, returning control to the event loop until an awaited operation completes.
- **INTUITION**: A chef in a busy restaurant kitchen. After putting a steak on the grill, the chef doesn't stand still staring at the meat for 10 minutes. Instead, the chef turns around and chops vegetables (`await`), returning to the steak when the kitchen timer rings.
- **WHY IT EXISTS**: Synchronous code blocks the entire thread during I/O (`time.sleep(10)` stops everything). Coroutines allow cooperative multitasking: when one task is waiting for the network, other agent tasks continue executing.
- **HOW IT WORKS**: Calling an `async def` function does not run it; it creates a coroutine object. When `await coro` is evaluated, Python yields execution back to the active event loop, which schedules other runnable tasks until `coro` produces a result.
- **CODE**:
```python
import asyncio

async def fetch_web_page(url: str) -> str:
    print(f"Starting fetch: {url}")
    await asyncio.sleep(0.5)  # Non-blocking simulated network latency
    print(f"Completed fetch: {url}")
    return f"<html>Content for {url}</html>"
```

---

### Concept 2: Event Loop
- **TERM**: Event Loop
- **DEFINITION**: The central infinite loop that monitors pending I/O events, schedules coroutines, and executes tasks when their awaited dependencies are satisfied.
- **INTUITION**: An air traffic control tower. It coordinates incoming and outgoing planes on runways, ensuring every plane gets airtime without crashing or waiting needlessly.
- **WHY IT EXISTS**: Operating system threads are heavy (each consumes 8MB stack memory by default). A single event loop can manage tens of thousands of concurrent asynchronous tasks with minimal RAM and zero thread-switching CPU overhead.
- **HOW IT WORKS**: `asyncio.run(main())` initializes the event loop, registers `main()` as a task, runs until `main()` returns, cancels any lingering tasks, and shuts down the loop.
- **CODE**:
```python
async def agent_entrypoint():
    page = await fetch_web_page("https://docs.python.org")
    print(page)

# Runs the event loop to completion
asyncio.run(agent_entrypoint())
```

---

### Concept 3: Concurrent Task Gathering (`asyncio.gather`)
- **TERM**: `asyncio.gather`
- **DEFINITION**: A utility that schedules multiple awaitable objects concurrently on the event loop, waiting until all complete and returning an ordered list of their results.
- **INTUITION**: Sending three scouts into different parts of the forest at the same moment. You wait at base camp until all three return with their maps.
- **WHY IT EXISTS**: Agents frequently generate multi-tool plans (e.g., "Check weather in Tokyo, London, and New York"). Running them sequentially multiplies latency; `asyncio.gather` executes them in parallel.
- **HOW IT WORKS**: `gather(*coros)` wraps each coroutine in a `Task`, registers them with the event loop, and awaits their collective completion, preserving the original order of arguments in the returned list.
- **CODE**:
```python
async def get_multi_city_weather(cities: list[str]) -> list[str]:
    tasks = [fetch_web_page(f"https://weather.api/{city}") for city in cities]
    # All tasks execute concurrently
    results = await asyncio.gather(*tasks)
    return results
```

---

### Concept 4: Concurrency Throttling (`asyncio.Semaphore`)
- **TERM**: `asyncio.Semaphore`
- **DEFINITION**: A synchronization primitive that manages an internal counter of available permits, suspending tasks when the permit count reaches zero until another task releases a permit.
- **INTUITION**: A night club with a maximum capacity of 5 guests. If 5 people are inside, the bouncer makes the 6th person wait in line until someone leaves.
- **WHY IT EXISTS**: If an agent spawns 100 concurrent tool requests, external APIs will immediately return HTTP 429 (Too Many Requests), or local system resources will crash. A semaphore bounds concurrency to a safe maximum (e.g. 5 concurrent requests).
- **HOW IT WORKS**: Entering `async with semaphore:` decrements the internal counter. If counter is 0, the task suspends. Exiting increments the counter and resumes the next waiting coroutine.
- **CODE**:
```python
sem = asyncio.Semaphore(3)  # Maximum 3 concurrent tool calls

async def safe_api_call(endpoint: str) -> str:
    async with sem:
        # At most 3 coroutines will execute this block simultaneously
        return await fetch_web_page(endpoint)
```

---

### Concept 5: Timeout Protection (`asyncio.wait_for`)
- **TERM**: `asyncio.wait_for`
- **DEFINITION**: A wrapper that runs an awaitable with a deadline; if the operation exceeds the deadline, it is immediately cancelled and `asyncio.TimeoutError` is raised.
- **INTUITION**: A kitchen egg timer. If the oven hasn't beeped within 10 minutes, you shut off the gas so the food doesn't burn.
- **WHY IT EXISTS**: AI agents can freeze indefinitely if a remote tool hangs on an unclosed socket. Hard timeout boundaries ensure the agent can catch the timeout, inform the user or LLM, and take alternate paths.
- **HOW IT WORKS**: Schedules the coroutine and a timer callback on the loop. If the timer fires first, the coroutine task is sent a cancellation request (`task.cancel()`) and raises `TimeoutError`.
- **CODE**:
```python
async def resilient_tool_execution(coro, timeout_seconds: float = 2.0):
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        return "ERROR: Tool execution timed out."
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Blocking the Event Loop with Synchronous Code
- **The Bug**: Calling `time.sleep()`, synchronous `requests.get()`, or a heavy NumPy calculation directly inside a coroutine.
- **The Consequence**: Freezes the entire Python event loop. All other concurrent agent tasks, user requests, and background timers stall completely.
- **The Fix**: Offload blocking calls using `await asyncio.to_thread(blocking_func, *args)`.

### Anti-Pattern 2: Unbounded Task Spawning
- **The Bug**: Looping over a 500-item list with `asyncio.create_task()` without a semaphore.
- **The Consequence**: Spawns 500 simultaneous network connections, causing socket exhaustion, TCP connection resets, and immediate HTTP 429 rate limit bans.
- **The Fix**: Protect concurrent fan-outs with an `asyncio.Semaphore(max_concurrency)`.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What keyword is used to pause execution of a coroutine until an asynchronous operation yields a result?
2. What happens if you call `time.sleep(5)` inside an `async def` function?
3. Which standard library function runs a blocking synchronous function in a separate thread pool from within an async loop?

### Tier 2 (Debugging)
Find the bug in this concurrent agent execution snippet:
```python
async def run_all_tools(tool_list):
    results = []
    for tool in tool_list:
        res = await tool.execute()  # Why does this defeat concurrency?
        results.append(res)
    return results
```
*Hint*: The loop awaits each tool one after another sequentially! Rewrite using `asyncio.gather`.

### Tier 3 (Application)
Write an async function `fetch_with_fallback(primary_coro, fallback_coro, timeout: float)` that attempts `primary_coro` within `timeout` seconds. If it times out or fails, it executes `fallback_coro` and returns its result.

### Tier 4 (Challenge)
Build an `AsyncToolRunner` class with:
1. An `asyncio.Semaphore(capacity)`.
2. A method `run_batch(tool_calls: list[Callable]) -> list[Any]` that runs all tool calls concurrently with timeout protection per tool and returns ordered results.
3. Automated capture of errors without aborting other concurrent tasks (`return_exceptions=True`).

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/04_async_and_event_loops/async_basics.py
python3 course_0_prerequisites/04_async_and_event_loops/concurrent_tools.py
```
