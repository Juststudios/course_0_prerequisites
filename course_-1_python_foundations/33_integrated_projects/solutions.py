"""
Module 33 Solutions: Integrated Projects — The Mini ReAct Agent Pipeline
========================================================================
Reference implementations for all 4 levels of Module 33 exercises.
"""

import inspect
import sqlite3
from typing import Any, Callable, Dict, List, Optional


# =====================================================================
# LEVEL 1: RECALL — Tool Parameter Validator Solution
# =====================================================================

def validate_tool_arguments(func: Callable[..., Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Validates that kwargs satisfy the callable signature of func."""
    if not callable(func):
        raise TypeError(f"Expected callable, got {type(func).__name__}")

    sig = inspect.signature(func)
    has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())

    required_params = {
        name for name, p in sig.parameters.items()
        if p.default is inspect.Parameter.empty and p.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    }

    all_named_params = {
        name for name, p in sig.parameters.items()
        if p.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    }

    missing = sorted([p for p in required_params if p not in kwargs])
    extra = [] if has_var_keyword else sorted([k for k in kwargs if k not in all_named_params])
    valid = (len(missing) == 0 and len(extra) == 0)

    return {
        "valid": valid,
        "missing": missing,
        "extra": extra,
    }


# =====================================================================
# LEVEL 2: MODIFY — Filtered Agent Memory Solution
# =====================================================================

class FilteredAgentMemory:
    """Enhanced persistent SQLite memory with filtering and metrics."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id   TEXT NOT NULL,
                tool         TEXT NOT NULL,
                status       TEXT NOT NULL,
                duration_ms  REAL NOT NULL
            )
        """)
        self.conn.commit()

    def save(self, session_id: str, tool: str, status: str, duration_ms: float) -> int:
        """Inserts interaction record and returns row id."""
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO interactions (session_id, tool, status, duration_ms)
            VALUES (?, ?, ?, ?)
        """, (session_id, tool, status, duration_ms))
        self.conn.commit()
        return cur.lastrowid or -1

    def query(
        self,
        session_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Queries interactions matching non-None session_id and status filters."""
        query_sql = "SELECT id, session_id, tool, status, duration_ms FROM interactions"
        filters = []
        params = []

        if session_id is not None:
            filters.append("session_id = ?")
            params.append(session_id)

        if status is not None:
            filters.append("status = ?")
            params.append(status)

        if filters:
            query_sql += " WHERE " + " AND ".join(filters)

        query_sql += " ORDER BY id ASC"

        cur = self.conn.cursor()
        cur.execute(query_sql, params)
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "session_id": r[1],
                "tool": r[2],
                "status": r[3],
                "duration_ms": r[4],
            }
            for r in rows
        ]

    def get_success_rate(self, tool: str) -> float:
        """Calculates success rate (0.0 to 1.0) for the specified tool."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT
                COUNT(*),
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END)
            FROM interactions
            WHERE tool = ?
        """, (tool,))
        row = cur.fetchone()
        if not row or row[0] == 0:
            return 0.0
        total_calls = row[0]
        successful_calls = row[1] or 0
        return float(successful_calls) / float(total_calls)

    def close(self) -> None:
        self.conn.close()


# =====================================================================
# LEVEL 3: BUILD — Multi-Step ReAct Loop Engine Solution
# =====================================================================

class ReActLoopEngine:
    """Executes multi-step ReAct reasoning sequences with tool dispatch and guardrails."""

    def __init__(self, registry: Dict[str, Callable[..., Any]], max_steps: int = 5) -> None:
        self.registry = dict(registry)
        self.max_steps = max_steps

    def step(self, thought: str, action: str, action_input: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a single ReAct step."""
        if action == "final_answer":
            answer = action_input.get("answer", "")
            return {
                "thought": thought,
                "action": "final_answer",
                "observation": answer,
                "status": "finished",
            }

        if action not in self.registry:
            return {
                "thought": thought,
                "action": action,
                "observation": f"Error: Tool '{action}' not found",
                "status": "error",
            }

        try:
            func = self.registry[action]
            result = func(**action_input)
            return {
                "thought": thought,
                "action": action,
                "observation": result,
                "status": "success",
            }
        except Exception as exc:
            return {
                "thought": thought,
                "action": action,
                "observation": f"Error: {type(exc).__name__}: {exc}",
                "status": "error",
            }

    def run_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executes a sequence of steps up to completion or max_steps."""
        trace: List[Dict[str, Any]] = []
        completed = False
        final_answer = None

        for item in plan:
            if len(trace) >= self.max_steps:
                break

            thought = item.get("thought", "")
            action = item.get("action", "")
            action_input = item.get("action_input", {})

            step_res = self.step(thought, action, action_input)
            trace.append(step_res)

            if step_res["status"] == "finished":
                completed = True
                final_answer = step_res["observation"]
                break

        return {
            "total_steps": len(trace),
            "completed": completed,
            "final_answer": final_answer,
            "trace": trace,
        }


# =====================================================================
# LEVEL 4: DEBUG — Repaired Agent Pipeline Solution
# =====================================================================

class RepairedAgentPipeline:
    """The corrected, reliable, and isolated agent execution pipeline."""

    def __init__(self, tools: Optional[Dict[str, Callable[..., Any]]] = None) -> None:
        # Avoid mutable default argument state pollution
        self.tools: Dict[str, Callable[..., Any]] = dict(tools) if tools is not None else {}
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE IF NOT EXISTS log (tool TEXT, result TEXT)")
        self.conn.commit()

    def register(self, name: str, func: Callable[..., Any]) -> None:
        """Registers a tool into this pipeline instance."""
        self.tools[name] = func

    def execute(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Safely executes tool, commits to SQLite, and returns structured result."""
        if name not in self.tools:
            return {"status": "error", "error": f"Tool '{name}' not found"}

        try:
            res = self.tools[name](**kwargs)
            self.conn.execute("INSERT INTO log VALUES (?, ?)", (name, str(res)))
            # Fix: Ensure transaction is committed
            self.conn.commit()
            return {"status": "ok", "result": res}
        except Exception as err:
            return {"status": "error", "error": f"{type(err).__name__}: {err}"}

    def get_log_count(self) -> int:
        """Returns count of recorded log rows."""
        row = self.conn.execute("SELECT COUNT(*) FROM log").fetchone()
        return row[0] if row else 0


# =====================================================================
# VERIFICATION RUNNER
# =====================================================================

def verify_module_33() -> None:
    print("Verifying Module 33 Solutions...")

    # --- Test Level 1: validate_tool_arguments ---
    def add_numbers(x: int, y: int, round_digits: int = 2) -> float:
        return round(x + y, round_digits)

    # Valid call
    v1 = validate_tool_arguments(add_numbers, {"x": 5, "y": 10})
    assert v1["valid"] is True
    assert v1["missing"] == []
    assert v1["extra"] == []

    # Missing required argument 'y'
    v2 = validate_tool_arguments(add_numbers, {"x": 5})
    assert v2["valid"] is False
    assert v2["missing"] == ["y"]

    # Extra unexpected argument 'unexpected'
    v3 = validate_tool_arguments(add_numbers, {"x": 5, "y": 10, "unexpected": True})
    assert v3["valid"] is False
    assert v3["extra"] == ["unexpected"]

    # Function with **kwargs allows extra kwargs
    def flexible_tool(a: str, **kwargs: Any) -> str:
        return a

    v4 = validate_tool_arguments(flexible_tool, {"a": "ok", "extra_param": 123})
    assert v4["valid"] is True
    assert v4["extra"] == []

    # Verify non-callable raises TypeError
    try:
        validate_tool_arguments("not_a_func", {})  # type: ignore
        assert False, "Should have raised TypeError"
    except TypeError:
        pass
    print("  [✓] Level 1 (Recall) passed!")

    # --- Test Level 2: FilteredAgentMemory ---
    mem = FilteredAgentMemory()
    id1 = mem.save("sess-1", "search", "success", 120.5)
    id2 = mem.save("sess-1", "calculate", "success", 15.0)
    id3 = mem.save("sess-1", "search", "error", 200.0)
    id4 = mem.save("sess-2", "search", "success", 95.0)

    assert id1 == 1 and id4 == 4

    # Query all
    all_rows = mem.query()
    assert len(all_rows) == 4

    # Query by session
    s1_rows = mem.query(session_id="sess-1")
    assert len(s1_rows) == 3

    # Query by status
    err_rows = mem.query(status="error")
    assert len(err_rows) == 1
    assert err_rows[0]["id"] == 3

    # Check success rate: search has 2 successes out of 3 total -> 2/3 = ~0.6667
    rate_search = mem.get_success_rate("search")
    assert abs(rate_search - (2.0 / 3.0)) < 0.001

    # Tool with 100% success rate
    rate_calc = mem.get_success_rate("calculate")
    assert rate_calc == 1.0

    # Unknown tool returns 0.0
    assert mem.get_success_rate("unknown") == 0.0
    print("  [✓] Level 2 (Modify) passed!")

    # --- Test Level 3: ReActLoopEngine ---
    registry = {
        "double": lambda n: n * 2,
        "greet": lambda name: f"Hello, {name}!",
        "div": lambda a, b: a / b,
    }
    engine = ReActLoopEngine(registry=registry, max_steps=4)

    plan = [
        {"thought": "Double 21 to get 42", "action": "double", "action_input": {"n": 21}},
        {"thought": "Divide by zero to test error capture", "action": "div", "action_input": {"a": 10, "b": 0}},
        {"thought": "Call unknown tool", "action": "missing_tool", "action_input": {}},
        {"thought": "We reached final answer", "action": "final_answer", "action_input": {"answer": "Computation finished!"}},
    ]

    result = engine.run_plan(plan)
    assert result["total_steps"] == 4
    assert result["completed"] is True
    assert result["final_answer"] == "Computation finished!"
    assert result["trace"][0]["status"] == "success"
    assert result["trace"][0]["observation"] == 42
    assert result["trace"][1]["status"] == "error"
    assert "ZeroDivisionError" in result["trace"][1]["observation"]
    assert result["trace"][2]["status"] == "error"
    assert "missing_tool" in result["trace"][2]["observation"]

    # Test max_steps constraint
    truncated_plan = [
        {"thought": "Step 1", "action": "double", "action_input": {"n": 1}},
        {"thought": "Step 2", "action": "double", "action_input": {"n": 2}},
        {"thought": "Step 3", "action": "double", "action_input": {"n": 3}},
        {"thought": "Step 4", "action": "double", "action_input": {"n": 4}},
        {"thought": "Step 5", "action": "final_answer", "action_input": {"answer": "Never reached"}},
    ]
    truncated_res = engine.run_plan(truncated_plan)
    assert truncated_res["total_steps"] == 4  # Stopped at max_steps=4
    assert truncated_res["completed"] is False
    assert truncated_res["final_answer"] is None
    print("  [✓] Level 3 (Build) passed!")

    # --- Test Level 4: RepairedAgentPipeline ---
    p1 = RepairedAgentPipeline()
    p2 = RepairedAgentPipeline()

    p1.register("tool_a", lambda x: x + 10)
    assert "tool_a" not in p2.tools, "Tools must not bleed across instances!"

    res_ok = p1.execute("tool_a", x=5)
    assert res_ok["status"] == "ok"
    assert res_ok["result"] == 15
    assert p1.get_log_count() == 1
    assert p2.get_log_count() == 0

    # Error handling
    res_err_missing = p1.execute("non_existent")
    assert res_err_missing["status"] == "error"

    p1.register("fail_tool", lambda: 1 / 0)
    res_err_crash = p1.execute("fail_tool")
    assert res_err_crash["status"] == "error"
    assert "ZeroDivisionError" in res_err_crash["error"]
    print("  [✓] Level 4 (Debug) passed!")

    print("All Module 33 solutions verified successfully!\n")


if __name__ == "__main__":
    verify_module_33()
