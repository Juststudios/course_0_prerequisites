"""test_mini_agent.py - Comprehensive pytest suite for MiniAgent Capstone project."""

import pytest
import asyncio
import sqlite3
import os

from course_0_prerequisites.mini_agent.config import AgentConfig
from course_0_prerequisites.mini_agent.models import (
    MessageRole,
    ToolCall,
    ToolResult,
    AgentStep,
    AgentResponse,
)
from course_0_prerequisites.mini_agent.memory import SQLiteMemory
from course_0_prerequisites.mini_agent.tools import (
    ToolRegistry,
    SafeASTCalculator,
    default_registry,
    calculator,
    local_search,
    run_python,
    get_time,
)
from course_0_prerequisites.mini_agent.engine import DeterministicReActEngine
from course_0_prerequisites.mini_agent.agent import MiniAgent, trace_id_ctx, session_id_ctx


# ==============================================================================
# 1. Tool System & Safe AST Calculator Tests
# ==============================================================================

def test_safe_ast_calculator_valid():
    """Verifies that mathematical expressions evaluate correctly without eval()."""
    assert SafeASTCalculator.evaluate("10 + 25") == 35.0
    assert SafeASTCalculator.evaluate("(15 * 4) + (100 / 5)") == 80.0
    assert SafeASTCalculator.evaluate("2 ** 3") == 8.0
    assert SafeASTCalculator.evaluate("-5 + 10") == 5.0
    assert SafeASTCalculator.evaluate("100 % 7") == 2.0


def test_safe_ast_calculator_division_by_zero():
    """Verifies that division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        SafeASTCalculator.evaluate("42 / 0")


def test_safe_ast_calculator_disallowed_syntax():
    """Verifies that arbitrary code execution, functions, and imports are blocked."""
    with pytest.raises(ValueError):
        SafeASTCalculator.evaluate("__import__('os').system('ls')")

    with pytest.raises(ValueError):
        SafeASTCalculator.evaluate("abs(-5)")

    with pytest.raises(ValueError):
        SafeASTCalculator.evaluate("x = 10")


def test_tool_registry_schemas_and_execution():
    """Verifies registering tools, extracting JSON schemas, and error boundaries."""
    registry = ToolRegistry()

    @registry.register
    def dummy_tool(name: str, count: int = 1) -> str:
        """A test tool for unit testing.

        Args:
            name: The target name.
            count: Number of repetitions.
        """
        return f"{name} " * count

    schemas = registry.get_schemas()
    assert len(schemas) == 1
    assert schemas[0]["function"]["name"] == "dummy_tool"
    assert "name" in schemas[0]["function"]["parameters"]["required"]
    assert "count" not in schemas[0]["function"]["parameters"]["required"]

    # Test clean execution
    res = registry.execute("dummy_tool", name="agent", count=2)
    assert res.success is True
    assert res.output == "agent agent "

    # Test execution error boundary
    res_err = registry.execute("dummy_tool")  # Missing required arg
    assert res_err.success is False
    assert "missing" in res_err.error.lower() or "typeerror" in res_err.error.lower()

    # Test non-existent tool
    res_missing = registry.execute("unknown_tool")
    assert res_missing.success is False
    assert "not found" in res_missing.error


def test_builtin_tools():
    """Verifies default registered tools."""
    # Calculator tool
    calc_res = default_registry.execute("calculator", expression="50 * 2")
    assert calc_res.success is True
    assert calc_res.output == 100.0

    # Local search tool
    search_res = default_registry.execute("local_search", query="python async")
    assert search_res.success is True
    assert isinstance(search_res.output, list)
    assert len(search_res.output) > 0

    # Run Python tool
    py_res = default_registry.execute("run_python", code="print(7 * 6)")
    assert py_res.success is True
    assert "42" in py_res.output

    # Get time tool
    time_res = default_registry.execute("get_time")
    assert time_res.success is True
    assert "UTC" in time_res.output


# ==============================================================================
# 2. SQLite Memory Tests
# ==============================================================================

def test_sqlite_memory_crud_and_sliding_window():
    """Verifies message storage, sliding window retrieval, and session cleanup."""
    memory = SQLiteMemory(db_path=":memory:")
    session = "test_sess_01"

    memory.add_message(session, MessageRole.SYSTEM.value, "System instructions.")
    memory.add_message(session, MessageRole.USER.value, "Message 1")
    memory.add_message(session, MessageRole.ASSISTANT.value, "Message 2")
    memory.add_message(session, MessageRole.USER.value, "Message 3")

    history = memory.get_history(session, limit=2)
    assert len(history) == 2
    # Verify chronological order
    assert history[0]["content"] == "Message 2"
    assert history[1]["content"] == "Message 3"

    # Test audit logging
    memory.log_tool_call(
        session_id=session,
        trace_id="tr_101",
        tool_name="calculator",
        args={"expression": "1+1"},
        result=2.0,
        success=True,
        duration_ms=12.5
    )

    audits = memory.get_audit_logs(session)
    assert len(audits) == 1
    assert audits[0]["tool_name"] == "calculator"
    assert audits[0]["success"] is True

    # Test clear history
    memory.clear_history(session)
    assert len(memory.get_history(session)) == 0
    assert len(memory.get_audit_logs(session)) == 0
    memory.close()


# ==============================================================================
# 3. DeterministicReActEngine Tests
# ==============================================================================

def test_react_engine_arithmetic_plan():
    """Verifies that engine plans a calculator step and synthesizes an answer."""
    engine = DeterministicReActEngine()
    available = ["calculator", "local_search"]

    # Step 1: Initial user query
    thought1, tool1, final1 = engine.plan_next_step(
        query="What is 15 + 35?",
        history=[],
        steps=[],
        available_tools=available
    )
    assert tool1 is not None
    assert tool1.tool_name == "calculator"
    assert final1 is None

    # Step 2: With tool observation
    step1 = AgentStep(
        step_number=1,
        thought=thought1,
        tool_call=tool1,
        observation="50.0"
    )
    thought2, tool2, final2 = engine.plan_next_step(
        query="What is 15 + 35?",
        history=[],
        steps=[step1],
        available_tools=available
    )
    assert tool2 is None
    assert final2 is not None
    assert "50.0" in final2


# ==============================================================================
# 4. End-to-End MiniAgent Asynchronous Execution Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_mini_agent_e2e_math_task():
    """Verifies end-to-end task execution for arithmetic query."""
    config = AgentConfig(agent_name="TestAgent", max_steps=4, verbose=False)
    memory = SQLiteMemory(db_path=":memory:")
    agent = MiniAgent(
        config=config,
        memory=memory,
        tools=default_registry,
        engine=DeterministicReActEngine()
    )

    resp = await agent.run("What is (25 * 4) + (100 / 5)?", session_id="test_math")
    assert resp.success is True
    assert "120.0" in resp.final_answer
    assert len(resp.steps) == 1
    assert resp.steps[0].tool_call.tool_name == "calculator"

    # Verify memory persistence
    history = memory.get_history("test_math")
    assert len(history) == 2  # 1 user message + 1 assistant message
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"

    # Verify audit log
    audit = memory.get_audit_logs("test_math")
    assert len(audit) == 1
    assert audit[0]["tool_name"] == "calculator"


@pytest.mark.asyncio
async def test_mini_agent_e2e_search_task():
    """Verifies end-to-end task execution for local knowledge search."""
    config = AgentConfig(agent_name="TestAgent", max_steps=4, verbose=False)
    memory = SQLiteMemory(db_path=":memory:")
    agent = MiniAgent(
        config=config,
        memory=memory,
        tools=default_registry,
        engine=DeterministicReActEngine()
    )

    resp = await agent.run("Search for python async", session_id="test_search")
    assert resp.success is True
    assert len(resp.steps) == 1
    assert resp.steps[0].tool_call.tool_name == "local_search"
    assert "documentation" in resp.final_answer.lower() or "async" in resp.final_answer.lower()


@pytest.mark.asyncio
async def test_mini_agent_e2e_python_subprocess():
    """Verifies end-to-end task execution running a safe Python script."""
    config = AgentConfig(agent_name="TestAgent", max_steps=4, verbose=False)
    memory = SQLiteMemory(db_path=":memory:")
    agent = MiniAgent(
        config=config,
        memory=memory,
        tools=default_registry,
        engine=DeterministicReActEngine()
    )

    resp = await agent.run("Run python script to compute squares", session_id="test_py")
    assert resp.success is True
    assert len(resp.steps) == 1
    assert resp.steps[0].tool_call.tool_name == "run_python"
    assert "[1, 4, 9, 16, 25]" in resp.final_answer


@pytest.mark.asyncio
async def test_mini_agent_contextvar_trace_propagation():
    """Verifies that trace_id and session_id ContextVars propagate correctly."""
    config = AgentConfig(agent_name="TraceAgent", max_steps=2, verbose=False)
    agent = MiniAgent(config=config)

    # Initial context values
    assert trace_id_ctx.get() == "untraced"
    assert session_id_ctx.get() == "default"

    resp = await agent.run("What time is it?", session_id="session_ctx_test")
    assert resp.success is True
    assert resp.trace_id.startswith("trace_")

    # Ensure context was reset after run
    assert trace_id_ctx.get() == "untraced"
    assert session_id_ctx.get() == "default"
