"""
Module 10: Errors and Exceptions — Robust Execution and Resilient Failure Handling
==================================================================================

In software development and autonomous agent systems, things will go wrong:
network calls drop, files fail to open, user inputs fail validation, and LLMs
produce malformed outputs. Rather than letting unexpected conditions crash
your application, Python provides a powerful exception-handling architecture.

This comprehensive lesson covers:
  1. Syntax Errors vs Runtime Exceptions
  2. The Python Exception Hierarchy & Specific vs Broad Catching
  3. The Complete 4-Part Flow: try, except, else, and finally
  4. Raising Exceptions & Input Contract Enforcements
  5. Custom Domain Exception Hierarchies with Structured Metadata
  6. Exception Chaining (raise ... from ...) and Suppressed Context
  7. EAFP ("Easier to Ask for Forgiveness") vs LBYL ("Look Before You Leap")
  8. Programmatic Traceback Inspection using the traceback module
  9. Real-World AI Agent Pattern: Resilient Tool Execution with Retries & Fallbacks
"""

import json
import sys
import time
import traceback
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

print("=" * 75)
print("MODULE 10: ERRORS AND EXCEPTIONS IN PYTHON")
print("=" * 75)


# ==============================================================================
# SECTION 1: Syntax Errors vs. Runtime Exceptions
# ==============================================================================
print("\n--- 1. Syntax Errors vs. Runtime Exceptions ---")

# Syntax errors happen at COMPILE time when Python parses code.
# The code cannot even begin execution if there is a syntax error.
# Example: `if True print("missing colon")` -> SyntaxError

# Exceptions occur at RUNTIME when syntactically valid code encounters
# an impossible or illegal operation.
# We can intercept and handle runtime exceptions using try/except blocks:

def demonstrate_runtime_exception() -> None:
    print("  Attempting to divide 100 by 0...")
    try:
        result = 100 / 0
        print(f"  Result: {result}")
    except ZeroDivisionError as err:
        print(f"  [Handled] Caught ZeroDivisionError: {err}")
        print(f"  Exception type: {type(err).__name__}")

demonstrate_runtime_exception()


# ==============================================================================
# SECTION 2: The Exception Hierarchy and Catching Specific Exceptions
# ==============================================================================
print("\n--- 2. The Exception Hierarchy and Specific Exceptions ---")

# All standard exceptions derive from BaseException -> Exception.
# Catching specific exceptions prevents accidentally masking bugs:

def parse_agent_record(raw_record: Dict[str, Any], index: int) -> str:
    """Safely extracts a user summary from a raw dictionary record."""
    try:
        # Might raise KeyError if 'users' is missing
        user_list = raw_record["users"]
        # Might raise IndexError if index is out of range
        selected_user = user_list[index]
        # Might raise TypeError or KeyError
        name = selected_user["name"].strip()
        age = int(selected_user["age"])  # Might raise ValueError
        return f"User '{name}', Age {age}"
    except KeyError as key_err:
        return f"[KeyError] Missing required dictionary key: {key_err}"
    except IndexError as idx_err:
        return f"[IndexError] User position {index} does not exist: {idx_err}"
    except ValueError as val_err:
        return f"[ValueError] Age could not be converted to integer: {val_err}"
    except (TypeError, AttributeError) as type_err:
        # Grouping related exceptions into a single tuple
        return f"[TypeError] Record structure corrupted: {type_err}"

sample_database = {
    "users": [
        {"name": "Alice Agent", "age": "28"},
        {"name": "Bob Builder", "age": "not_an_int"},  # Triggers ValueError
        {"name": 42},                                   # Missing age, invalid name type
    ]
}

print("  Valid lookup:  ", parse_agent_record(sample_database, 0))
print("  ValueError:    ", parse_agent_record(sample_database, 1))
print("  Corrupt type:  ", parse_agent_record(sample_database, 2))
print("  IndexError:    ", parse_agent_record(sample_database, 99))
print("  Missing 'users':", parse_agent_record({}, 0))


# ==============================================================================
# SECTION 3: The Complete try...except...else...finally Lifecycle
# ==============================================================================
print("\n--- 3. The try...except...else...finally Lifecycle ---")

# The four clauses serve distinct roles:
#   try:     Monitors operations that might fail
#   except:  Executes only if an error occurs
#   else:    Executes only if NO error occurred in the try block
#   finally: ALWAYS executes, guaranteed cleanup

def simulate_database_query(query: str) -> Optional[str]:
    print(f"\n  [Query Start] Executing query: '{query}'")
    connection_open = True
    result: Optional[str] = None

    try:
        print("    [try] Opening database connection...")
        if "DROP" in query:
            raise PermissionError("Destructive operations are forbidden!")
        if "CORRUPT" in query:
            raise ValueError("Query syntax unrecognized by engine.")
        
        # Simulating successful query
        result = f"Query results for '{query}'"
    except PermissionError as perm_err:
        print(f"    [except] Security violation intercepted: {perm_err}")
    except ValueError as val_err:
        print(f"    [except] Query error intercepted: {val_err}")
    else:
        print("    [else] Query succeeded without errors! Processing rows...")
    finally:
        print("    [finally] Closing database connection lock and releasing buffer.")
        connection_open = False

    return result

simulate_database_query("SELECT name, role FROM agents WHERE active = 1")
simulate_database_query("DROP TABLE audit_logs")
simulate_database_query("CORRUPT SYNTAX ???")


# ==============================================================================
# SECTION 4: Raising Exceptions and Validating Invariants
# ==============================================================================
print("\n--- 4. Raising Exceptions for Defensive Programming ---")

def allocate_agent_memory(buffer_mb: int, session_id: str) -> Dict[str, Any]:
    """Allocates a memory buffer, raising descriptive exceptions on bad inputs."""
    if not isinstance(buffer_mb, int):
        raise TypeError(f"buffer_mb must be an integer, got {type(buffer_mb).__name__}")
    if buffer_mb <= 0:
        raise ValueError(f"buffer_mb must be positive, got {buffer_mb}")
    if buffer_mb > 1024:
        raise ValueError(f"Requested buffer {buffer_mb}MB exceeds maximum limit of 1024MB")
    if not session_id or not session_id.strip():
        raise ValueError("session_id cannot be empty or whitespace")

    return {"session_id": session_id, "allocated_mb": buffer_mb, "status": "active"}

try:
    allocate_agent_memory(-10, "sess_123")
except ValueError as err:
    print(f"  Caught expected invariant check: {err}")

try:
    allocate_agent_memory(2048, "sess_123")
except ValueError as err:
    print(f"  Caught memory limit check: {err}")


# ==============================================================================
# SECTION 5: Custom Domain Exceptions
# ==============================================================================
print("\n--- 5. Custom Domain Exception Hierarchies ---")

# In production applications, create dedicated exception hierarchies that inherit
# from Exception. This lets callers catch high-level domain errors cleanly.

class AgentError(Exception):
    """Base exception for all agent subsystem errors."""
    def __init__(self, message: str, agent_id: str):
        super().__init__(message)
        self.agent_id = agent_id
        self.timestamp = time.time()


class RateLimitExceededError(AgentError):
    """Raised when an agent makes too many requests to an external API."""
    def __init__(self, message: str, agent_id: str, retry_after_sec: float):
        super().__init__(message, agent_id)
        self.retry_after_sec = retry_after_sec


class ToolExecutionError(AgentError):
    """Raised when an individual tool fails during agent task execution."""
    def __init__(self, message: str, agent_id: str, tool_name: str, exit_code: int):
        super().__init__(message, agent_id)
        self.tool_name = tool_name
        self.exit_code = exit_code

def invoke_search_tool(query: str, agent_id: str) -> str:
    if len(query) < 3:
        raise ToolExecutionError("Search query too short", agent_id, tool_name="search", exit_code=1)
    if "rate_limit" in query:
        raise RateLimitExceededError("Google Search API quota exhausted", agent_id, retry_after_sec=5.0)
    return f"Found 3 results for '{query}'"

for q in ["a", "rate_limit_test", "python tutorials"]:
    try:
        res = invoke_search_tool(q, agent_id="agent_alpha_01")
        print(f"  [Success] {res}")
    except RateLimitExceededError as rle:
        print(f"  [RateLimit] Agent {rle.agent_id} must wait {rle.retry_after_sec}s: {rle}")
    except ToolExecutionError as tee:
        print(f"  [ToolError] Tool '{tee.tool_name}' failed with code {tee.exit_code}: {tee}")
    except AgentError as ae:
        print(f"  [GeneralAgentError] Fallback handler: {ae}")


# ==============================================================================
# SECTION 6: Exception Chaining (raise ... from ...)
# ==============================================================================
print("\n--- 6. Exception Chaining and Suppressed Context ---")

# When translating low-level system errors into high-level domain errors,
# use `from` to link them so the original root cause is preserved.

class ConfigurationLoadError(Exception):
    """Raised when application configuration fails to parse."""
    pass

def load_agent_config_chained(config_json: str) -> Dict[str, Any]:
    try:
        return json.loads(config_json)
    except json.JSONDecodeError as decode_err:
        # Preserves decode_err in the __cause__ attribute
        raise ConfigurationLoadError(f"Failed to parse config string: {decode_err.msg}") from decode_err

try:
    load_agent_config_chained("{invalid_json: true}")
except ConfigurationLoadError as cle:
    print(f"  Caught domain exception: {cle}")
    print(f"  Original underlying cause (__cause__): {type(cle.__cause__).__name__} -> {cle.__cause__}")


# ==============================================================================
# SECTION 7: EAFP vs LBYL
# ==============================================================================
print("\n--- 7. EAFP vs LBYL Paradigms ---")

# LBYL: Look Before You Leap (Defensive manual checks)
def get_user_score_lbyl(data: Dict[str, Any], user_id: str) -> int:
    if "users" in data and isinstance(data["users"], dict):
        if user_id in data["users"]:
            user_data = data["users"][user_id]
            if isinstance(user_data, dict) and "score" in user_data:
                return user_data["score"]
    return 0

# EAFP: Easier to Ask for Forgiveness than Permission (Idiomatic Python)
def get_user_score_eafp(data: Dict[str, Any], user_id: str) -> int:
    try:
        return data["users"][user_id]["score"]
    except (KeyError, TypeError):
        return 0

test_data = {"users": {"u1": {"score": 95}}}
print(f"  LBYL score result: {get_user_score_lbyl(test_data, 'u1')}")
print(f"  EAFP score result: {get_user_score_eafp(test_data, 'u1')}")
print(f"  EAFP missing user: {get_user_score_eafp(test_data, 'nonexistent')}")


# ==============================================================================
# SECTION 8: Programmatic Traceback Inspection
# ==============================================================================
print("\n--- 8. Programmatic Traceback Inspection ---")

def deep_nested_failure() -> None:
    raise RuntimeError("Deep calculation pipeline crashed!")

def intermediate_caller() -> None:
    deep_nested_failure()

try:
    intermediate_caller()
except RuntimeError as run_err:
    # Format the traceback into a clean diagnostic string
    tb_lines = traceback.format_exception(type(run_err), run_err, run_err.__traceback__)
    print("  Captured Traceback Summary:")
    for line in tb_lines[-3:]:  # Print last 3 lines
        print(f"    | {line.strip()}")


# ==============================================================================
# SECTION 9: AI Agent Pattern: Resilient Tool Executor with Retries
# ==============================================================================
print("\n--- 9. Resilient AI Agent Tool Executor with Backoff ---")

def execute_with_resilience(
    task_name: str,
    operation: Callable[[], Any],
    max_retries: int = 3,
    initial_delay: float = 0.05
) -> Dict[str, Any]:
    """
    Executes a potentially flaky agent tool operation with exponential backoff.
    Captures unexpected crashes and returns structured telemetry.
    """
    attempts = 0
    delay = initial_delay

    while attempts < max_retries:
        attempts += 1
        try:
            print(f"  [Attempt {attempts}/{max_retries}] Executing '{task_name}'...")
            result = operation()
            return {
                "status": "success",
                "task": task_name,
                "attempts": attempts,
                "result": result
            }
        except (ConnectionError, TimeoutError) as transient_err:
            print(f"    Transient error ({transient_err}). Waiting {delay:.2f}s before retry...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except Exception as unrecoverable_err:
            # Fatal error that cannot be resolved by retrying
            print(f"    Unrecoverable failure: {unrecoverable_err}")
            return {
                "status": "fatal_error",
                "task": task_name,
                "attempts": attempts,
                "error": str(unrecoverable_err)
            }

    return {
        "status": "exhausted_retries",
        "task": task_name,
        "attempts": attempts,
        "error": f"Failed after {max_retries} attempts"
    }

# Demonstration with a simulated transient network tool
counter = 0
def flaky_api_call() -> str:
    global counter
    counter += 1
    if counter < 3:
        raise ConnectionError(f"HTTP 503 Service Unavailable (attempt {counter})")
    return "API response: {'status': 200, 'data': 'Agent Plan Validated'}"

res = execute_with_resilience("verify_agent_plan", flaky_api_call, max_retries=4)
print(f"  Resilience result: {res}")

print("\n" + "=" * 75)
print("MODULE 10 COMPLETE: ALL LESSON DEMONSTRATIONS EXECUTED CLEANLY")
print("=" * 75)
