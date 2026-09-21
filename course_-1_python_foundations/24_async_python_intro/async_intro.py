"""Module 24: Async Python Introduction"""
import asyncio, time

async def fetch_data(source: str, delay: float) -> str:
    """Simulate fetching data (e.g. LLM API call)."""
    print(f"  Fetching from {source}...")
    await asyncio.sleep(delay)    # yield control to event loop
    return f"Data from {source}"

async def main():
    # Sequential:
    t0 = time.perf_counter()
    r1 = await fetch_data("LLM",  2.0)
    r2 = await fetch_data("Tool", 1.0)
    seq_time = time.perf_counter() - t0
    print(f"Sequential: {seq_time:.2f}s")

    # Concurrent with gather:
    t0 = time.perf_counter()
    r1, r2 = await asyncio.gather(
        fetch_data("LLM",  2.0),
        fetch_data("Tool", 1.0),
    )
    con_time = time.perf_counter() - t0
    print(f"Concurrent: {con_time:.2f}s")
    print(f"Speedup: {seq_time/con_time:.1f}x")

asyncio.run(main())
