# Topic: Context Managers and the `with` Statement

## What You Will Learn
In this module, you will master Python context managers and the `with` statement—the standard mechanism for deterministic resource acquisition, lifecycle management, and guaranteed teardown. You will learn:
- Why manual cleanup with `try/finally` is error-prone and how the `with` statement provides guaranteed execution.
- The two magic dunder methods forming the Context Manager Protocol: `__enter__()` and `__exit__()`.
- How the return value of `__enter__()` binds to the target variable in `with ... as target:`.
- How `__exit__()` receives exception diagnostics (`exc_type`, `exc_val`, `exc_tb`) and controls whether an exception is propagated or suppressed.
- How to transform standard generator functions into lightweight context managers using `@contextlib.contextmanager`.
- How to use standard library context utilities including `contextlib.suppress` and `contextlib.ExitStack`.
- How AI agents use context managers to establish sandbox environments, isolate scratch workspaces, manage database transactions, and handle secure API authentication sessions.

## Prerequisites
Before mastering context managers, you should be comfortable with:
- Exception handling using `try`, `except`, `finally`, and `raise` (Module 10).
- Working with file input/output and system paths (Module 11).
- Object-oriented programming: classes, instances, `self`, and dunder methods (Module 13).
- Generators and the `yield` keyword (Module 17).
- Function decorators (Module 19).

## The Problem
Software programs interact with scarce operating system resources: open file descriptors, network sockets, thread mutexes, database connections, and temporary directories.
Consider an AI agent processing a batch of user files:
```python
def process_agent_file(filename: str):
    f = open(filename, "w")
    data = fetch_agent_response()  # What if this raises an exception or times out?
    f.write(data)
    f.close()                      # NEVER REACHED IF AN ERROR OCCURS!
```
If `fetch_agent_response()` crashes, the file remains open. On Linux and macOS systems, an operating system process can only have a finite number of file descriptors open simultaneously (often 1,024). Once exhausted, every subsequent file read, network request, or socket connection will crash with `OSError: [Errno 24] Too many open files`.

Even worse, if a lock is acquired and never released because of an exception, your multi-threaded agent deadlocks indefinitely.
Writing `try...finally` blocks everywhere solves the leak, but produces repetitive, bloated code:
```python
f = open(filename, "w")
try:
    data = fetch_agent_response()
    f.write(data)
finally:
    f.close()
```
Context managers encapsulate this setup-and-teardown lifecycle into a reusable, declarative, and foolproof syntax.

## Key Terminology
- **Context Manager**: An object that controls runtime context for a code block by implementing `__enter__()` and `__exit__()`.
- **`with` Statement**: A compound Python statement that wraps execution of a block with methods defined by a context manager.
- **`__enter__()`**: The method executed before the `with` block begins. Its return value is bound to the identifier specified after `as`.
- **`__exit__()`**: The method executed after the `with` block finishes or exits due to an exception. It takes three arguments: `exc_type`, `exc_val`, and `exc_tb`.
- **Exception Suppression**: If `__exit__()` returns a truthy value (`True`), Python suppresses the active exception and continues execution immediately after the `with` block. If it returns `False` or `None`, any exception propagates upward.
- **`@contextlib.contextmanager`**: A decorator from the standard library that allows defining a context manager using a single generator function containing exactly one `yield`.
- **`contextlib.ExitStack`**: A dynamic context manager that allows managing a variable number of context managers programmatically.
- **Resource Acquisition Is Initialization (RAII)**: A software design pattern where resource allocation is tied directly to object lifetime and cleanup is guaranteed upon scope exit.

## Intuition
Imagine renting a secure workspace or a hotel room:
- **`__enter__()`**: You check in at the reception desk, receive a keycard (`as room`), and the hotel powers on the lights and air conditioning.
- **The `with` body**: You enter the room, conduct your meetings, write code, or sleep.
- **`__exit__()`**: When you leave the room—whether you finished your work peacefully or ran out because of a fire alarm (`exception`)—the hotel staff automatically inspects the room, locks the door, shuts off the power, and cleans the room.
- You never have to worry about accidentally leaving the lights on for three weeks. The teardown happens automatically the instant you leave the doorway.

## Concept
The runtime execution flow of a `with` block follows a strict invariant:
1. The context expression is evaluated to produce a context manager object `cm`.
2. `cm.__enter__()` is invoked.
3. If an `as target` clause is present, the return value of `__enter__()` is assigned to `target`.
4. The code block inside the `with` statement executes.
5. If the block finishes normally (without an exception), `cm.__exit__(None, None, None)` is called.
6. If an exception occurs inside the block:
   - Python captures the exception type, value, and traceback.
   - It calls `cm.__exit__(exc_type, exc_val, exc_tb)`.
   - If `__exit__()` returns `True`, the exception is swallowed.
   - If `__exit__()` returns `False` (or anything non-truthy), the exception is re-raised automatically.
7. Crucially, `__exit__()` is **always** executed, even if the block exits via `return`, `break`, `continue`, or an unhandled exception!

## Syntax
### 1. Class-Based Context Manager
```python
class DatabaseConnection:
    def __enter__(self):
        print("Connecting to database...")
        self.conn = "Active Connection Object"
        return self.conn  # Binds to target variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        # Returning False allows exceptions to bubble up
        return False

with DatabaseConnection() as conn:
    print(f"Executing query with {conn}")
```

### 2. Generator-Based Context Manager (`@contextlib.contextmanager`)
```python
import contextlib

@contextlib.contextmanager
def temporary_flag(obj, attribute, temp_value):
    original_value = getattr(obj, attribute)
    setattr(obj, attribute, temp_value)
    try:
        yield temp_value  # Target variable receives temp_value
    finally:
        setattr(obj, attribute, original_value)  # Guaranteed restoration
```

### 3. Suppressing Specific Exceptions
```python
import contextlib
import os

# Safely remove a file without crashing if it does not exist
with contextlib.suppress(FileNotFoundError):
    os.remove("non_existent_file.tmp")
```

## Example
Here is a complete, runnable example demonstrating a secure Agent Scratchpad Sandbox that sets up an isolated workspace directory, handles failures cleanly, and wipes the directory upon task completion:

```python
import os
import shutil
import tempfile
import time
from typing import Dict, Any

class AgentExecutionSandbox:
    """
    Guarantees an isolated filesystem sandbox for an AI agent's execution.
    Automatically creates a unique directory on entry and safely wipes it on exit.
    """
    def __init__(self, agent_id: str, auto_cleanup: bool = True):
        self.agent_id = agent_id
        self.auto_cleanup = auto_cleanup
        self.sandbox_path = None

    def __enter__(self) -> str:
        self.sandbox_path = tempfile.mkdtemp(prefix=f"agent_{self.agent_id}_")
        print(f"[SANDBOX ENTER] Created workspace for {self.agent_id}: {self.sandbox_path}")
        return self.sandbox_path

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            print(f"[SANDBOX ERROR] Agent execution failed with {exc_type.__name__}: {exc_val}")
        else:
            print(f"[SANDBOX SUCCESS] Agent task finished cleanly.")

        if self.auto_cleanup and self.sandbox_path and os.path.exists(self.sandbox_path):
            print(f"[SANDBOX TEARDOWN] Removing sandbox directory {self.sandbox_path}...")
            shutil.rmtree(self.sandbox_path)

        # Return False so any agent runtime exceptions still propagate to coordinator
        return False

# Demonstration of happy path:
with AgentExecutionSandbox(agent_id="coder_01") as workspace:
    test_file = os.path.join(workspace, "solution.py")
    with open(test_file, "w") as f:
        f.write("print('Hello from isolated sandbox!')")
    print(f"Workspace file created: {os.path.exists(test_file)}")

print(f"Workspace cleaned up: {not os.path.exists(workspace)}")
```

## Line-by-Line Explanation
Let's dissect the `AgentExecutionSandbox` execution flow:
1. `class AgentExecutionSandbox:`: Declares the class implementing the Context Manager Protocol.
2. `def __init__(self, agent_id: str, auto_cleanup: bool = True):`: Initializes configuration parameters without acquiring the system resource yet.
3. `def __enter__(self) -> str:`: Invoked when entering the `with` block.
4. `self.sandbox_path = tempfile.mkdtemp(...)`: Allocates the filesystem resource, ensuring a collision-free temporary folder.
5. `return self.sandbox_path`: Whatever is returned here is bound to `workspace` in `with AgentExecutionSandbox(...) as workspace:`.
6. `def __exit__(self, exc_type, exc_val, exc_tb) -> bool:`: Invoked when the `with` block terminates.
7. `if exc_type is not None:`: Inspects whether the block terminated cleanly or with an exception. If an exception occurred, `exc_type` holds the exception class (e.g., `ValueError`), `exc_val` holds the exception instance, and `exc_tb` holds the traceback object.
8. `shutil.rmtree(self.sandbox_path)`: Deletes the directory and all created files, guaranteeing that disk space is never leaked.
9. `return False`: Ensures that any exceptions raised inside the sandbox are not hidden from the caller, preserving observability.

## What Python Is Doing
At the interpreter level, Python transforms a `with` block into explicit exception handling:
```text
SETUP_WITH     label_cleanup
STORE_FAST     target
... body ...
POP_BLOCK
LOAD_CONST     None
... normal exit cleanup ...
label_cleanup:
WITH_EXCEPT_START
POP_JUMP_IF_TRUE label_suppressed
RERAISE
```
Here is the CPython virtual machine step-by-step logic:
1. CPython evaluates the expression, calls `type(mgr)->tp_descr_get` or `getattr(mgr, '__enter__')`, and invokes `__enter__()`.
2. The result is placed on the evaluation stack and assigned to the `as` variable if specified.
3. CPython establishes an exception-handling block on the internal stack frame (`PyFrameObject`).
4. When the body finishes normally:
   - CPython calls `__exit__(None, None, None)`.
5. When an unhandled exception occurs in the body:
   - CPython intercepts the exception before unwinding the stack.
   - It packages the exception into `(exc_type, exc_value, traceback)`.
   - It executes `__exit__(exc_type, exc_value, traceback)`.
   - If the return value is truthy (e.g. `True`), CPython clears the active exception (`PyErr_Clear()`) and continues execution normally after the `with` block.
   - If falsy (e.g. `False` or `None`), CPython re-raises the original exception (`RERAISE`).

## Common Mistakes
### 1. Accidentally Suppressing All Exceptions by Returning `True`
```python
class CarelessManager:
    def __enter__(self): return self
    def __exit__(self, *args):
        return True  # BUG: Swallows EVERY exception silently!

with CarelessManager():
    raise ZeroDivisionError("Crash!")
print("Carried on as if nothing happened!")  # Silent bug mask!
```
**Fix**: Only return `True` when you specifically intend to swallow known, recoverable exceptions. Otherwise, return `False` or `None`.

### 2. Forgetting to Yield in `@contextmanager`
A function decorated with `@contextlib.contextmanager` must contain exactly one `yield`. If it contains zero yields or multiple yields, Python raises `RuntimeError: generator didn't yield` or `RuntimeError: generator didn't stop`.

### 3. Omitting the `try/finally` Block in `@contextmanager`
If you write:
```python
@contextlib.contextmanager
def leaky():
    acquire()
    yield
    release() # BUG: If with-block raises an error, release() is NEVER called!
```
**Fix**: Always place `yield` inside a `try` block and teardown logic inside a `finally` block:
```python
@contextlib.contextmanager
def safe():
    acquire()
    try:
        yield
    finally:
        release()
```

### 4. Returning the Manager Object Instead of the Desired Resource
If `__enter__` returns `self` when the user expected a database connection or file handle, `with Manager() as m:` leaves `m` pointing to the wrapper rather than the target resource.

## Real-World Uses
- **File I/O (`open()`)**: Flushing write buffers and closing OS file handles.
- **Database Transactions (`sqlite3`, SQLAlchemy, Django ORM)**: Committing changes on success and rolling back transactions on failure.
- **Concurrency Locks (`threading.Lock`, `asyncio.Lock`)**: Acquiring mutex locks before critical sections and releasing them on exit.
- **Testing & Patching (`unittest.mock.patch`)**: Temporarily replacing functions or classes with mock objects during test runs.
- **Environment & Directory Switching**: Temporarily changing the current working directory (`os.chdir`) or masking environment variables during subprocess calls.

## Connection to AI Agents
In AI agent architectures, context managers provide vital safety rails:
- **Sandbox Workspace Isolation**: Generating ephemeral directories for untrusted code execution generated by LLMs, ensuring file artifacts are wiped cleanly after execution.
- **Database Transaction Integrity**: Recording agent thoughts, tool call inputs, and execution results in SQLite/PostgreSQL with automatic rollback if tool invocation crashes mid-operation.
- **Temporary Secret Masking**: Injecting API keys into environment variables only for the duration of an external API request, removing them immediately afterward to prevent leakage.
- **Async HTTP Clients (`httpx.AsyncClient`)**: Managing connection pools and keep-alive sockets across asynchronous LLM requests with `async with httpx.AsyncClient() as client:`.

## Practice
Put these principles into action with these practice tasks:
1. Write a context manager class `Timer` that records elapsed wall-clock time using `time.perf_counter()` and prints the elapsed duration upon exiting.
2. Modify `Timer` so that it stores the elapsed duration in an attribute `self.elapsed`, accessible via `with Timer() as t:`.
3. Use `@contextlib.contextmanager` to write a context manager `temporary_env_var(key, val)` that sets an environment variable and restores its original value on exit.
4. Experiment with returning `True` vs `False` in `__exit__` when an intentional exception is raised in the block.

## Challenge
Build an `AgentTransactionManager` context manager that coordinates an agent's memory update.
1. When entering, it creates a shallow copy of the agent's memory state dictionary.
2. During the `with` block, the agent can modify the working memory.
3. If an exception occurs, the transaction rolls back: changes are discarded and the original memory is preserved.
4. If the block completes successfully, the changes are committed to the primary memory store.
5. Provide both a class-based version and a generator-based version using `@contextlib.contextmanager`.

## Summary
- Context managers ensure deterministic setup and teardown of resources regardless of exceptions.
- The protocol consists of `__enter__()` (setup/acquire) and `__exit__()` (cleanup/release).
- The value returned by `__enter__()` is bound to the `as` variable.
- `__exit__()` receives exception info; returning `True` suppresses the exception, while returning `False` allows it to propagate.
- `@contextlib.contextmanager` turns any generator with a `try/yield/finally` structure into a context manager.
- AI agents rely on context managers for sandboxed code execution, transaction rollbacks, and secure API session management.

## What You Should Know Before Moving On
Before advancing to Module 21 (Testing), verify that you can:
- Write a class implementing `__enter__` and `__exit__` from scratch.
- Explain the significance of returning `True` vs `False` in `__exit__`.
- Implement a context manager using `@contextlib.contextmanager` with proper `try...yield...finally` structure.
- Explain why file descriptors and database connections must be managed with context managers rather than manual closes.
- Describe how an AI agent uses context managers to isolate execution workspaces and manage transaction rollbacks.
