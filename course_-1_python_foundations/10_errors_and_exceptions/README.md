# Errors and Exceptions in Python

## What You Will Learn
In this module, you will master Python's error handling and exception management system:
- The fundamental distinction between compile-time Syntax Errors and runtime Exceptions.
- The Python Exception Hierarchy and why catching `BaseException` or using bare `except:` is hazardous.
- How to structure robust `try`, `except`, `else`, and `finally` control blocks.
- How to catch multiple specific exceptions cleanly and avoid masking unintended failures.
- How to raise exceptions intentionally using `raise` to enforce contracts.
- How to perform explicit exception chaining using `raise ... from ...` and suppress noisy internal tracebacks with `from None`.
- How to create domain-specific custom exception classes with structured metadata.
- Python's core programming philosophy: **EAFP** ("Easier to Ask for Forgiveness than Permission") versus **LBYL** ("Look Before You Leap").
- How to programmatically inspect tracebacks, stack frames, and error origins using the `traceback` module.
- How autonomous AI agent systems use resilient exception pipelines to intercept tool execution crashes, parse malformed LLM outputs, implement exponential backoff retries, and return structured error diagnostics back into context windows for agent self-correction.

## Prerequisites
Before beginning this module, you should be comfortable with:
- Module 03: Variables, primitive data types, and dictionary lookups.
- Module 07: Control flow constructs (`if/elif/else`, `for`, `while`, `break`).
- Module 08: Defining functions, parameters, return statements, and docstrings.
- Module 09: Scope, variable lifetimes, and namespaces.

## The Problem
In software, the unexpected is guaranteed to occur:
- An API endpoint times out or returns HTTP 503 Service Unavailable.
- A user provides a file path that doesn't exist on disk, or a path where your program lacks read permissions.
- An LLM generates a JSON tool payload with a missing closing bracket or an invalid field name.
- A calculation attempts to divide by zero due to an uninitialized sensor reading.

In languages without structured exception handling (or in code where errors are ignored), unexpected conditions cause immediate, fatal process crashes. For an autonomous AI agent operating in production, an unhandled exception terminates the entire reasoning loop, dropping active user sessions, corrupting pending database transactions, and leaving resources open. 

Error handling provides the structured mechanism to detect anomalous runtime conditions, protect system invariants, gracefully recover or fallback, and ensure that critical resources (sockets, files, locks) are safely released under all circumstances.

## Key Terminology
- **Syntax Error (Parsing Error)**: An error detected by the Python parser before code execution begins, caused by invalid grammar (e.g., missing colons, unmatched parentheses).
- **Exception (Runtime Error)**: An anomalous event detected during execution that interrupts the normal flow of instructions (e.g., `ZeroDivisionError`, `KeyError`, `IndexError`).
- **Exception Hierarchy**: The object-oriented tree of Python exception classes rooted at `BaseException`, branching into `Exception`, `KeyboardInterrupt`, `SystemExit`, and specialized standard exceptions.
- **`try` Block**: A code block monitored by Python's runtime for raised exceptions.
- **`except` Block**: An exception handler block executed when a matching exception occurs in the preceding `try` block.
- **`else` Block**: An optional clause executed after the `try` block **only** if no exceptions were raised.
- **`finally` Block**: A cleanup clause guaranteed to execute before the `try/except` construct exits, regardless of whether exceptions were raised, handled, or unhandled.
- **Exception Chaining**: Preserving the original cause of an error when raising a new, higher-level domain exception using `raise NewException from original_error`.
- **EAFP (Easier to Ask for Forgiveness than Permission)**: The idiomatic Python design philosophy that assumes valid keys or operations and handles exceptions if they fail, rather than executing expensive upfront checks.
- **LBYL (Look Before You Leap)**: The defensive programming style that explicitly tests preconditions (e.g., `if key in dict:` or `if os.path.exists(path):`) before performing operations.
- **Traceback**: A formatted diagnostic report detailing the sequence of function calls and stack frames active at the exact moment an exception was raised.

## Intuition
Think of running a software program like launching a satellite into orbit:
- A **Syntax Error** is discovering during the rocket assembly phase that the booster fins were bolted on backwards. The rocket cannot even be rolled out to the launchpad; the mission aborts before the engine ignites.
- An **Exception** is encountering high-altitude wind shear during flight. The rocket is already flying. If the flight computer has an exception protocol (`try...except`), it adjusts the thrusters to compensate for the turbulence and continues to orbit.
- The **`try` block** is the turbulent maneuver.
- The **`except` block** is the emergency stabilization thruster protocol.
- The **`else` block** is the confirmation beacon transmitted only when the maneuver finishes with zero turbulence.
- The **`finally` block** is logging the telemetry and securing the fuel valves, which must occur whether the maneuver succeeded, stabilized, or failed.
- A **bare `except:`** or catching `BaseException` is disabling all alarms, including the flight crew pressing the Emergency Abort switch (`KeyboardInterrupt`), causing the rocket to blindly crash into the ocean.

## Concept

### 1. The Python Exception Tree
All exceptions in Python are instances of classes inheriting from `BaseException`. However, normal application code should only ever catch classes derived from `Exception`:

```
BaseException
├── SystemExit                     (Raised by sys.exit(); do NOT catch in app logic!)
├── KeyboardInterrupt              (Raised by Ctrl+C; do NOT catch in app logic!)
├── GeneratorExit                  (Raised when generators close)
└── Exception                      (Root of all non-system-exiting exceptions)
    ├── ArithmeticError
    │   ├── ZeroDivisionError      (1 / 0)
    │   └── OverflowError          (Math calculation too large)
    ├── LookupError
    │   ├── IndexError             (list[999] out of range)
    │   └── KeyError               (dict["missing_key"])
    ├── ValueError                 (int("invalid_text"))
    ├── TypeError                  ("text" + 5)
    ├── OSError
    │   ├── FileNotFoundError      (File does not exist on disk)
    │   └── PermissionError        (Insufficient OS privileges)
    └── RuntimeError
```

If you catch `Exception`, you catch application bugs and runtime errors, while allowing critical process interrupts like `KeyboardInterrupt` and `SystemExit` to pass through.

### 2. The Complete `try...except...else...finally` Lifecycle
Python's exception lifecycle has four distinct stages:
1. **`try`**: Python executes statements sequentially. If an exception occurs, execution immediately stops and jumps to the first matching `except` clause.
2. **`except ExceptionType as err`**: If the raised exception is an instance of `ExceptionType`, this block executes. You can bind the exception instance to a variable (`as err`) to inspect its message and arguments.
3. **`else`**: Runs **only** if the `try` block completed without raising any exceptions. This separates code that might raise an error from code that should run upon success, preventing accidental catching of errors in subsequent steps.
4. **`finally`**: Always executes before leaving the block, whether the `try` block succeeded, an `except` handled an error, or an unhandled exception is propagating up the call stack.

```
+-----------------------------------+
|             try block             |
+-----------------------------------+
       |                     |
   Exception              No Error
       v                     v
+-------------------+ +-------------------+
|   except block    | |    else block     |
+-------------------+ +-------------------+
       \                     /
        v                   v
+-----------------------------------+
|           finally block           |
|  (Always executes unconditionally)|
+-----------------------------------+
```

### 3. EAFP vs LBYL
- **LBYL (Look Before You Leap)**:
  ```python
  if key in mapping and isinstance(mapping[key], dict) and "score" in mapping[key]:
      score = mapping[key]["score"]
  ```
  Requires multiple key lookups and creates race conditions in concurrent systems (the key might be deleted between the `if` check and the access).
- **EAFP (Easier to Ask for Forgiveness than Permission)**:
  ```python
  try:
      score = mapping[key]["score"]
  except (KeyError, TypeError):
      score = default_score
  ```
  Faster when success is the common path, atomic, and idiomatic Python.

## Syntax

```python
# 1. Full 4-part Exception Handling
try:
    data = load_telemetry(sensor_id)
except (ConnectionError, TimeoutError) as net_err:
    log_warning(f"Network failure: {net_err}")
    data = fallback_telemetry()
except ValueError as val_err:
    log_error(f"Corrupt telemetry format: {val_err}")
    raise
else:
    update_dashboard(data)
finally:
    release_sensor_lock(sensor_id)

# 2. Raising Exceptions Intentionally
if step_budget <= 0:
    raise ValueError(f"step_budget must be positive, got {step_budget}")

# 3. Custom Exception Class with Metadata
class AgentExecutionError(Exception):
    """Raised when an autonomous agent fails a step."""
    def __init__(self, message: str, step_id: str, tool_name: str):
        super().__init__(message)
        self.step_id = step_id
        self.tool_name = tool_name

# 4. Explicit Exception Chaining
try:
    response = raw_http_call(url)
except OSError as raw_err:
    raise AgentExecutionError("Tool HTTP request failed", step_id="step_4", tool_name="web_search") from raw_err
```

## Example

```python
"""
Resilient AI Agent Tool Invocation Dispatcher with Structured Exceptions.
Demonstrates custom exception hierarchies, chaining, EAFP, and cleanup.
"""
import json
import time
from typing import Any, Callable, Dict, Optional


# Domain-specific exception hierarchy
class ToolError(Exception):
    """Base exception for all agent tool execution failures."""
    def __init__(self, message: str, tool_name: str, payload: Dict[str, Any]):
        super().__init__(message)
        self.tool_name = tool_name
        self.payload = payload


class ToolNotFoundError(ToolError):
    """Raised when the agent attempts to invoke an unregistered tool."""
    pass


class ToolValidationError(ToolError):
    """Raised when the tool parameters fail validation."""
    pass


class ToolExecutionTimeoutError(ToolError):
    """Raised when the tool takes longer than the allowed timeout."""
    pass


# Agent Tool Registry
REGISTRY: Dict[str, Callable[..., Any]] = {}


def register_tool(name: str) -> Callable:
    def decorator(fn: Callable) -> Callable:
        REGISTRY[name] = fn
        return fn
    return decorator


@register_tool("calculator")
def run_calculator(expression: str) -> float:
    # Safe calculator evaluating basic arithmetic
    allowed = set("0123456789+-*/. ()")
    if not all(c in allowed for c in expression):
        raise ValueError(f"Expression contains unauthorized characters: {expression}")
    return float(eval(expression, {"__builtins__": None}, {}))


def execute_agent_tool_call(raw_json_request: str) -> Dict[str, Any]:
    """
    Safely parses and executes an agent tool call request.
    Returns a structured dictionary suitable for returning to the LLM context.
    """
    start_time = time.perf_counter()
    tool_name = "unknown"
    args = {}

    try:
        # Phase 1: Parse JSON payload
        try:
            call_spec = json.loads(raw_json_request)
        except json.JSONDecodeError as json_err:
            raise ToolValidationError(
                f"Malformed JSON in tool call: {json_err.msg}",
                tool_name=tool_name,
                payload={"raw": raw_json_request}
            ) from json_err

        tool_name = call_spec.get("tool", "")
        args = call_spec.get("arguments", {})

        # Phase 2: Validate tool registration
        if tool_name not in REGISTRY:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' is not in the active agent tool registry.",
                tool_name=tool_name,
                payload=args
            )

        # Phase 3: Execute tool
        tool_fn = REGISTRY[tool_name]
        result = tool_fn(**args)

    except ToolError as tool_err:
        # Caught known agent domain error
        return {
            "status": "error",
            "error_type": type(tool_err).__name__,
            "message": str(tool_err),
            "tool_name": tool_err.tool_name,
            "recoverable": True,
        }
    except Exception as unexpected_err:
        # Caught unexpected lower-level crash
        return {
            "status": "fatal_error",
            "error_type": type(unexpected_err).__name__,
            "message": f"Unexpected crash during '{tool_name}': {unexpected_err}",
            "tool_name": tool_name,
            "recoverable": False,
        }
    else:
        # Success path
        return {
            "status": "success",
            "tool_name": tool_name,
            "result": result,
        }
    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000
        # Telemetry cleanup guaranteed to execute
        print(f"[Telemetry] Tool '{tool_name}' execution concluded in {duration_ms:.2f}ms")


# Run demonstrations
print("--- 1. Successful Tool Invocation ---")
r1 = execute_agent_tool_call('{"tool": "calculator", "arguments": {"expression": "(12 + 8) * 3"}}')
print(f"Result 1: {r1}\n")

print("--- 2. Unregistered Tool Request ---")
r2 = execute_agent_tool_call('{"tool": "database_search", "arguments": {"query": "SELECT *"}}')
print(f"Result 2: {r2}\n")

print("--- 3. Malformed JSON Request ---")
r3 = execute_agent_tool_call('{"tool": "calculator", "arguments": {expression: 10 + 5}')  # invalid JSON
print(f"Result 3: {r3}\n")
```

## Line-by-Line Explanation
1. `class ToolError(Exception):`: Declares a base custom exception subclassing `Exception`.
2. `def __init__(self, message: str, tool_name: str, payload: Dict[str, Any]):`: Custom constructor accepting error description plus metadata (`tool_name`, `payload`).
3. `super().__init__(message)`: Calls the parent `Exception` constructor so standard Python string formatting and traceback generation display the message correctly.
4. `class ToolNotFoundError(ToolError):`: Subclasses `ToolError`, allowing downstream callers to catch either specific errors or all tool errors polymorphically.
5. `def execute_agent_tool_call(raw_json_request: str) -> Dict[str, Any]:`: Main entry point providing a fault boundary.
6. `try: ... except json.JSONDecodeError as json_err:`: Catches the specific JSON parsing exception if the LLM provided malformed text.
7. `raise ToolValidationError(...) from json_err`: Explicitly chains the new `ToolValidationError` to the underlying `json_err`, keeping the original line/column location in `__cause__`.
8. `except ToolError as tool_err:`: Catches any custom exception in our domain hierarchy. Notice this comes **before** `except Exception:` so specific handlers run first.
9. `except Exception as unexpected_err:`: Catch-all safety net for unpredicted failures (e.g., divide by zero, type errors inside the tool).
10. `else:`: Executes only when no exceptions occurred, packaging the successful result.
11. `finally:`: Computes execution duration and logs telemetry, executing even if an exception was raised, handled, or re-raised.

## What Python Is Doing
Under the hood, Python manages exceptions using an internal exception stack and stack unwinding:
1. **Raising an Exception**: When `raise obj` is executed, Python verifies that `obj` is an instance of `BaseException`. It creates a traceback object (`PyTracebackObject`) capturing the current execution frame (`f_code`, `f_lineno`, `f_locals`).
2. **Stack Unwinding**: Python pauses the current instruction pointer and inspects the active frame's exception table.
   - If the current frame has a matching `except` block for the exception type, the instruction pointer jumps directly to that handler.
   - If no matching handler exists, the active frame is popped off the call stack, resources in local scopes are dereferenced, and Python inspects the caller's frame. This unwinding continues up the call chain.
   - If no frame handles the exception, Python terminates the thread and prints the traceback to `sys.stderr`.
3. **The `__cause__` and `__context__` Attributes**:
   - When you write `raise B from A`, Python sets `B.__cause__ = A` and `B.__suppress_context__ = True`.
   - If an exception occurs inside an `except` block without `from`, Python automatically attaches the prior error to `B.__context__ = A`. When printed, Python displays: *"During handling of the above exception, another exception occurred"*.

## Common Mistakes

### 1. The Catastrophic Bare `except:` or Catching `BaseException`
- **Bad**:
  ```python
  try:
      run_agent()
  except:  # Or except BaseException:
      pass
  ```
- **Why**: This intercepts `KeyboardInterrupt` (Ctrl+C) and `SystemExit` (`sys.exit()`). The program becomes an un-killable zombie process in your terminal or container orchestrator.
- **Fix**: Always catch `Exception` or specific subclasses: `except Exception as e:`.

### 2. Over-Broad Exception Catching Hiding Bugs
- **Bad**:
  ```python
  try:
      user_age = int(user_input["age"])
  except Exception:
      user_age = 0
  ```
- **Why**: If `user_input` had a typo in code (e.g. `user_inpt["age"]`), Python raises `NameError`. The catch-all absorbs the typo, setting age to 0, hiding a critical software bug.
- **Fix**: Catch only the expected exceptions: `except (KeyError, ValueError):`.

### 3. Returning Values Inside `finally`
- **Bad**:
  ```python
  def calculate():
      try:
          return 10 / 0  # Raises ZeroDivisionError
      finally:
          return 42      # Silently swallows the exception!
  ```
- **Why**: A `return`, `break`, or `continue` inside a `finally` block discards any active exception being propagated!
- **Fix**: Never return values or break loops inside `finally`. Use `finally` strictly for side-effect cleanups (closing files, releasing locks).

### 4. Forgetting `as e` When Re-Raising
- If you catch an exception and want to re-raise it after logging, simply write `raise` on its own. Do not write `raise e`, as `raise` alone preserves the original traceback line numbers without adding redundant frames.

## Real-World Uses
- **Network Resilience & Exponential Backoff**: Catching `requests.exceptions.RequestException` and sleeping with increasing delays (`2 ** attempt`) before retrying.
- **Database Transaction Rollback**:
  ```python
  try:
      db.execute(transfer_funds)
      db.commit()
  except DatabaseError:
      db.rollback()
      raise
  ```
- **Configuration Parsing**: Attempting to load user-customized YAML/JSON configuration files, falling back to sensible hardcoded defaults if `FileNotFoundError` occurs.
- **Graceful Shutdown**: Intercepting `KeyboardInterrupt` in CLI tools to flush write buffers, close database connections, and exit cleanly with code 0.

## Connection to AI Agents
Modern AI agents rely heavily on defensive exception architectures:
1. **Agent Self-Correction**: When an LLM generates invalid arguments for a tool, the agent runtime catches the `ValidationError` or `KeyError`, formats the error message into a user-role prompt (`"Tool execution failed with error: Key 'query' missing. Please correct your request."`), and feeds it back to the LLM. The agent reflects and produces a valid call on the next turn.
2. **Tool Sandboxing**: When agents run code in a Python REPL or bash shell, errors must be contained. The agent wraps tool execution in a `try...except Exception` harness, capturing stdout, stderr, and tracebacks so a crash in a student's script doesn't crash the agent server.
3. **API Rate Limit Handling**: LLM providers frequently return HTTP 429 "Too Many Requests". Autonomous pipelines catch `RateLimitError`, inspect the `retry-after` header, pause execution asynchronously, and resume automatically.

## Practice
1. Write a function `safe_divide(a: Any, b: Any) -> Optional[float]` that catches `ZeroDivisionError` and `TypeError`, returning `None` and printing a helpful message when errors occur.
2. Create a custom exception `NegativeBalanceError` that stores an account ID and current balance. Write a function that raises this exception when a withdrawal exceeds available funds.
3. Write a `try...except...else...finally` block that reads an integer from a string, squares it in the `else` block, and prints `"Conversion attempt finished"` in the `finally` block.

## Challenge
Implement a resilient API retry harness `execute_with_retry(fn: Callable[[], T], max_retries: int = 3, retryable_exceptions: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError)) -> T`:
- Executes callable `fn`.
- If an exception in `retryable_exceptions` occurs, increment the attempt counter, calculate a backoff delay, and retry.
- If an un-retryable exception (e.g. `ValueError`) occurs, fail immediately without retrying.
- If all retries are exhausted, raise a custom `MaxRetriesExceededError` that chains the last observed exception using `raise ... from last_error`.
- Ensure all attempts record attempt telemetry.

## Summary
- Syntax Errors occur at compile time due to invalid code structure; Exceptions occur at runtime during execution.
- Never catch `BaseException` or use bare `except:`; always catch `Exception` or specific subclasses.
- `try` monitors code; `except` handles specific errors; `else` runs only upon success; `finally` runs unconditionally.
- EAFP ("Easier to ask forgiveness") is Python's standard idiomatic style over verbose LBYL checks.
- Custom exceptions should inherit from `Exception` and include structured metadata for downstream diagnosis.
- Use `raise NewError from original_error` to preserve the causal chain in tracebacks.
- Never place `return` or `break` statements inside `finally` blocks.

## What You Should Know Before Moving On
Before advancing to Module 11 (Files and I/O), ensure you can:
- Construct multi-branch `try/except/else/finally` statements with exact control flow comprehension.
- Differentiate between exceptions that should be caught and those that should crash the program.
- Implement custom exception classes with extra fields and methods.
- Chain exceptions properly using `from` syntax.
- Write EAFP-style code that handles errors cleanly without crashing.
