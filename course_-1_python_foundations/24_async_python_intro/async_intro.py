"""
Module 24: Introduction to Asynchronous Python
==============================================

This lesson explores the foundations of asynchronous programming in Python.

Unlike traditional synchronous programming, where the CPU halts while waiting
for network, disk, or timers, asynchronous programming enables single-threaded
cooperative multitasking. By using coroutines and an event loop, Python can
execute other tasks while an I/O operation is in flight.

Key Concepts Covered:
---------------------
1. The Anatomy of a Coroutine (`async def`, coroutine objects).
2. The `await` keyword and yielding control to the Event Loop.
3. Starting async programs using `asyncio.run()`.
4. Comparing non-blocking `asyncio.sleep()` with blocking operations.
5. Coroutine chaining and returning data through pipelines.
6. Asynchronous error handling and recovery.
7. Asynchronous generators (`async def` with `yield`) for streaming LLM tokens.
"""

import asyncio
import inspect
import time
from typing import AsyncGenerator, Dict, List, Optional


# ============================================================================
# Section 1: Coroutine Objects vs Function Calls
# ============================================================================

async def sample_coroutine(name: str) -> str:
    """A minimal coroutine returning a formatted greeting."""
    return f"Hello from coroutine: {name}"


def demonstrate_coroutine_object() -> None:
    """
    Demonstrates what happens when an async def function is called directly.
    
    Calling an async function does NOT execute its body immediately. Instead,
    it creates and returns a coroutine object.
    """
    print("=" * 68)
    print("1. COROUTINE OBJECTS VS REGULAR FUNCTION CALLS")
    print("=" * 68)
    
    # Direct invocation without await:
    coro = sample_coroutine("Explorer")
    
    print(f"Object returned by calling sample_coroutine(): {coro}")
    print(f"Type of object: {type(coro)}")
    print(f"Is inspect.iscoroutine(coro)? {inspect.iscoroutine(coro)}")
    
    # We close the unawaited coroutine explicitly to prevent Python from printing
    # RuntimeWarning: coroutine was never awaited.
    coro.close()
    print("Note: Coroutines must be passed to the event loop via 'await' or 'asyncio.run()'.")
    print("-" * 68 + "\n")


# ============================================================================
# Section 2: The Basics of async def and await
# ============================================================================

async def fetch_simulated_data(source_id: int, delay: float) -> Dict[str, object]:
    """
    Simulates a non-blocking asynchronous data fetch (e.g. from an API).
    
    `await asyncio.sleep(delay)` suspends this coroutine, returning control
    to the event loop so other coroutines can run during the delay.
    """
    print(f"  [{time.strftime('%X')}] [Fetch {source_id}] Starting network request ({delay}s delay)...")
    await asyncio.sleep(delay)  # Cooperative, non-blocking pause
    print(f"  [{time.strftime('%X')}] [Fetch {source_id}] Response received successfully!")
    return {
        "source_id": source_id,
        "payload": f"Telemetry Data #{source_id * 100}",
        "latency_seconds": delay,
    }


async def demonstrate_sequential_await() -> None:
    """
    Demonstrates sequential execution of coroutines.
    Each await pauses the current function until the target coroutine finishes.
    """
    print("=" * 68)
    print("2. SEQUENTIAL COROUTINE EXECUTION (await)")
    print("=" * 68)
    start_time = time.perf_counter()
    
    print(f"[{time.strftime('%X')}] Initiating Sequential Awaits...")
    result_1 = await fetch_simulated_data(1, 0.2)
    result_2 = await fetch_simulated_data(2, 0.3)
    
    total_time = time.perf_counter() - start_time
    print(f"[{time.strftime('%X')}] All sequential requests completed.")
    print(f"Result 1: {result_1['payload']}")
    print(f"Result 2: {result_2['payload']}")
    print(f"Total elapsed time: {total_time:.3f} seconds (0.2s + 0.3s ≈ 0.5s)")
    print("-" * 68 + "\n")


# ============================================================================
# Section 3: Coroutine Chaining & Multi-Stage Pipelines
# ============================================================================

async def stage_one_fetch_query(query: str) -> str:
    """Stage 1: Simulates fetching raw search results from an external engine."""
    await asyncio.sleep(0.1)
    return f"raw_data_for({query})"


async def stage_two_clean_data(raw_data: str) -> str:
    """Stage 2: Cleans and filters the fetched data."""
    await asyncio.sleep(0.1)
    cleaned = raw_data.replace("raw_data_for(", "").rstrip(")")
    return cleaned.upper()


async def stage_three_format_report(cleaned_data: str) -> Dict[str, str]:
    """Stage 3: Packages the final result into an analytical record."""
    await asyncio.sleep(0.1)
    return {
        "status": "success",
        "processed_entity": cleaned_data,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


async def run_data_pipeline(query: str) -> Dict[str, str]:
    """
    Orchestrates an end-to-end multi-stage pipeline using coroutine chaining.
    """
    print(f"  [*] Pipeline starting for query: '{query}'")
    raw = await stage_one_fetch_query(query)
    cleaned = await stage_two_clean_data(raw)
    report = await stage_three_format_report(cleaned)
    print(f"  [+] Pipeline finished: {report['processed_entity']}")
    return report


# ============================================================================
# Section 4: Asynchronous Error Handling
# ============================================================================

class ToolExecutionError(Exception):
    """Custom exception raised when an asynchronous tool fails."""
    pass


async def risky_remote_tool(tool_name: str, should_fail: bool) -> str:
    """
    Simulates a tool that might encounter a remote failure.
    Coroutines support standard Python try/except/finally blocks!
    """
    print(f"  [*] Executing tool: {tool_name} (will_fail={should_fail})...")
    await asyncio.sleep(0.15)
    if should_fail:
        raise ToolExecutionError(f"Tool '{tool_name}' failed: remote endpoint timeout")
    return f"Success: Output from {tool_name}"


async def demonstrate_error_handling() -> None:
    """Demonstrates catching and recovering from coroutine exceptions."""
    print("=" * 68)
    print("3. ASYNCHRONOUS ERROR HANDLING AND RECOVERY")
    print("=" * 68)
    
    # Case A: Successful tool call
    try:
        res = await risky_remote_tool("calculator_tool", should_fail=False)
        print(f"  Result: {res}")
    except ToolExecutionError as exc:
        print(f"  Caught error: {exc}")
        
    # Case B: Failing tool call with graceful fallback
    print("\n  Now calling an unreliable tool:")
    try:
        res = await risky_remote_tool("unstable_web_search", should_fail=True)
        print(f"  Result: {res}")
    except ToolExecutionError as exc:
        print(f"  [Recovered] Gracefully caught error: '{exc}'")
        print("  [Fallback] Engaging local cached fallback knowledge base.")
    print("-" * 68 + "\n")


# ============================================================================
# Section 5: Asynchronous Generators & Token Streaming (AI Agent Pattern)
# ============================================================================

async def stream_llm_tokens(prompt: str) -> AsyncGenerator[str, None]:
    """
    Simulates how LLM providers (OpenAI, Anthropic, Ollama) stream tokens
    asynchronously using an async generator (`async def` with `yield`).
    
    The consumer receives tokens one at a time as they arrive over the wire!
    """
    simulated_tokens = [
        "Autonomous ",
        "AI ",
        "agents ",
        "leverage ",
        "asynchronous ",
        "Python ",
        "for ",
        "real-time ",
        "token ",
        "streaming.",
    ]
    for token in simulated_tokens:
        await asyncio.sleep(0.05)  # Simulate network latency between generated tokens
        yield token


async def demonstrate_streaming() -> None:
    """
    Consumes an async generator using the `async for` syntax.
    """
    print("=" * 68)
    print("4. ASYNC GENERATORS: LLM TOKEN STREAMING (AI AGENT PATTERN)")
    print("=" * 68)
    print("Agent Prompt: 'Explain async agents.'")
    print("Streaming response: ", end="", flush=True)
    
    # The `async for` loop pauses waiting for the next yielded token:
    async for token in stream_llm_tokens("Explain async agents."):
        print(token, end="", flush=True)
        
    print("\n" + "-" * 68 + "\n")


# ============================================================================
# Section 6: Main Async Orchestrator
# ============================================================================

async def async_main() -> None:
    """The master coroutine that orchestrates all async demonstrations."""
    print(f"Event loop initialized at {time.strftime('%X')}.")
    
    # 1. Sequential await demonstration
    await demonstrate_sequential_await()
    
    # 2. Coroutine pipeline demonstration
    print("=" * 68)
    print("5. MULTI-STAGE COROUTINE PIPELINE")
    print("=" * 68)
    pipeline_result = await run_data_pipeline("autonomous_agent_architecture")
    print(f"Final Pipeline Result Dictionary: {pipeline_result}")
    print("-" * 68 + "\n")
    
    # 3. Error handling demonstration
    await demonstrate_error_handling()
    
    # 4. Token streaming demonstration
    await demonstrate_streaming()
    
    print(f"All async tasks completed cleanly at {time.strftime('%X')}.")


def main() -> None:
    """
    Synchronous entrypoint.
    Runs non-async setup first, then hands control to asyncio.run().
    """
    print("\n" + "=" * 68)
    print("     MODULE 24: INTRODUCTION TO ASYNCHRONOUS PYTHON")
    print("=" * 68 + "\n")
    
    # Demonstrate unawaited coroutines in synchronous code
    demonstrate_coroutine_object()
    
    # asyncio.run() creates a new event loop, executes async_main(), and closes the loop.
    asyncio.run(async_main())
    
    print("=" * 68)
    print("Module 24 lesson executed successfully with exit code 0.")
    print("=" * 68 + "\n")


if __name__ == "__main__":
    main()
