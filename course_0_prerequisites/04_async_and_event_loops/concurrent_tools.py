"""concurrent_tools.py - Demonstrates semaphore throttling and timeout protection for agent tools.

Key concepts demonstrated:
1. Throttling concurrent tool execution using asyncio.Semaphore.
2. Protecting against hanging tools using asyncio.wait_for.
3. Resilient batch execution with asyncio.gather(..., return_exceptions=True).
"""

import asyncio
import time
from typing import List, Any, Dict


class ThrottledToolExecutor:
    """Executes a batch of asynchronous tools while enforcing concurrency limits and timeouts."""

    def __init__(self, max_concurrency: int = 2, timeout_seconds: float = 0.2) -> None:
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.timeout_seconds = timeout_seconds
        self.active_count = 0
        self.max_observed_concurrency = 0

    async def execute_tool(self, tool_name: str, delay: float, should_fail: bool = False) -> Dict[str, Any]:
        """Runs a simulated tool under semaphore and timeout boundaries."""
        async with self.semaphore:
            self.active_count += 1
            self.max_observed_concurrency = max(self.max_observed_concurrency, self.active_count)
            try:
                # Wrap with timeout
                result = await asyncio.wait_for(
                    self._simulated_tool_body(tool_name, delay, should_fail),
                    timeout=self.timeout_seconds
                )
                return {"tool": tool_name, "status": "success", "result": result}
            except asyncio.TimeoutError:
                return {"tool": tool_name, "status": "timeout", "error": f"Exceeded {self.timeout_seconds}s limit"}
            except Exception as e:
                return {"tool": tool_name, "status": "error", "error": str(e)}
            finally:
                self.active_count -= 1

    async def _simulated_tool_body(self, tool_name: str, delay: float, should_fail: bool) -> str:
        await asyncio.sleep(delay)
        if should_fail:
            raise RuntimeError(f"Tool '{tool_name}' encountered internal error")
        return f"Result from {tool_name}"

    async def run_batch(self, tool_specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Runs an arbitrary batch of tool calls concurrently."""
        tasks = [
            self.execute_tool(
                spec["name"],
                spec.get("delay", 0.05),
                spec.get("fail", False)
            )
            for spec in tool_specs
        ]
        return await asyncio.gather(*tasks, return_exceptions=False)


async def main() -> None:
    print("=== Module 04: Concurrent Tools & Rate Limiting Demo ===")

    executor = ThrottledToolExecutor(max_concurrency=2, timeout_seconds=0.1)

    tools_to_run = [
        {"name": "fast_search", "delay": 0.02, "fail": False},
        {"name": "calculator", "delay": 0.03, "fail": False},
        {"name": "slow_external_api", "delay": 0.25, "fail": False},  # Will timeout (0.25s > 0.1s)
        {"name": "crashing_tool", "delay": 0.02, "fail": True},        # Will catch error
        {"name": "weather_lookup", "delay": 0.02, "fail": False},
    ]

    start = time.perf_counter()
    results = await executor.run_batch(tools_to_run)
    elapsed = time.perf_counter() - start

    print(f"Executed batch of {len(results)} tools in {elapsed:.3f}s")
    print(f"Max observed concurrency: {executor.max_observed_concurrency} (Semaphore cap: 2)")

    # Assertions
    assert executor.max_observed_concurrency <= 2, "Semaphore exceeded allowed concurrency limit!"
    assert len(results) == 5

    # Check statuses
    statuses = {r["tool"]: r["status"] for r in results}
    assert statuses["fast_search"] == "success"
    assert statuses["calculator"] == "success"
    assert statuses["slow_external_api"] == "timeout"
    assert statuses["crashing_tool"] == "error"
    assert statuses["weather_lookup"] == "success"

    print(f"[OK] Batch statuses verified: {statuses}")
    print("All tests in concurrent_tools.py passed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
