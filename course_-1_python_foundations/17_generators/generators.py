"""
Module 17: Generators and Lazy Evaluation
==========================================

This lesson covers Python generators in depth, demonstrating how lazy
evaluation allows high-performance, low-memory data streaming.

Topics covered:
  1. The yield keyword vs return: Suspension and resumption
  2. The step-by-step lifecycle of a generator object and StopIteration
  3. Memory profiling: List comprehensions vs Generator expressions
  4. Infinite series and stateful stream generation
  5. Multi-stage streaming data pipelines
  6. Subgenerator delegation with `yield from`
  7. Practical AI Agent pattern: Streaming LLM tokens with real-time buffering
"""

import sys
import time
from typing import Generator, Iterable, List, Dict, Any


# =====================================================================
# 1. Yield vs Return: The Mechanics of Suspension
# =====================================================================
print("=" * 60)
print("1. Yield vs Return: Mechanics of Suspension")
print("=" * 60)

def eager_range(limit: int) -> List[int]:
    """
    Standard eager function:
    Allocates an entire list in memory, fills it completely, and returns it.
    """
    print(f"  [eager_range] Starting eager allocation for limit={limit}")
    results = []
    for i in range(limit):
        results.append(i)
    print(f"  [eager_range] Done allocating. Returning list of size {len(results)}")
    return results

def lazy_range(limit: int) -> Generator[int, None, None]:
    """
    Generator function:
    Uses `yield` to return one element at a time. The execution frame is
    frozen between invocations.
    """
    print(f"  [lazy_range] Generator initialized for limit={limit}")
    current = 0
    while current < limit:
        print(f"  [lazy_range] About to yield {current}")
        yield current
        print(f"  [lazy_range] Resumed after yielding {current}")
        current += 1
    print("  [lazy_range] Loop finished, generator exiting.")

# Notice what happens when we call the generator function:
print("\nCalling lazy_range(3)...")
gen_obj = lazy_range(3)
print(f"Returned object: {gen_obj} (Type: {type(gen_obj).__name__})")
print("Notice that NO lines inside lazy_range ran yet!\n")

# Now let's manually advance the generator using next()
print("First call to next(gen_obj):")
val1 = next(gen_obj)
print(f"Received from generator: {val1}\n")

print("Second call to next(gen_obj):")
val2 = next(gen_obj)
print(f"Received from generator: {val2}\n")

print("Third call to next(gen_obj):")
val3 = next(gen_obj)
print(f"Received from generator: {val3}\n")

# Fourth call will cause StopIteration because the generator finishes
print("Fourth call to next(gen_obj) expecting StopIteration:")
try:
    next(gen_obj)
except StopIteration:
    print("Caught expected StopIteration! Generator stream is exhausted.")


# =====================================================================
# 2. Memory Comparison: List Comprehension vs Generator Expression
# =====================================================================
print("\n" + "=" * 60)
print("2. Memory Footprint: Lists vs Generator Expressions")
print("=" * 60)

n_elements = 100_000

# A list comprehension allocates all elements immediately
eager_squares = [x * x for x in range(n_elements)]
eager_size = sys.getsizeof(eager_squares)

# A generator expression creates a generator object without computing values
lazy_squares = (x * x for x in range(n_elements))
lazy_size = sys.getsizeof(lazy_squares)

print(f"Number of elements: {n_elements:,}")
print(f"List comprehension memory:   {eager_size:,} bytes")
print(f"Generator expression memory: {lazy_size:,} bytes")
print(f"Memory reduction factor:     {eager_size / lazy_size:.1f}x less RAM used!")

# Demonstrate that we can still compute values from the generator
first_five = [next(lazy_squares) for _ in range(5)]
print(f"First 5 elements pulled from generator: {first_five}")


# =====================================================================
# 3. Infinite Generators: Producing Sequences Without Bounds
# =====================================================================
print("\n" + "=" * 60)
print("3. Infinite Sequences: Fibonacci Generator")
print("=" * 60)

def fibonacci_stream() -> Generator[int, None, None]:
    """
    An infinite generator yielding Fibonacci numbers: 0, 1, 1, 2, 3, 5, 8, ...
    Because it is lazy, having an infinite while loop is completely safe!
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci_stream()
first_10_fib = [next(fib) for _ in range(10)]
print(f"First 10 Fibonacci numbers from infinite stream: {first_10_fib}")

# Pulling 5 more picks up right where it left off
next_5_fib = [next(fib) for _ in range(5)]
print(f"Next 5 Fibonacci numbers: {next_5_fib}")


# =====================================================================
# 4. Multi-Stage Generator Pipelines
# =====================================================================
print("\n" + "=" * 60)
print("4. Multi-Stage Streaming Pipelines")
print("=" * 60)

def raw_telemetry_stream(count: int) -> Generator[str, None, None]:
    """Stage 1: Generates raw simulated log records."""
    for i in range(count):
        status = 500 if i % 4 == 0 else 200
        latency_ms = (i * 17) % 250
        yield f"timestamp=2026-09-21T15:{i:02d}:00Z status={status} latency={latency_ms}ms"

def parse_telemetry(lines: Iterable[str]) -> Generator[Dict[str, Any], None, None]:
    """Stage 2: Parses raw log strings into structured dictionaries."""
    for line in lines:
        parts = line.split()
        data = {}
        for part in parts:
            key, val = part.split("=")
            if key == "status":
                data[key] = int(val)
            elif key == "latency":
                data[key] = int(val.rstrip("ms"))
            else:
                data[key] = val
        yield data

def filter_server_errors(records: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    """Stage 3: Filters records, passing through only 500 errors."""
    for record in records:
        if record.get("status") == 500:
            yield record

# Assemble and run the pipeline
# Note: No data is processed until we iterate through the final consumer!
raw_logs = raw_telemetry_stream(12)
parsed_logs = parse_telemetry(raw_logs)
error_logs = filter_server_errors(parsed_logs)

print("Processing pipeline stages lazily:")
for err in error_logs:
    print(f"  [ALERT] Encountered error: time={err['timestamp']} latency={err['latency']}ms")


# =====================================================================
# 5. Delegating Generators: yield from
# =====================================================================
print("\n" + "=" * 60)
print("5. Subgenerator Delegation with 'yield from'")
print("=" * 60)

def batch_one() -> Generator[str, None, None]:
    yield "agent_auth_ok"
    yield "session_initialized"

def batch_two() -> Generator[str, None, None]:
    yield "prompt_submitted"
    yield "response_streamed"
    yield "session_closed"

def combined_audit_trail() -> Generator[str, None, None]:
    """Delegates sequence generation directly to subgenerators."""
    print("  -> Delegating to batch_one...")
    yield from batch_one()
    print("  -> Delegating to batch_two...")
    yield from batch_two()

events = list(combined_audit_trail())
print(f"Combined events collected: {events}")


# =====================================================================
# 6. AI Agent Pattern: Streaming LLM Tokens with Real-Time Buffering
# =====================================================================
print("\n" + "=" * 60)
print("6. AI Agent Pattern: Streaming Token Generator")
print("=" * 60)

def mock_llm_token_stream(prompt: str) -> Generator[str, None, None]:
    """
    Simulates streaming tokens arriving over a network socket from an LLM.
    In a real agent, this consumes chunked SSE packets.
    """
    sample_tokens = [
        "Plan", ": ", "1", ".", " Search", " database", " for", " active",
        " agents", ".\n", "2", ".", " Compute", " aggregate", " metrics", ".\n",
        "Done", "!"
    ]
    for token in sample_tokens:
        yield token

def word_buffer_pipeline(token_stream: Iterable[str]) -> Generator[str, None, None]:
    """
    Buffer incomplete sub-tokens and yield complete words or sentences.
    Ensures agent output parsing doesn't break across token splits.
    """
    buffer = ""
    for token in token_stream:
        buffer += token
        if " " in buffer or "\n" in buffer:
            yield buffer
            buffer = ""
    if buffer:
        yield buffer

print("Consuming simulated LLM stream:")
full_response = ""
for chunk in word_buffer_pipeline(mock_llm_token_stream("Summarize next steps")):
    full_response += chunk
    print(f"  [STREAM CHUNK]: {repr(chunk)}")

print("\nFinal assembled agent output:")
print(full_response.strip())

print("\n" + "=" * 60)
print("Lesson 17 complete: Generators mastered successfully!")
print("=" * 60)
