"""Module 25: Async Concurrency"""
import asyncio, time

# MATHEMATICAL MODEL
# If tasks A=2s, B=3s, C=1s:
# Sequential:  T = 2+3+1 = 6 seconds
# Concurrent:  T ≈ max(2,3,1) = 3 seconds  (idealized)
# Speedup ≈ 6/3 = 2x
# Reality: overhead means speedup is slightly less than ideal.

async def task(name: str, duration: float) -> str:
    await asyncio.sleep(duration)
    return f"{name} done"

async def main():
    tasks = [
        task("A", 2.0),
        task("B", 3.0),
        task("C", 1.0),
    ]
    t0 = time.perf_counter()
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - t0
    print(f"Results: {results}")
    print(f"Actual time: {elapsed:.2f}s (sequential would be 6s)")

asyncio.run(main())
