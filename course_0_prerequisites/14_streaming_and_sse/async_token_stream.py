"""async_token_stream.py - Demonstrates asynchronous generators and live token streaming.

Key concepts demonstrated:
1. Defining and consuming an AsyncGenerator (async def ... yield).
2. Simulating per-token neural network generation latency.
3. Live streaming display without newline breaks.
"""

import asyncio
import time
from typing import AsyncGenerator, List


async def simulate_token_stream(prompt: str, delay_ms: float = 15.0) -> AsyncGenerator[str, None]:
    """Asynchronous generator yielding tokens one by one."""
    sample_response = (
        f"Synthesizing thoughts for query '{prompt}': "
        "Autonomous agents leverage async event loops, contextvars for state, "
        "and SQLite memory for persistent multi-turn reasoning."
    )
    tokens = sample_response.split(" ")

    for i, token in enumerate(tokens):
        await asyncio.sleep(delay_ms / 1000.0)
        yield token + (" " if i < len(tokens) - 1 else "")


async def main() -> None:
    print("=== Module 14: Async Token Streaming Demo ===")

    start_time = time.perf_counter()
    accumulated_tokens: List[str] = []

    print("Live token output: ", end="", flush=True)
    async for token in simulate_token_stream("Explain agent architecture", delay_ms=10.0):
        print(token, end="", flush=True)
        accumulated_tokens.append(token)
    print("\n")

    elapsed = time.perf_counter() - start_time
    full_text = "".join(accumulated_tokens)

    # Assertions
    assert len(accumulated_tokens) > 10
    assert "Autonomous agents leverage async event loops" in full_text
    assert elapsed >= 0.15, f"Expected elapsed time >= 0.15s, got {elapsed:.3f}s"

    print(f"[OK] Streamed {len(accumulated_tokens)} tokens in {elapsed:.3f}s")
    print("All tests in async_token_stream.py passed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
