# Topic: Integrated Projects — The Mini ReAct Agent Pipeline Capstone

Welcome to the capstone milestone of Course -1: Python Foundations. In this module, everything you have learned across the preceding 32 modules converges into a unified, functioning software architecture: an autonomous, tool-using **Mini ReAct (Reasoning + Acting) Agent Pipeline**.

You are no longer writing isolated snippets, small utility functions, or disconnected loops. You are now engineering a production-grade system that integrates dataclasses, object-oriented design, dynamic tool registries, asynchronous event loops, SQLite database persistence, structured JSON communication, defensive exception handling, and diagnostic logging.

This capstone forms the conceptual and architectural bridge directly into **Course 0: Prerequisites for AI Agent Engineering**.

---

## What You Will Learn

- **End-to-End System Synthesis**: How all 32 fundamental modules (data structures, OOP, async, JSON, SQLite, architecture, debugging) assemble into a cohesive system.
- **The ReAct Agent Pattern**: The industry-standard loop of **Thought → Action → Observation → Response** first formalized by Yao et al. (2022).
- **The Tool Registry Architecture**: Building a decoupled, introspectable registry that allows agents to discover, validate, and execute tools dynamically.
- **Persistent Agent Memory**: Using SQLite to record an immutable, auditable log of user requests, intermediate thoughts, tool calls, and observations.
- **Asynchronous Agent Orchestration**: Executing I/O-bound tool invocations asynchronously without blocking the central execution loop.
- **Defensive Error Boundaries**: Ensuring malformed inputs, failing tools, or missing parameters produce structured diagnostic observations rather than crashing the agent.

---

## Prerequisites

Before tackling this capstone, you should have mastered the core concepts from across the curriculum:
- **Dataclasses & Types**: `@dataclass`, default values, type hints (Modules 15 & 16).
- **Classes, OOP & Interfaces**: Encapsulation, constructors, instance methods, and Dependency Injection (Modules 13 & 30).
- **Asynchronous Python**: Coroutines, `async def`, `await`, and `asyncio.run()` (Modules 24 & 25).
- **Serialization & Data Storage**: `json.dumps()` / `loads()`, and `sqlite3` schemas, transactions, and queries (Modules 26 & 29).
- **Logging & Debugging**: Structured logging levels, exception traceback inspection, and diagnostic error payloads (Modules 22 & 32).

---

## The Problem

Beginners frequently conceptualize AI agents as magical "black boxes" consisting of a single prompt sent to an LLM API. But in real-world engineering, an LLM by itself cannot read a database, execute a Python script, query an API, or remember past interactions across restarts.

Without a robust, well-architected execution harness:
1. **Tool execution is fragile**: If an external calculation or API throws an exception, the entire agent crashes.
2. **State is ephemeral**: When the Python script exits, all conversation history, tool outputs, and reasoning steps evaporate.
3. **Components are tightly coupled**: Changing the database schema or adding a new math tool requires rewriting the core agent loop.
4. **Operations are synchronous**: Waiting for one slow tool stalls the entire application.

To build intelligent systems that interact with external environments reliably, you must engineer a robust pipeline that surrounds the reasoning model with modular, safe, and persistent infrastructure.

---

## Key Terminology

- **ReAct (Reason + Act)**: A prompting and execution paradigm where an agent alternates between generating verbal reasoning traces ("Thoughts") and operational tool invocations ("Actions"), receiving environmental feedback ("Observations").
- **Agent Pipeline**: The end-to-end software pipeline that receives raw user input, routes it through reasoning and tool dispatch, persists execution state, and returns formatted responses.
- **Tool Registry**: A centralized registry holding callable tools along with their metadata, parameter schemas, and execution handlers.
- **Memory Store**: A persistence backend (such as SQLite) that stores dialogue sessions, interaction records, and tool execution logs.
- **Execution Step**: A single turn within an agent loop comprising one Thought, one Action (or Final Answer), and one Observation.
- **Dependency Injection (DI)**: Passing the ToolRegistry, Memory, and Config into the Agent constructor from the outside, ensuring each component can be independently tested and swapped.

---

## Intuition

Think of an autonomous agent like a skilled human investigator solving a complex case:
- **The Case File (`AgentConfig`)**: Contains the investigator's name, credentials, and constraints (e.g., maximum budget, deadline).
- **The Toolkit (`ToolRegistry`)**: The investigator's briefcase containing specialized instruments: a calculator, a fingerprint magnifier, a search phone, and a notebook. Each tool has a clear label and manual.
- **The Evidence Locker (`Memory / SQLite`)**: Every clue discovered, interview conducted, and calculation performed is stamped with a timestamp and filed permanently in the evidence locker.
- **The Reasoning Cycle (`ReAct Loop`)**:
  - *Thought*: "The user wants to know the combined revenue of our two European branches in USD."
  - *Action*: "I will pull the Euro totals using branch_search, then convert to USD using currency_convert."
  - *Observation*: "Branch A = 120,000 EUR, Branch B = 80,000 EUR; Conversion rate = 1.08."
  - *Thought*: "Now I must sum 120,000 + 80,000 = 200,000, then multiply by 1.08."
  - *Action*: "calculator(200000 * 1.08)"
  - *Observation*: "216,000."
  - *Final Answer*: "The combined revenue is $216,000 USD."

---

## Concept

The Mini ReAct Agent pipeline is architected around four decoupled components governed by Dependency Injection:

```text
               ┌────────────────────────────────────────────────────────┐
               │                     USER REQUEST                       │
               │               (JSON string or CLI prompt)              │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AGENT CORE (Agent)                                       │
│  - Receives request                                                                      │
│  - Orchestrates reasoning loop                                                           │
│  - Delegates tool calls to Registry                                                      │
│  - Commits audit logs to Memory                                                          │
└──────────────┬───────────────────────────┬───────────────────────────────┬───────────────┘
               │                           │                               │
               ▼                           ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────┐ ┌─────────────────────────────────┐
│        CONFIGURATION        │ │    TOOL REGISTRY    │ │             MEMORY              │
│       (AgentConfig)         │ │   (ToolRegistry)    │ │            (Memory)             │
│                             │ │                     │ │                                 │
│ - Agent Name                │ │ - math_eval         │ │ - SQLite table: interactions    │
│ - Max Iterations            │ │ - string_reverse    │ │ - Session history queries       │
│ - Database Path             │ │ - search_kb         │ │ - Audit trail persistence       │
└─────────────────────────────┘ └─────────────────────┘ └─────────────────────────────────┘
```

### The ReAct Execution Lifecycle
1. **Input Normalization**: Parse raw JSON or text into a typed request.
2. **Dispatch & Guardrails**: Look up the requested tool in the `ToolRegistry`. Validate parameter types and check against iteration limits.
3. **Execution & Isolation**: Execute the tool callable inside an asynchronous `try...except` boundary. If an error occurs, catch it and convert it into a structured error observation.
4. **Persistence**: Record the input, tool name, arguments, observation, and status into the SQLite `interactions` table.
5. **Output Delivery**: Return a standardized JSON response envelope containing status, result, and execution metadata.

---

## Syntax

### 1. Agent Configuration Dataclass
```python
@dataclass
class AgentConfig:
    name: str = "MiniReAct"
    max_steps: int = 5
    db_path: str = ":memory:"
    verbose: bool = True
```

### 2. Registering Tools with Type Metadata
```python
def calculator(expression: str) -> float:
    """Evaluates basic mathematical expressions."""
    ...

registry = ToolRegistry()
registry.register("calculator", calculator)
```

### 3. Asynchronous Agent Pipeline Invocation
```python
agent = Agent(config=config, registry=registry, memory=memory)
response_json = await agent.run('{"tool": "calculator", "args": {"expression": "25 * 4"}}')
```

---

## Example

Below is a complete architectural snapshot demonstrating how the components interact:

```python
import asyncio
import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Callable, Dict

@dataclass
class AgentConfig:
    name: str = "Hermes-Lite"
    db_path: str = ":memory:"

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        self._tools[name] = func

    def execute(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name](**kwargs)

class Memory:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, tool TEXT, result TEXT)"
        )
        self.conn.commit()

    def record(self, tool: str, result: Any) -> None:
        self.conn.execute("INSERT INTO logs (tool, result) VALUES (?, ?)", (tool, str(result)))
        self.conn.commit()

class Agent:
    def __init__(self, config: AgentConfig, registry: ToolRegistry, memory: Memory) -> None:
        self.config = config
        self.registry = registry
        self.memory = memory

    async def handle_request(self, raw_json: str) -> str:
        try:
            req = json.loads(raw_json)
            tool_name = req["tool"]
            args = req.get("args", {})
            result = self.registry.execute(tool_name, **args)
            self.memory.record(tool_name, result)
            return json.dumps({"status": "ok", "result": result})
        except Exception as exc:
            return json.dumps({"status": "error", "message": str(exc)})

async def main() -> None:
    config = AgentConfig()
    registry = ToolRegistry()
    registry.register("add", lambda a, b: a + b)
    memory = Memory(config.db_path)

    agent = Agent(config, registry, memory)
    response = await agent.handle_request('{"tool": "add", "args": {"a": 12, "b": 30}}')
    print("Agent Response:", response)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Line-by-Line Explanation

- `@dataclass class AgentConfig:`: Encapsulates agent configuration options in a clean, typed container with default values.
- `class ToolRegistry:`: Implements the Registry pattern, maintaining an internal mapping of tool names to callable objects.
- `def register(self, name: str, func: Callable) -> None:`: Adds a callable to the registry, decoupling tool authoring from the agent's core loop.
- `class Memory:`: Encapsulates database storage, managing SQLite connections, table migrations, and SQL queries cleanly behind methods.
- `class Agent:`: Represents the orchestrator. Notice that `Agent.__init__` receives its dependencies (`config`, `registry`, `memory`) as parameters—this is **Dependency Injection**.
- `async def handle_request(self, raw_json: str) -> str:`: Defines an asynchronous coroutine capable of handling requests non-blockingly.
- `req = json.loads(raw_json)`: Deserializes the incoming JSON string into native Python dictionaries.
- `self.memory.record(tool_name, result)`: Writes the result of the tool call to persistent SQLite storage before returning.

---

## What Python Is Doing

1. **Dependency Wiring**: In the `main()` function, Python constructs each object (`AgentConfig`, `ToolRegistry`, `Memory`) in memory. The `Agent` instance stores references to these objects in its `self` dictionary, sharing the single active database connection.
2. **Coroutines and the Event Loop**: When `asyncio.run(main())` is called, Python initializes the asyncio event loop thread. Calling `await agent.handle_request(...)` registers the coroutine as an active task on the event loop, allowing asynchronous suspension if any sub-tasks perform async I/O.
3. **Exception Propagation & Boundaries**: If `self.registry.execute()` fails (e.g. unknown tool or invalid math), Python creates an exception object and begins stack unwinding. The `try...except Exception as exc:` block intercepts the unwinding *before* it leaves the agent, converting the exception into a structured JSON string response.
4. **SQLite Serialization**: Python's `sqlite3` driver converts Python strings and tuples into binary SQLite protocol buffers, writes them to the designated database file or memory space, and enforces ACID transaction guarantees via `commit()`.

---

## Common Mistakes

### 1. Hardcoding Database Connections Inside the Agent
```python
# ANTI-PATTERN: Impossible to mock or test in isolation
class BadAgent:
    def __init__(self):
        self.db = sqlite3.connect("production.db")  # Hardcoded dependency!
```
*Correction*: Inject the database or `Memory` instance into `__init__`.

### 2. Forgetting to Commit SQLite Transactions
Calling `cursor.execute("INSERT ...")` without calling `connection.commit()` means that written records remain in uncommitted memory buffers and are permanently discarded when the program terminates.

### 3. Unbounded Tool Execution
Allowing an agent to loop infinitely when calling tools. Always enforce a `max_steps` or `max_iterations` counter to terminate runaway execution.

### 4. Raw Unsanitized Eval
Using Python's built-in `eval()` to execute mathematical tool inputs without sandboxing or mathematical expression parsing exposes the host system to arbitrary code execution vulnerabilities.

---

## Real-World Uses

- **Enterprise AI Workflows**: Frameworks like LangChain, LlamaIndex, AutoGen, and Semantic Kernel are built upon this exact architecture: a central orchestrator delegating to tool registries, persisting to relational/vector databases, and maintaining session state.
- **Autonomous Customer Assistants**: Processing customer orders, querying CRM databases, issuing refunds, and sending confirmation emails via registered microservices.
- **Automated Data Science Pipelines**: Agents that iteratively fetch datasets, clean missing rows, train baseline models, evaluate F1 scores, and persist results to experiment-tracking databases.

---

## Connection to AI Agents

This module is the culmination of Python foundations and the direct blueprint for AI Agent engineering:
- **LLM Function Calling**: In Course 0 and production OpenAI/Anthropic APIs, the LLM outputs a JSON payload specifying which tool to invoke and what arguments to supply. The `ToolRegistry` and `Agent` you build here are the exact components that parse and execute those function calls.
- **ReAct Observability**: Multi-turn agents rely on state history. The SQLite `Memory` engine provides the context window memory that allows an agent to reflect upon past observations and decide what action to take next.
- **Sandboxed Tool Execution**: Robust agent systems encapsulate external tools within defensive error boundaries so that unexpected API failures are treated as informative observations rather than fatal crashes.

---

## Practice

1. **Add a String Reversal Tool**: Write a function `reverse_text(text: str) -> str` and register it in the `ToolRegistry`. Test invoking it through the agent.
2. **Add a Timestamp to Memory**: Alter the SQLite `logs` table in `Memory` to include a `timestamp DATETIME DEFAULT CURRENT_TIMESTAMP` column and verify that records are correctly ordered by time.
3. **Session Querying**: Write a method `get_recent_logs(limit: int = 5)` on the `Memory` class that returns the most recent interactions in reverse chronological order.

---

## Challenge

Build an **Autonomous Multi-Step ReAct Solver**:
- Register three tools:
  - `fetch_dataset(name: str) -> list[int]`: Returns a list of numbers.
  - `calculate_mean(numbers: list[int]) -> float`: Calculates arithmetic average.
  - `calculate_variance(numbers: list[int], mean: float) -> float`: Calculates variance.
- Implement an agent reasoning loop that takes a complex query: `"Analyze dataset sales"`.
- The agent must:
  1. Step 1: Call `fetch_dataset` to obtain the numbers.
  2. Step 2: Feed the numbers into `calculate_mean`.
  3. Step 3: Feed both numbers and mean into `calculate_variance`.
  4. Step 4: Persist all 3 intermediate steps into SQLite memory.
  5. Step 5: Deliver a final formatted summary string: `"Mean: X, Variance: Y"`.

---

## Summary

- The Mini ReAct Agent pipeline demonstrates the synthesis of object-oriented architecture, functional callables, asynchronous concurrency, JSON protocols, and relational database persistence.
- The **Tool Registry** decouples the agent's core reasoning engine from specific tool implementations.
- The **Memory** layer provides an immutable, auditable log of all agent actions and observations using SQLite.
- The **ReAct loop** alternates between reasoning steps and action steps, enabling multi-step problem solving.
- You are now fully prepared to enter Course 0: Prerequisites for AI Agent Engineering.

---

## What You Should Know Before Moving On

- How to assemble classes, dataclasses, callables, and persistence into a coherent architecture.
- How the ReAct paradigm structures agent thoughts, actions, and observations.
- How to implement the Registry pattern with typed functions and error handling.
- How to persist and query structured interaction histories using SQLite.
- How asynchronous agent workflows execute non-blocking operations cleanly.
