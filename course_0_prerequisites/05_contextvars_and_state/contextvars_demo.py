"""contextvars_demo.py - Demonstrates ContextVar usage, task inheritance, and token management.

Key concepts demonstrated:
1. Defining and setting ContextVar instances.
2. Context inheritance across nested coroutines and asyncio.create_task.
3. Clean token management with ScopedContext context manager.
"""

import asyncio
import contextvars
from typing import Generator, Any
from contextlib import contextmanager

# Global context variables for tracing agent workflows
trace_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id_var", default="trace_root")
agent_step_var: contextvars.ContextVar[int] = contextvars.ContextVar("agent_step_var", default=0)


@contextmanager
def scoped_context(var: contextvars.ContextVar[Any], value: Any) -> Generator[None, None, None]:
    """Context manager for guaranteed token reset."""
    token = var.set(value)
    try:
        yield
    finally:
        var.reset(token)


async def deep_tool_helper(action_name: str) -> str:
    """A deeply nested helper that reads context without receiving it in arguments."""
    current_trace = trace_id_var.get()
    current_step = agent_step_var.get()
    return f"Helper [{action_name}] executed under trace={current_trace}, step={current_step}"


async def agent_action_step(step_number: int) -> str:
    """An agent reasoning step setting step-local state."""
    with scoped_context(agent_step_var, step_number):
        # Calls deeply nested helper without passing step_number
        result = await deep_tool_helper("search_kb")
        return result


async def run_agent_workflow(workflow_id: str) -> list[str]:
    """Simulates an entire agent workflow with its own trace ID."""
    with scoped_context(trace_id_var, workflow_id):
        # Run three consecutive steps
        res1 = await agent_action_step(1)
        res2 = await agent_action_step(2)
        res3 = await agent_action_step(3)
        return [res1, res2, res3]


async def main() -> None:
    print("=== Module 05: ContextVars & Task-Scoped State Demo ===")

    # Baseline verification
    assert trace_id_var.get() == "trace_root"
    assert agent_step_var.get() == 0

    # Run workflow 1
    wf1_results = await run_agent_workflow("wf_alpha_101")
    for line in wf1_results:
        print(f"[Workflow 1 Output] {line}")
        assert "trace=wf_alpha_101" in line

    # Verify context reset back to root
    assert trace_id_var.get() == "trace_root"
    assert agent_step_var.get() == 0
    print("[OK] ScopedContext cleanly reset state back to defaults.")

    # Verify child task inheritance
    async def child_task():
        return trace_id_var.get()

    token = trace_id_var.set("trace_parent_task")
    child = asyncio.create_task(child_task())
    child_trace = await child
    assert child_trace == "trace_parent_task", f"Expected trace_parent_task, got {child_trace}"
    trace_id_var.reset(token)
    print(f"[OK] Child task inherited parent context: {child_trace}")

    print("All tests in contextvars_demo.py completed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
