"""dunder_patterns.py - Demonstrates Python dunder methods and context managers.

Key concepts demonstrated:
1. __repr__ and __str__ for formatted agent trace inspection.
2. __getitem__, __len__, and __iter__ for dictionary-like conversation history.
3. Synchronous & Asynchronous Context Managers (__enter__/__exit__, __aenter__/__aexit__).
"""

from typing import List, Dict, Any, Iterator
import time
import asyncio


class AgentMessage:
    """Represents a single message turn with custom string representations."""

    def __init__(self, role: str, content: str, tool_name: str | None = None) -> None:
        self.role = role
        self.content = content
        self.tool_name = tool_name
        self.timestamp = time.time()

    def __repr__(self) -> str:
        """Developer-friendly unambiguous representation for logs and debugging."""
        tool_clause = f", tool={self.tool_name!r}" if self.tool_name else ""
        return f"AgentMessage(role={self.role!r}, content={self.content[:20]!r}...{tool_clause})"

    def __str__(self) -> str:
        """User-facing clean formatted text for prompt rendering."""
        prefix = f"[{self.role.upper()}]"
        if self.tool_name:
            prefix += f" (tool: {self.tool_name})"
        return f"{prefix}: {self.content}"


class ConversationHistory:
    """Collection implementing list/sequence dunder methods."""

    def __init__(self) -> None:
        self._history: List[AgentMessage] = []

    def append(self, role: str, content: str, tool_name: str | None = None) -> None:
        self._history.append(AgentMessage(role, content, tool_name))

    def __len__(self) -> int:
        return len(self._history)

    def __getitem__(self, index: int) -> AgentMessage:
        return self._history[index]

    def __iter__(self) -> Iterator[AgentMessage]:
        return iter(self._history)

    def __contains__(self, role: str) -> bool:
        return any(msg.role == role for msg in self._history)


class ExecutionTraceSpan:
    """Context manager for tracking tool execution time and error state."""

    def __init__(self, span_name: str) -> None:
        self.span_name = span_name
        self.start_time: float = 0.0
        self.duration_ms: float = 0.0
        self.success: bool = False

    def __enter__(self) -> "ExecutionTraceSpan":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        self.duration_ms = (time.perf_counter() - self.start_time) * 1000.0
        if exc_type is None:
            self.success = True
        else:
            self.success = False
        # Do not suppress exceptions
        return False


class AsyncResourceGuard:
    """Asynchronous context manager managing an async resource lock."""

    def __init__(self, resource_name: str) -> None:
        self.resource_name = resource_name
        self.acquired = False

    async def __aenter__(self) -> "AsyncResourceGuard":
        await asyncio.sleep(0.01)  # Simulate async resource acquisition
        self.acquired = True
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        await asyncio.sleep(0.01)  # Simulate async resource cleanup
        self.acquired = False
        return False


def test_sync_dunders() -> None:
    history = ConversationHistory()
    history.append("system", "You are an autonomous engineering assistant.")
    history.append("user", "Calculate the trajectory of a rocket.", tool_name=None)
    history.append("tool", "Velocity: 11.2 km/s", tool_name="orbital_calc")

    assert len(history) == 3, f"Expected 3 messages, got {len(history)}"
    assert history[0].role == "system"
    assert "user" in history
    assert "assistant" not in history

    # Check __repr__ and __str__
    str_view = str(history[2])
    assert "[TOOL] (tool: orbital_calc): Velocity: 11.2 km/s" == str_view
    repr_view = repr(history[1])
    assert "AgentMessage(role='user'" in repr_view

    print("[OK] Synchronous dunder methods (__len__, __getitem__, __repr__, __str__) verified.")


def test_trace_context() -> None:
    with ExecutionTraceSpan("vector_search") as span:
        time.sleep(0.02)
        assert span.start_time > 0

    assert span.success is True
    assert span.duration_ms >= 15.0, f"Expected duration >= 15ms, got {span.duration_ms}"
    print(f"[OK] Context manager completed: span {span.span_name} in {span.duration_ms:.2f}ms")

    # Test error capture in context manager
    span_err = ExecutionTraceSpan("failing_tool")
    try:
        with span_err:
            raise ValueError("Simulated tool crash")
    except ValueError:
        pass

    assert span_err.success is False
    assert span_err.duration_ms > 0
    print("[OK] Context manager properly recorded failure without swallowing exception.")


async def test_async_context() -> None:
    guard = AsyncResourceGuard("gpu_tensor_cache")
    assert guard.acquired is False
    async with guard as active_guard:
        assert active_guard.acquired is True
    assert guard.acquired is False
    print("[OK] Async context manager (__aenter__/__aexit__) verified cleanly.")


def main() -> None:
    print("=== Module 02: Dunder Patterns & Context Managers Demo ===")
    test_sync_dunders()
    test_trace_context()
    asyncio.run(test_async_context())
    print("All tests in dunder_patterns.py completed successfully!\n")


if __name__ == "__main__":
    main()
