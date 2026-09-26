"""
Module 20: Context Managers and the with Statement
==================================================

This lesson explores Python's Context Manager Protocol, the mechanics of
resource lifecycle management, and how the `with` statement guarantees
safe acquisition and cleanup of resources.

Topics covered:
  1. The Resource Management Problem: Manual try/finally vs `with`
  2. The Context Manager Protocol: __enter__ and __exit__
  3. Stateful Context Managers: Execution Timer with Bound Variable
  4. Exception Handling and Suppression in __exit__
  5. Lightweight Context Managers with `@contextlib.contextmanager`
  6. Standard Library Helpers: `contextlib.suppress` and `redirect_stdout`
  7. AI Agent Case Study: Sandboxed Workspace Manager with Rollback
"""

import contextlib
import io
import os
import shutil
import tempfile
import time
from typing import Any, Dict, List, Optional


# =====================================================================
# 1. The Resource Management Problem: Manual try/finally vs `with`
# =====================================================================
print("=" * 70)
print("1. RESOURCE MANAGEMENT: MANUAL try/finally VS `with`")
print("=" * 70)

# Without context managers, managing resources like files or network handles
# requires verbose, error-prone try/finally blocks.

temp_file_path = "temp_scratchpad.txt"

# Old / manual pattern:
file_handle = open(temp_file_path, "w", encoding="utf-8")
try:
    file_handle.write("Simulated telemetry log data\n")
    print(f"  [Manual File IO] Wrote data to {temp_file_path}")
finally:
    file_handle.close()
    print("  [Manual File IO] File handle closed in finally block.")

# Modern Python: The `with` statement guarantees cleanup automatically:
with open(temp_file_path, "a", encoding="utf-8") as f:
    f.write("Second telemetry entry\n")
    print(f"  [with Statement] Successfully appended. File closed? {f.closed}")

print(f"  [with Statement Exit] Outside `with` block: File closed? {f.closed}")

# Clean up temporary scratchpad file
if os.path.exists(temp_file_path):
    os.remove(temp_file_path)


# =====================================================================
# 2. The Context Manager Protocol: __enter__ and __exit__
# =====================================================================
print("\n" + "=" * 70)
print("2. THE CONTEXT MANAGER PROTOCOL: __enter__ AND __exit__")
print("=" * 70)

class SimpleResource:
    """
    Demonstrates the exact lifecycle of __enter__ and __exit__.
    """
    def __init__(self, resource_name: str):
        self.name = resource_name

    def __enter__(self) -> str:
        print(f"  >>> [__enter__] Acquiring resource '{self.name}'...")
        # The return value of __enter__ is what gets bound to the 'as' variable
        return f"ACTIVE_CONNECTION_TO_{self.name.upper()}"

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print(f"  <<< [__exit__] Releasing resource '{self.name}'...")
        if exc_type is not None:
            print(f"      Encountered exception during execution: {exc_type.__name__}: {exc_val}")
        else:
            print("      Execution completed cleanly without exceptions.")
        # Return False to ensure any exception propagates normally
        return False

print("Running with SimpleResource:")
with SimpleResource("AgentVectorDatabase") as connection:
    print(f"    Inside with-block using: {connection}")


# =====================================================================
# 3. Stateful Context Managers: Execution Timer with Bound Variable
# =====================================================================
print("\n" + "=" * 70)
print("3. STATEFUL CONTEXT MANAGERS: EXECUTION TIMER")
print("=" * 70)

class ExecutionTimer:
    """
    Measures elapsed time for a block of code and stores the duration
    in an accessible attribute on the manager object.
    """
    def __init__(self, label: str):
        self.label = label
        self.start_time: float = 0.0
        self.elapsed_ms: float = 0.0

    def __enter__(self) -> "ExecutionTimer":
        self.start_time = time.perf_counter()
        print(f"  [Timer '{self.label}'] Started timing...")
        # Returning self allows caller to inspect properties inside and after block
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.elapsed_ms = (time.perf_counter() - self.start_time) * 1000
        print(f"  [Timer '{self.label}'] Completed in {self.elapsed_ms:.2f}ms")
        return False

with ExecutionTimer("Simulated Model Inference") as timer:
    # Simulate work
    total = sum(i * i for i in range(200_000))
    print(f"    Computed sum of squares: {total}")

# Notice that the timer object and its recorded duration persist after the block!
print(f"  Recorded elapsed duration outside block: {timer.elapsed_ms:.2f}ms")


# =====================================================================
# 4. Exception Handling and Suppression in __exit__
# =====================================================================
print("\n" + "=" * 70)
print("4. EXCEPTION HANDLING AND SUPPRESSION IN __exit__")
print("=" * 70)

class ExceptionHandlerContext:
    """
    Demonstrates controlling exception propagation:
    - If caught exception matches target_exc, suppress it by returning True.
    - Otherwise, return False to let it propagate.
    """
    def __init__(self, catch_type: type):
        self.catch_type = catch_type
        self.exception_caught = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None and issubclass(exc_type, self.catch_type):
            print(f"  [Suppression] Caught and suppressed expected exception: {exc_val}")
            self.exception_caught = True
            # Returning True instructs Python to swallow the exception!
            return True
        # Returning False allows unhandled exceptions to crash / propagate
        return False

print("Scenario A: Suppressing expected ZeroDivisionError:")
with ExceptionHandlerContext(ZeroDivisionError):
    print("    About to divide by zero...")
    result = 10 / 0
    print("    This line will never be reached.")

print("    Program continued normally after suppressed division error!")


# =====================================================================
# 5. Lightweight Context Managers with `@contextlib.contextmanager`
# =====================================================================
print("\n" + "=" * 70)
print("5. LIGHTWEIGHT CONTEXT MANAGERS WITH `@contextlib.contextmanager`")
print("=" * 70)

@contextlib.contextmanager
def temporary_config_override(config: Dict[str, Any], key: str, temp_value: Any):
    """
    Temporarily overrides a configuration key, guaranteeing restoration
    of the original value even if an error occurs.
    """
    original_value = config.get(key)
    print(f"  [ConfigManager] Setting config['{key}'] = '{temp_value}' (was: '{original_value}')")
    config[key] = temp_value
    try:
        # Everything up to yield is __enter__
        yield temp_value
        # If the with block finishes without exception, execution resumes here
    finally:
        # Everything in finally is __exit__ (guaranteed to execute)
        if original_value is not None:
            config[key] = original_value
        else:
            config.pop(key, None)
        print(f"  [ConfigManager] Restored config['{key}'] to '{original_value}'")

agent_settings = {"model": "gpt-4o", "temperature": 0.2}
print(f"Initial settings: {agent_settings}")

with temporary_config_override(agent_settings, "temperature", 0.9):
    print(f"    Inside with-block: Active temperature is {agent_settings['temperature']}")

print(f"Final settings after exit: {agent_settings}")


# =====================================================================
# 6. Standard Library Helpers: `contextlib.suppress` & `redirect_stdout`
# =====================================================================
print("\n" + "=" * 70)
print("6. STANDARD LIBRARY CONTEXT HELPERS")
print("=" * 70)

# contextlib.suppress: elegant one-line exception ignoring
with contextlib.suppress(KeyError):
    empty_dict = {}
    val = empty_dict["missing_agent_action"]
print("  contextlib.suppress(KeyError) executed cleanly.")

# contextlib.redirect_stdout: capture print statements into an in-memory buffer
captured_buffer = io.StringIO()
with contextlib.redirect_stdout(captured_buffer):
    print("Agent thought: Analyzing AST structure of target code.")
    print("Agent thought: Preparing modification chunk.")

captured_text = captured_buffer.getvalue()
print(f"  Captured printed thoughts:\n{captured_text.strip()}")


# =====================================================================
# 7. AI Agent Case Study: Sandboxed Workspace Manager with Rollback
# =====================================================================
print("\n" + "=" * 70)
print("7. AI AGENT CASE STUDY: SANDBOXED WORKSPACE & TRANSACTION ROLLBACK")
print("=" * 70)

class AgentWorkspaceSandbox:
    """
    Creates an isolated filesystem sandbox directory for an AI agent's code
    generation task. Automatically deletes the sandbox upon task completion.
    If an error occurs, records the failure reason before teardown.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.workspace_dir: Optional[str] = None

    def __enter__(self) -> str:
        self.workspace_dir = tempfile.mkdtemp(prefix=f"agent_ws_{self.agent_name}_")
        print(f"  [SANDBOX INIT] Workspace created at: {self.workspace_dir}")
        return self.workspace_dir

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            print(f"  [SANDBOX TEARDOWN] Agent crashed ({exc_val}). Performing rollback...")
        else:
            print("  [SANDBOX TEARDOWN] Agent task completed successfully.")

        if self.workspace_dir and os.path.exists(self.workspace_dir):
            shutil.rmtree(self.workspace_dir)
            print(f"  [SANDBOX TEARDOWN] Wiped workspace {self.workspace_dir}")

        # Let exceptions bubble up to supervisor
        return False

# Demonstrate agent creating code in sandbox
with AgentWorkspaceSandbox("coder_agent_4") as ws_path:
    code_path = os.path.join(ws_path, "generated_script.py")
    with open(code_path, "w", encoding="utf-8") as script_file:
        script_file.write("print('Hello from generated script')")
    print(f"    Created generated script inside sandbox: {os.path.exists(code_path)}")

print(f"  Workspace deleted on exit? {not os.path.exists(ws_path)}")

print("\n" + "=" * 70)
print("Module 20 lesson completed successfully!")
print("=" * 70)
