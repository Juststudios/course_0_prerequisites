# Topic: Python Logging and Observability

## What You Will Learn
In this module, you will master Python's built-in `logging` subsystem—the industry standard for telemetry, diagnostic recording, and observability in production systems. You will learn:
- Why `print()` statements are dangerous and insufficient for production software.
- The 5 standard severity levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.
- The core architectural components of the logging ecosystem: **Loggers**, **Handlers**, **Formatters**, and **Filters**.
- How logger hierarchies and propagation work using dot-delimited names (`agent.planner`, `agent.tools.calculator`).
- How to record unhandled exceptions and full stack traces using `logger.exception()`.
- How to write logs simultaneously to the console (stdout) and persistent disk files (`FileHandler`).
- How to implement structured JSON logging to feed cloud monitoring pipelines (Datadog, ELK, CloudWatch).
- How AI agent systems use structured logs to record multi-turn reasoning traces, tool execution parameters, token budgets, and safety guardrail triggers.

## Prerequisites
Before mastering logging, you should be comfortable with:
- Defining functions, modules, and variable scopes (Modules 08, 09, 12).
- Exception handling with `try/except` blocks (Module 10).
- File operations and path manipulation (Module 11).
- Object-oriented classes, inheritance, and string representation (Module 13).
- Context managers for resource safety (Module 20).

## The Problem
When developers first build an application, they rely on `print()` for debugging:
```python
def run_agent_task(prompt):
    print("Starting agent task...")
    print(f"DEBUG: prompt length is {len(prompt)}")
    response = call_llm(prompt)
    print("Got response from LLM")
    return response
```
While `print()` works for trivial 10-line scripts, it creates catastrophic problems in real-world systems:
1. **No Severity Filtering**: You cannot selectively turn off noisy debug prints in production while keeping critical error notices. All prints dump directly to standard output.
2. **No Destination Routing**: You cannot easily route warnings to a security alert channel, errors to a disk log file, and debug statements to a developer console.
3. **No Metadata Context**: `print()` output lacks timestamps, process IDs, thread names, module names, and source code line numbers unless manually formatted every single time.
4. **Silent Traceback Loss**: When an unexpected exception occurs inside a try/except block, `print(e)` only outputs a single-line message (e.g. `'connection reset'`), throwing away the vital stack trace needed to debug where the crash happened.
5. **Machine Parsing Failure**: In cloud environments with thousands of microservices, automated log aggregators cannot parse arbitrary unstructured text prints.

The Python `logging` module solves all of these problems through a decoupled, configurable architecture.

## Key Terminology
- **Logger**: The primary application interface object (`logging.getLogger(name)`). It exposes methods (`debug()`, `info()`, etc.) and determines if a log record should be processed based on its threshold level.
- **LogRecord**: A data object created automatically by a Logger whenever a message is logged. Contains all diagnostic metadata (timestamp, file path, line number, exception info).
- **Handler**: An engine that dispatches LogRecords to a specific output destination (console terminal, disk file, rotating archive, HTTP socket).
- **Formatter**: Specifies the final textual layout and structure of a LogRecord (e.g., standard human-readable text or structured JSON).
- **Filter**: Provides fine-grained contextual logic to decide whether a particular LogRecord should be emitted by a Logger or Handler.
- **Severity Level**: An integer threshold that classifies the urgency of a message (`DEBUG=10`, `INFO=20`, `WARNING=30`, `ERROR=40`, `CRITICAL=50`).
- **Propagation**: The mechanism by which a child logger passes LogRecords upward to its parent loggers in the naming hierarchy.
- **`logger.exception()`**: A convenience method that logs a message with `ERROR` level and automatically attaches the current exception's traceback (`exc_info=True`).

## Intuition
Think of a large hospital or airport control tower:
- **`print()`** is like a megaphone in the middle of the lobby. Anyone shouting anything creates overwhelming noise, wakes up patients, and cannot be categorized.
- **The Logging System** is a professional central dispatch radio network:
  - Different staff members carry radios tuned to specific channels (**Loggers**: `triage.er`, `flight.runway`).
  - Every message has a priority code (**Severity Level**: Code Green for `INFO`, Code Blue for `CRITICAL`).
  - Routine shift updates (**DEBUG**) only play on the technician's earpiece (**Console Handler**).
  - Emergency alerts (**ERROR**) trigger sirens, flash red lights, and get permanently recorded in the incident black box (**File Handler**).
  - Dispatch recorders format every transmission with precise UTC time, operator badge ID, and GPS coordinates (**Formatter**).

## Concept
The logging workflow follows a pipeline architecture:
```text
Application Code
      │ (logger.info("message"))
      ▼
   Logger ─── (Level Check: record.level >= logger.level?)
      │ Yes
      ▼
  LogRecord Created
      │
      ├───────────────────────────────┐
      ▼                               ▼
  Handler 1 (Console)             Handler 2 (File)
(Level Check >= INFO)           (Level Check >= ERROR)
      │                               │
  Formatter 1 (Color Text)        Formatter 2 (JSON)
      │                               │
      ▼                               ▼
 Terminal Screen                 /var/log/agent.log
```

### The 5 Standard Logging Levels
| Level | Numeric Value | When to Use |
|---|---|---|
| `DEBUG` | 10 | Granular diagnostic information useful during development (token counts, raw network payloads, variable dumps). |
| `INFO` | 20 | Normal operational events confirming system progress (agent initialized, tool loaded, task finished). |
| `WARNING` | 30 | Unexpected occurrence or edge case that does not stop execution (deprecated API used, retry triggered, high memory usage). |
| `ERROR` | 40 | A serious failure preventing a specific operation from completing (API call timed out, file write failed). |
| `CRITICAL` | 50 | A fatal system-level crash that halts the entire program (database corrupted, out of memory, safety guardrail breach). |

## Syntax
### 1. Basic Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
)

logger = logging.getLogger("agent")
logger.info("Agent subsystem started.")
```

### 2. Creating Dedicated Named Loggers with Handlers
```python
import logging

# Always use __name__ to match module hierarchy
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
```

### 3. Capturing Exception Tracebacks
```python
try:
    10 / 0
except ZeroDivisionError:
    # exc_info=True attaches full traceback automatically!
    logger.exception("Mathematical operation failed during reasoning step.")
```

### 4. Lazy String Formatting (Performance Best Practice)
Do not construct strings eagerly with f-strings in debug logs:
```python
# BAD (wastes CPU constructing string even if DEBUG is disabled):
logger.debug(f"Expensive calculation: {expensive_function()}")

# GOOD (lazy formatting, only evaluated if DEBUG is enabled):
logger.debug("Calculation value: %s", result)
```

## Example
The following complete runnable script sets up a multi-destination logging architecture for an AI Agent system, streaming colored human logs to standard output and structured logs to an in-memory buffer:

```python
import io
import json
import logging
import sys
import time

# 1. Custom Structured JSON Formatter
class AgentJsonFormatter(logging.Formatter):
    """Formats LogRecord objects into single-line JSON strings."""
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
        # Include custom extra fields if provided
        if hasattr(record, "agent_id"):
            log_payload["agent_id"] = record.agent_id
        if hasattr(record, "token_count"):
            log_payload["token_count"] = record.token_count
        return json.dumps(log_payload)


# 2. Setup Agent Logger
logger = logging.getLogger("ai_agent.runtime")
logger.setLevel(logging.DEBUG)
logger.propagate = False  # Avoid duplicate printing to root logger

# Handler A: Standard Console Output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_fmt = logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)s -> %(message)s")
console_handler.setFormatter(console_fmt)
logger.addHandler(console_handler)

# Handler B: In-Memory JSON Stream (simulating file or cloud shipper)
json_stream = io.StringIO()
json_handler = logging.StreamHandler(json_stream)
json_handler.setLevel(logging.DEBUG)
json_handler.setFormatter(AgentJsonFormatter())
logger.addHandler(json_handler)


# 3. Emitting Logs with Extra Context
logger.info("Agent booted successfully", extra={"agent_id": "planner_01"})
logger.debug("Prompt token count evaluated", extra={"agent_id": "planner_01", "token_count": 512})

try:
    raise ConnectionTimeoutError("LLM API endpoint did not respond within 10s")
except Exception:
    logger.exception("Failed to execute LLM step", extra={"agent_id": "planner_01"})


# 4. Inspecting Structured Output
print("\n--- Structured JSON Log Output (from stream) ---")
print(json_stream.getvalue().strip())
```

## Line-by-Line Explanation
Let's analyze how the dual-handler logging architecture operates:
1. `class AgentJsonFormatter(logging.Formatter):`: Subclasses standard `logging.Formatter` to produce machine-readable JSON logs for cloud aggregation.
2. `def format(self, record: logging.LogRecord) -> str:`: Overrides the core formatting method. It extracts attributes directly from the `record` object (such as `record.levelname`, `record.name`, and `record.lineno`).
3. `record.exc_info`: If an exception was active when logging, `self.formatException(record.exc_info)` serializes the full multi-line stack trace into a JSON string property.
4. `logger = logging.getLogger("ai_agent.runtime")`: Creates a named logger in the hierarchical namespace.
5. `logger.propagate = False`: Stops records from bubbling up to the root logger, preventing double-logging when root handlers exist.
6. `console_handler.setLevel(logging.INFO)`: Restricts console output to `INFO` and higher, filtering out verbose `DEBUG` messages.
7. `json_handler.setLevel(logging.DEBUG)`: Allows the JSON collector to record all `DEBUG` messages for forensic replay.
8. `extra={"agent_id": "planner_01"}`: Injects custom attributes into the `LogRecord`, accessible inside custom formatters.

## What Python Is Doing
At the internal module level:
1. **Logger Registry (`logging.Logger.manager`)**:
   `logging.getLogger(name)` checks a global singleton `Manager` dictionary. If a logger named `"ai_agent.runtime"` exists, it is returned immediately. If not, it is created.
2. **Hierarchy Navigation**:
   The `Manager` parses dot notation. The parent of `"ai_agent.runtime"` is `"ai_agent"`, and the parent of `"ai_agent"` is the root logger `""`.
3. **Dispatch Evaluation (`logger.handle`)**:
   When `logger.info(msg)` is called:
   - Python checks `logger.isEnabledFor(logging.INFO)`. If the logger's effective level is higher than 20, the call returns immediately without creating a record.
   - Otherwise, `logger.makeRecord(...)` instantiates a `LogRecord`.
   - The record passes through each attached `Handler`.
   - If `logger.propagate` is `True`, the record ascends to each ancestor logger, invoking their handlers until reaching the root.

## Common Mistakes
### 1. Calling `logging.basicConfig()` Multiple Times
`logging.basicConfig()` only works the very first time it is invoked. Subsequent calls are silently ignored unless `force=True` is provided (Python 3.8+).
```python
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)  # SILENTLY IGNORED!
```

### 2. Adding Handlers Inside Reusable Functions (Duplicate Logs)
If you configure and add a handler inside a function called multiple times, a new handler is appended on every call:
```python
def process():
    logger = logging.getLogger("worker")
    logger.addHandler(logging.StreamHandler())  # BUG: Duplicates output on each run!
    logger.info("Done")
```
**Fix**: Configure handlers once at application startup or module load.

### 3. Using `print(e)` Instead of `logger.exception()`
Logging only `str(e)` discards the stack trace, making debugging hard in production. Always use `logger.exception()` inside `except` blocks.

### 4. Naming Conflicts (`logging.py`)
Naming a local file `logging.py` shadows the Python standard library module, causing `AttributeError: module 'logging' has no attribute 'getLogger'`.

## Real-World Uses
- **Distributed Microservices**: Tracing requests across microservices using correlated `request_id` or `trace_id` headers.
- **Audit Trails & Security Compliance**: Recording administrative actions, authentication attempts, and data exports.
- **Performance Profiling**: Logging endpoint latencies and database query durations.
- **Automated Incident Response**: PagerDuty and Sentry integrations that alert on-call engineers when `CRITICAL` or `ERROR` logs appear.

## Connection to AI Agents
Observability is the lifeblood of reliable autonomous AI systems:
- **Reasoning Traces**: Recording the chain of thoughts, scratchpad reflections, and candidate actions at `DEBUG` level for prompt evaluation.
- **Tool Invocations**: Logging tool arguments, exit codes, and response lengths at `INFO` level.
- **Token & Cost Auditing**: Recording exact token usage (`prompt_tokens`, `completion_tokens`) and estimated costs per turn.
- **Safety & Guardrail Logging**: Logging when content moderation filters or sandboxing policies intercept unsafe outputs at `WARNING` or `ERROR` level.

## Practice
Solidify your logging knowledge with these practical tasks:
1. Configure `logging.basicConfig` to output timestamps and log levels, then emit messages across all 5 levels.
2. Create two distinct loggers: `"agent.planner"` and `"agent.executor"`. Set different logging levels on them.
3. Write a function that triggers a `KeyError` inside a `try/except` and log it using `logger.exception()`.
4. Add a `FileHandler` that writes logs to a file `agent.log` and verify that log messages appear in the file.

## Challenge
Build an `AgentObservabilityEngine`:
1. Create a logger hierarchy: root agent `"agent"` and child loggers `"agent.perception"`, `"agent.reasoning"`, `"agent.tools"`.
2. Configure a `StreamHandler` that outputs concise terminal messages for `INFO` and above.
3. Configure a custom structured Formatter that outputs JSON records with timestamps, logger names, latency in milliseconds, and token counts.
4. Simulate an agent task lifecycle (perceive, plan, execute tool, handle error) and verify that all messages route to their designated destinations without duplicate prints.

## Summary
- `print()` is for quick scratchpad exploration; `logging` is for robust production software.
- The 5 standard levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) allow dynamic filtering.
- Loggers create records, Handlers send them to destinations, and Formatters style them.
- Hierarchical dot-notation (`agent.tools`) enables modular configuration and propagation.
- `logger.exception()` automatically captures complete stack traces during errors.
- Modern AI systems rely on structured logging for prompt tracing, token cost accounting, and security audits.

## What You Should Know Before Moving On
Before advancing to Milestone M5 (Virtual Environments and Systems), verify that you can:
- List all 5 logging levels and their integer ordering.
- Configure a logger with custom formatting and appropriate handlers.
- Use `logger.exception()` to capture full stack traces in error handlers.
- Explain why propagation causes duplicate logs if handlers are attached at multiple levels.
- Describe how AI agents utilize structured logging for telemetry and runtime auditing.
