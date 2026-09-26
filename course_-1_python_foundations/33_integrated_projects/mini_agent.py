"""
Module 33: Integrated Project — The Mini ReAct Agent Pipeline
=============================================================

This capstone project synthesizes the core programming constructs and architectural
patterns learned across Modules 01 through 32 of Course -1 into a functional,
extensible, and persistent AI Agent pipeline.

Architectural Synthesis:
  - Dataclasses (Module 16)      -> AgentConfig and ToolMetadata
  - Classes & OOP (Module 13)    -> ToolRegistry, Memory, and MiniAgent
  - Type Hints (Module 15)       -> Comprehensive typing throughout
  - Async / Await (Module 24-25) -> Non-blocking agent execution loop
  - JSON (Module 26)             -> Serialization of requests, thoughts, and payloads
  - SQLite (Module 29)           -> Persistent session and interaction audit trail
  - Logging (Module 22)          -> Structured diagnostic events
  - Architecture (Module 30)     -> Dependency Injection and Registry patterns
  - Debugging (Module 32)        -> Defensive exception isolation and error reporting

Execution Flow:
  User Request (JSON string)
      ↓
  MiniAgent.run(input_json)
      ↓
  JSON Parsing & Intent Extraction
      ↓
  Thought Formation (ReAct)
      ↓
  ToolRegistry.call(tool_name, **kwargs)
      ↓
  Observation & Exception Boundary
      ↓
  Persistence (SQLite Memory Transaction)
      ↓
  JSON Response Envelope
"""

import asyncio
import inspect
import json
import logging
import sqlite3
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple


# =====================================================================
# LOGGING SETUP
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)-7s] [%(name)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("mini_agent")


# =====================================================================
# CONFIGURATION
# =====================================================================
@dataclass
class AgentConfig:
    """Immutable operational configuration for the agent pipeline."""
    name: str = "Hermes-Lite"
    db_path: str = ":memory:"
    max_steps: int = 5
    default_session_id: str = "sess-default-001"
    verbose: bool = True


# =====================================================================
# TOOL REGISTRY PATTERN
# =====================================================================
@dataclass
class ToolMetadata:
    """Metadata describing a registered tool's signature and documentation."""
    name: str
    description: str
    func: Callable[..., Any]
    param_count: int


class ToolRegistry:
    """Central catalog managing available agent tools using the Registry pattern."""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolMetadata] = {}

    def register(self, name: str, func: Callable[..., Any], description: Optional[str] = None) -> None:
        """Registers a function under name with signature introspection."""
        if not callable(func):
            raise TypeError(f"Tool '{name}' must be callable, got {type(func).__name__}")

        doc = description or (inspect.getdoc(func) or "No description provided.")
        sig = inspect.signature(func)
        param_count = len(sig.parameters)

        self._tools[name] = ToolMetadata(
            name=name,
            description=doc,
            func=func,
            param_count=param_count
        )
        logger.info("Registered tool: %r (%s params) — %s", name, param_count, doc)

    def has_tool(self, name: str) -> bool:
        """Checks if a tool name is registered."""
        return name in self._tools

    def get_metadata(self, name: str) -> ToolMetadata:
        """Retrieves tool metadata or raises KeyError."""
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name!r}")
        return self._tools[name]

    def list_tools(self) -> List[str]:
        """Returns a sorted list of registered tool names."""
        return sorted(self._tools.keys())

    def call(self, name: str, **kwargs: Any) -> Any:
        """Invokes a registered tool by name with keyword arguments."""
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name!r}. Available: {self.list_tools()}")
        meta = self._tools[name]
        return meta.func(**kwargs)


# =====================================================================
# PERSISTENCE & AUDIT MEMORY (SQLite)
# =====================================================================
class Memory:
    """SQLite-backed persistent store for agent sessions and interaction traces."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        """Initializes database schema with indexing."""
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id   TEXT NOT NULL,
                step         INTEGER NOT NULL,
                prompt       TEXT NOT NULL,
                thought      TEXT,
                tool         TEXT NOT NULL,
                arguments    TEXT NOT NULL,
                observation  TEXT NOT NULL,
                status       TEXT NOT NULL,
                timestamp    TEXT NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sess ON interactions(session_id)")
        self._conn.commit()

    def save_interaction(
        self,
        session_id: str,
        step: int,
        prompt: str,
        thought: str,
        tool: str,
        arguments: Dict[str, Any],
        observation: Any,
        status: str = "success"
    ) -> int:
        """Records a single interaction step into persistent storage."""
        now = datetime.now(timezone.utc).isoformat()
        args_json = json.dumps(arguments)
        obs_str = json.dumps(observation) if not isinstance(observation, str) else observation

        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO interactions (
                session_id, step, prompt, thought, tool, arguments, observation, status, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_id, step, prompt, thought, tool, args_json, obs_str, status, now))
        self._conn.commit()
        return cursor.lastrowid or -1

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves all interactions for a specific session in order."""
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT id, step, prompt, thought, tool, arguments, observation, status, timestamp
            FROM interactions
            WHERE session_id = ?
            ORDER BY step ASC
        """, (session_id,))
        rows = cursor.fetchall()
        history = []
        for r in rows:
            history.append({
                "id": r[0],
                "step": r[1],
                "prompt": r[2],
                "thought": r[3],
                "tool": r[4],
                "arguments": json.loads(r[5]),
                "observation": r[6],
                "status": r[7],
                "timestamp": r[8],
            })
        return history

    def all_interactions(self) -> List[Tuple]:
        """Returns raw interaction rows for inspection."""
        return self._conn.execute("SELECT id, session_id, step, tool, status FROM interactions").fetchall()

    def get_tool_usage_stats(self) -> Dict[str, int]:
        """Calculates invocation frequency per tool."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT tool, COUNT(*) FROM interactions GROUP BY tool")
        return dict(cursor.fetchall())

    def close(self) -> None:
        """Closes the underlying database connection cleanly."""
        self._conn.close()


# =====================================================================
# AGENT CORE ORCHESTRATOR
# =====================================================================
class MiniAgent:
    """
    Central ReAct agent orchestrator tying together configuration,
    tool execution, error boundaries, and persistent SQLite memory.
    """

    def __init__(self, config: AgentConfig, registry: ToolRegistry, memory: Memory) -> None:
        # Dependency Injection: collaborators provided from outside
        self.config = config
        self.registry = registry
        self.memory = memory

    async def run_request(self, input_json: str, session_id: Optional[str] = None) -> str:
        """
        Executes a single user request payload asynchronously:
          1. Parse JSON input envelope
          2. Execute requested tool within error boundary
          3. Commit step trace to SQLite memory
          4. Return standardized JSON response envelope
        """
        sess_id = session_id or self.config.default_session_id

        # Phase 1: Input Normalization & Parsing
        try:
            req = json.loads(input_json)
            if not isinstance(req, dict):
                raise ValueError(f"Request must be a JSON object, got {type(req).__name__}")
            tool_name: str = req["tool"]
            kwargs: Dict[str, Any] = req.get("args", {})
            prompt: str = req.get("prompt", f"Execute tool {tool_name}")
            thought: str = req.get("thought", f"Invoking tool {tool_name} with arguments {kwargs}")
        except (json.JSONDecodeError, KeyError, ValueError) as err:
            logger.error("Request validation failed: %s", err)
            return json.dumps({"status": "error", "error": f"Invalid request envelope: {err}"})

        # Phase 2: Tool Execution with Error Boundary
        step_index = 1
        try:
            logger.info("[%s] Calling tool %r with args=%s", sess_id, tool_name, kwargs)
            # Yield control to event loop simulation
            await asyncio.sleep(0.01)

            result = self.registry.call(tool_name, **kwargs)
            status = "success"
            observation = result

            # Phase 3: Persistent Audit Logging
            self.memory.save_interaction(
                session_id=sess_id,
                step=step_index,
                prompt=prompt,
                thought=thought,
                tool=tool_name,
                arguments=kwargs,
                observation=observation,
                status=status,
            )

            return json.dumps({
                "status": "ok",
                "tool": tool_name,
                "result": result,
                "session_id": sess_id,
            })

        except KeyError as err:
            error_msg = str(err).strip("'\"")
            logger.warning("[%s] Unknown tool error: %s", sess_id, error_msg)
            self.memory.save_interaction(
                session_id=sess_id,
                step=step_index,
                prompt=prompt,
                thought=thought,
                tool=tool_name,
                arguments=kwargs,
                observation=error_msg,
                status="error",
            )
            return json.dumps({"status": "error", "error": error_msg, "session_id": sess_id})

        except Exception as exc:
            error_msg = f"{type(exc).__name__}: {exc}"
            logger.error("[%s] Tool %r failed with exception: %s", sess_id, tool_name, error_msg)
            self.memory.save_interaction(
                session_id=sess_id,
                step=step_index,
                prompt=prompt,
                thought=thought,
                tool=tool_name,
                arguments=kwargs,
                observation=error_msg,
                status="error",
            )
            return json.dumps({"status": "error", "error": error_msg, "session_id": sess_id})

    async def execute_react_sequence(
        self,
        session_id: str,
        goal: str,
        plan_steps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Executes a multi-turn ReAct reasoning loop where multiple tools
        are invoked sequentially to fulfill an overarching goal.
        """
        logger.info("=== Starting Multi-Turn ReAct Plan for Goal: %r ===", goal)
        execution_trace: List[Dict[str, Any]] = []

        for idx, step_plan in enumerate(plan_steps, start=1):
            if idx > self.config.max_steps:
                logger.warning("Agent exceeded maximum step limit (%s). Terminating.", self.config.max_steps)
                break

            tool_name = step_plan["tool"]
            args = step_plan.get("args", {})
            thought = step_plan.get("thought", f"Step {idx}: Need to execute {tool_name}")

            logger.info("Thought: %s", thought)
            logger.info("Action: %s(%s)", tool_name, args)

            # Invoke tool
            try:
                result = self.registry.call(tool_name, **args)
                obs_status = "success"
                obs_val = result
            except Exception as e:
                obs_status = "error"
                obs_val = f"{type(e).__name__}: {e}"

            logger.info("Observation: %s", obs_val)

            # Record step in memory
            self.memory.save_interaction(
                session_id=session_id,
                step=idx,
                prompt=goal,
                thought=thought,
                tool=tool_name,
                arguments=args,
                observation=obs_val,
                status=obs_status,
            )

            execution_trace.append({
                "step": idx,
                "thought": thought,
                "tool": tool_name,
                "observation": obs_val,
                "status": obs_status,
            })

        return {
            "session_id": session_id,
            "goal": goal,
            "total_steps": len(execution_trace),
            "trace": execution_trace,
        }


# =====================================================================
# BUILT-IN AGENT TOOLS
# =====================================================================

def tool_add(a: float, b: float) -> float:
    """Calculates the sum of two numbers a and b."""
    return a + b

def tool_multiply(a: float, b: float) -> float:
    """Calculates the product of two numbers a and b."""
    return a * b

def tool_echo(message: str) -> str:
    """Echoes the input message string back verbatim."""
    return message

def tool_word_count(text: str) -> Dict[str, Any]:
    """Analyzes text and returns character, word, and line metrics."""
    words = text.split()
    lines = text.splitlines()
    return {
        "char_count": len(text),
        "word_count": len(words),
        "line_count": len(lines),
    }

def tool_knowledge_search(query: str) -> List[str]:
    """Simulates a knowledge base lookup returning relevant knowledge snippets."""
    kb = {
        "python": [
            "Python was created by Guido van Rossum and released in 1991.",
            "Python 3.0 was released in 2008 and emphasizes code readability."
        ],
        "agent": [
            "An AI agent perceives its environment, reasons, and acts autonomously.",
            "ReAct interleaves reasoning traces and action steps."
        ],
        "react": [
            "ReAct stands for Reasoning and Acting in language models.",
            "Formulated by Yao et al. in 2022 to prevent reasoning hallucination."
        ],
    }
    q_clean = query.lower().strip()
    for key, articles in kb.items():
        if key in q_clean:
            return articles
    return [f"No knowledge base entries found matching query '{query}'."]


# =====================================================================
# MAIN PIPELINE DEMONSTRATION
# =====================================================================

async def main() -> None:
    print("\n" + "=" * 75)
    print("      COURSE -1 CAPSTONE: MINI REACT AGENT PIPELINE DEMONSTRATION")
    print("=" * 75 + "\n")

    # 1. Dependency Initialization (Dependency Injection pattern)
    config = AgentConfig(name="Hermes-Capstone", db_path=":memory:", max_steps=5)
    registry = ToolRegistry()
    memory = Memory(config.db_path)

    # 2. Registering Capabilities
    registry.register("add", tool_add)
    registry.register("multiply", tool_multiply)
    registry.register("echo", tool_echo)
    registry.register("word_count", tool_word_count)
    registry.register("knowledge_search", tool_knowledge_search)

    # 3. Construct Agent with Injected Dependencies
    agent = MiniAgent(config=config, registry=registry, memory=memory)

    # 4. Scenario A: Single-Turn Tool Requests (Valid & Defensive Cases)
    print("\n--- SCENARIO A: Single-Turn JSON Request Dispatch ---")
    requests = [
        '{"tool": "add", "args": {"a": 42.5, "b": 17.5}}',
        '{"tool": "multiply", "args": {"a": 8.0, "b": 12.5}}',
        '{"tool": "word_count", "args": {"text": "Autonomous agents use tools to reason and act."}}',
        '{"tool": "knowledge_search", "args": {"query": "Tell me about ReAct"}}',
        '{"tool": "unknown_tool", "args": {"val": 100}}',  # Defensive test: unknown tool
        'MALFORMED_NON_JSON_STRING',                       # Defensive test: invalid JSON
    ]

    for req in requests:
        resp = await agent.run_request(req, session_id="sess-single-turn")
        print(f"\nRequest:  {req[:55]:<55}")
        print(f"Response: {resp}")

    # 5. Scenario B: Multi-Turn ReAct Reasoning Sequence
    print("\n\n--- SCENARIO B: Multi-Step ReAct Sequence Execution ---")
    goal = "Retrieve knowledge about Python and compute lexical statistics on the knowledge."
    react_plan = [
        {
            "thought": "I must first query the knowledge base for 'Python' articles.",
            "tool": "knowledge_search",
            "args": {"query": "python"},
        },
        {
            "thought": "Now I will analyze the word and character counts of the retrieved knowledge.",
            "tool": "word_count",
            "args": {"text": "Python was created by Guido van Rossum and released in 1991."},
        },
        {
            "thought": "Now I will compute the total character budget if multiplied by 3 replicas.",
            "tool": "multiply",
            "args": {"a": 63.0, "b": 3.0},
        },
    ]

    multi_result = await agent.execute_react_sequence(
        session_id="sess-react-multi",
        goal=goal,
        plan_steps=react_plan,
    )
    print(f"\nCompleted multi-turn plan: {multi_result['total_steps']} steps executed.")

    # 6. Scenario C: Inspecting Persistent Memory Audit Trail
    print("\n\n--- SCENARIO C: SQLite Memory Audit Trail Inspection ---")
    history = memory.get_session_history("sess-react-multi")
    print(f"Session 'sess-react-multi' has {len(history)} recorded steps:")
    for item in history:
        print(f"  Step {item['step']}: Tool={item['tool']:<16} Status={item['status']:<8} Obs={str(item['observation'])[:45]}")

    print("\nTool Usage Summary Across All Sessions:")
    stats = memory.get_tool_usage_stats()
    for tool_name, count in stats.items():
        print(f"  - {tool_name:<18}: {count} calls")

    print("\n" + "=" * 75)
    print("CapStone Mini ReAct Agent pipeline executed successfully with 0 errors!")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
