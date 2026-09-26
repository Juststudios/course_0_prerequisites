"""
Module 32: Python Debugging and Diagnostic Engineering
======================================================

A comprehensive, progressive guide to debugging Python applications,
understanding call stacks and tracebacks, transitioning from print statements
to structured logging, and building automated error diagnostics for AI agents.

Contents:
  1. Anatomy of a Python Traceback & Stack Frames
  2. Chained Exceptions & Root Cause Preservation
  3. Print Debugging vs. Structured Diagnostic Logging
  4. Frame Introspection & Runtime State Inspection
  5. The Scientific Debugging Workflow: A Complete Case Study
  6. Autonomous Error Telemetry for AI Agent Tooling
"""

import inspect
import io
import json
import logging
import sys
import time
import traceback
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple


# =====================================================================
# SECTION 1: ANATOMY OF A PYTHON TRACEBACK & STACK FRAMES
# =====================================================================
# When an exception is raised and not immediately handled, Python unwinds
# the call stack. Each active function call is represented by a Frame.
#
# Tracebacks print in chronological order:
#   - TOP: Entry point (oldest caller)
#   - MIDDLE: Intermediate function calls
#   - BOTTOM: The exact line that failed, plus the exception type & message!

def level_c(data_map: Dict[str, Any], key: str) -> Any:
    """Innermost function where the error occurs."""
    # This line will raise KeyError if key is missing
    return data_map[key]

def level_b(data_map: Dict[str, Any], key: str) -> Any:
    """Intermediate function propagating call."""
    return level_c(data_map, key)

def level_a(data_map: Dict[str, Any], key: str) -> Any:
    """Outermost caller in the application."""
    return level_b(data_map, key)

def demonstrate_traceback_anatomy() -> None:
    print("\n" + "=" * 70)
    print("SECTION 1: ANATOMY OF A PYTHON TRACEBACK")
    print("=" * 70)

    sample_dict = {"name": "Hermes-Agent", "status": "active"}

    try:
        level_a(sample_dict, "missing_config_key")
    except KeyError as exc:
        print("\n1. Caught unhandled KeyError during call stack unwinding.")
        print(f"   Exception Type:    {type(exc).__name__}")
        print(f"   Exception Message: {exc}")

        # Programmatically inspect the traceback using Python's traceback module
        exc_type, exc_value, exc_tb = sys.exc_info()
        assert exc_tb is not None

        # Extract structured frame summaries
        frames: List[traceback.FrameSummary] = traceback.extract_tb(exc_tb)

        print(f"\n2. Call Stack Depth: {len(frames)} frames unwound.")
        for idx, frame in enumerate(frames):
            print(f"   [Frame {idx + 1}] File: {frame.filename.split('/')[-1]}")
            print(f"            Function: {frame.name}()")
            print(f"            Line {frame.lineno}: {frame.line}")

        innermost_frame = frames[-1]
        print(f"\n3. Root Cause Frame Identified:")
        print(f"   Function: '{innermost_frame.name}' on line {innermost_frame.lineno}")
        print(f"   Code line: '{innermost_frame.line}'")


# =====================================================================
# SECTION 2: CHAINED EXCEPTIONS & ROOT CAUSE PRESERVATION
# =====================================================================
# When building high-level libraries or agents, low-level technical errors
# (e.g. JSONDecodeError, FileNotFoundError) should be converted into clear
# domain exceptions (e.g. AgentConfigError) while preserving the original cause.
#
# Python 3 provides: raise NewException(...) from original_exception

class AgentToolError(Exception):
    """Domain exception raised when an agent tool fails."""
    pass

def execute_raw_calculation(formula: str) -> float:
    """Parses and calculates a formula string, vulnerable to ZeroDivisionError."""
    if "/" in formula:
        parts = formula.split("/")
        num, denom = float(parts[0].strip()), float(parts[1].strip())
        return num / denom
    return float(formula)

def safe_tool_runner(formula_str: str) -> float:
    """Wraps low-level arithmetic in a domain exception with explicit chaining."""
    try:
        return execute_raw_calculation(formula_str)
    except ZeroDivisionError as err:
        # Explicit exception chaining connects original error via __cause__
        raise AgentToolError(f"Calculation failed for formula '{formula_str}'") from err

def demonstrate_chained_exceptions() -> None:
    print("\n" + "=" * 70)
    print("SECTION 2: CHAINED EXCEPTIONS & ROOT CAUSE PRESERVATION")
    print("=" * 70)

    try:
        safe_tool_runner("100 / 0")
    except AgentToolError as domain_err:
        print("\n1. Caught High-Level Domain Exception:")
        print(f"   Error: {domain_err}")

        # Check explicit root cause
        root_cause = domain_err.__cause__
        print(f"\n2. Inspected Explicit Root Cause (__cause__):")
        print(f"   Root Type: {type(root_cause).__name__}")
        print(f"   Root Message: {root_cause}")

        # Format full chained traceback
        formatted_chain = "".join(traceback.format_exception(
            type(domain_err), domain_err, domain_err.__traceback__
        ))
        print("\n3. Formatted Chained Traceback Preview:")
        for line in formatted_chain.splitlines()[-6:]:
            print(f"   | {line}")


# =====================================================================
# SECTION 3: PRINT DEBUGGING VS. STRUCTURED DIAGNOSTIC LOGGING
# =====================================================================
# Beginners use print() for debugging. While convenient for 10-line scripts,
# print debugging fails in production systems because:
#   - Prints lack timestamps, severity levels, and module origins.
#   - Prints cannot be redirected to log files or filtered by log level.
#   - Prints pollute standard output, breaking JSON or CLI piping.

def demonstrate_structured_logging() -> None:
    print("\n" + "=" * 70)
    print("SECTION 3: PRINT DEBUGGING VS STRUCTURED DIAGNOSTIC LOGGING")
    print("=" * 70)

    # Configure a dedicated in-memory logger for diagnostic demonstrations
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)-8s] [%(name)s:%(funcName)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger("diagnostic_demo")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    # Simulate an agent workflow with structured diagnostic telemetry
    logger.debug("Initializing agent memory store with SQLite backend.")
    logger.info("Agent received user prompt: 'Calculate annual revenue growth'.")

    try:
        payload = {"base_revenue": 50000.0, "current_revenue": "corrupted_string"}
        logger.debug("Validating input payload keys and types.")
        growth = (payload["current_revenue"] - payload["base_revenue"]) / payload["base_revenue"]  # type: ignore
        logger.info("Calculation completed: %s", growth)
    except TypeError:
        # logger.exception automatically appends full traceback details to ERROR logs!
        logger.exception("Type mismatch detected while calculating revenue growth.")

    # Display captured structured logs
    print("Captured Structured Log Output:")
    for log_line in log_stream.getvalue().strip().splitlines():
        print(f"   {log_line}")


# =====================================================================
# SECTION 4: FRAME INTROSPECTION & RUNTIME STATE INSPECTION
# =====================================================================
# When a bug occurs only in deep nested calls, you can inspect the active
# frame, local variables, and caller stack using Python's inspect module.

def compute_nested_ratio(dividend: float, divisor: float, metadata: Dict[str, Any]) -> float:
    """Demonstrates inspecting frame locals dynamically."""
    # Obtain current stack frame
    current_frame = inspect.currentframe()
    if current_frame is not None:
        local_vars = current_frame.f_locals
        # We can inspect exact variable values inside the function
        assert "dividend" in local_vars and "divisor" in local_vars

    if divisor == 0:
        # Instead of crashing silently or guessing, inspect caller
        caller_frame = inspect.stack()[1]
        caller_name = caller_frame.function
        caller_line = caller_frame.lineno
        raise ValueError(f"Invalid zero divisor passed by caller '{caller_name}' at line {caller_line}")

    return dividend / divisor

def demonstrate_frame_introspection() -> None:
    print("\n" + "=" * 70)
    print("SECTION 4: FRAME INTROSPECTION & RUNTIME STATE INSPECTION")
    print("=" * 70)

    meta = {"request_id": "req-9823", "client": "analytics_bot"}
    try:
        compute_nested_ratio(150.0, 0.0, meta)
    except ValueError as err:
        print(f"\n1. Frame inspection captured caller context successfully:")
        print(f"   {err}")


# =====================================================================
# SECTION 5: THE SCIENTIFIC DEBUGGING WORKFLOW
# =====================================================================
# Step-by-step case study demonstrating the 6-step debugging process:
#   1. Observe: Capture symptom
#   2. Reproduce: Build Minimal Reproducible Example (MRE)
#   3. Locate: Pinpoint root cause
#   4. Hypothesize: Explain why invalid state happened
#   5. Fix: Apply minimal correct edit
#   6. Verify: Confirm fix and test regression cases

class BuggyTokenCounter:
    """Contains a subtle bug: off-by-one error and mutating input list."""
    def count_tokens(self, messages: List[str]) -> int:
        # Defect: mutates messages via pop() and counts wrong range
        total = 0
        while len(messages) > 0:
            msg = messages.pop(0)  # Destructive mutation!
            total += len(msg.split())
        return total

class RepairedTokenCounter:
    """The fixed, non-destructive token counter."""
    def count_tokens(self, messages: List[str]) -> int:
        # Non-destructive iteration preserving caller input
        return sum(len(msg.split()) for msg in messages)

def demonstrate_scientific_workflow() -> None:
    print("\n" + "=" * 70)
    print("SECTION 5: THE SCIENTIFIC DEBUGGING WORKFLOW")
    print("=" * 70)

    # 1. Observe & 2. Reproduce with MRE
    test_messages = ["Hello agent", "Please perform task", "Status complete"]
    original_copy = list(test_messages)

    buggy_counter = BuggyTokenCounter()
    print("Step 1 & 2: Reproducing bug with minimal test input...")
    count_1 = buggy_counter.count_tokens(test_messages)
    print(f"  First count: {count_1} tokens")
    print(f"  Remaining messages in list after call: {len(test_messages)} (Expected 3!)")

    # Second call fails because input list was destroyed!
    count_2 = buggy_counter.count_tokens(test_messages)
    print(f"  Second count on same list: {count_2} tokens (BUG CONFIRMED: List was emptied)")

    # 3. Locate & 4. Hypothesize
    print("\nStep 3 & 4: Located defect in count_tokens() - while loop used messages.pop(0).")
    print("Hypothesis: Iterating directly without popping will preserve list integrity.")

    # 5. Fix & 6. Verify
    repaired_counter = RepairedTokenCounter()
    test_messages_2 = list(original_copy)
    repaired_1 = repaired_counter.count_tokens(test_messages_2)
    repaired_2 = repaired_counter.count_tokens(test_messages_2)

    assert repaired_1 == 7, f"Expected 7 tokens, got {repaired_1}"
    assert repaired_2 == 7, f"Expected 7 tokens on repeated run, got {repaired_2}"
    assert len(test_messages_2) == 3, "Input list should remain unmodified!"
    print(f"\nStep 5 & 6: Verification PASSED:")
    print(f"  Count 1: {repaired_1}, Count 2: {repaired_2}, List size preserved: {len(test_messages_2)}")


# =====================================================================
# SECTION 6: AUTONOMOUS ERROR TELEMETRY FOR AI AGENT TOOLING
# =====================================================================
# In an autonomous AI agent architecture, the agent itself must inspect
# errors produced by tool executions and formulate a self-correction.
#
# A Diagnostic Tool Harness intercepts exceptions, extracts structured
# telemetry, sanitizes sensitive data, and packages diagnostic JSON.

@dataclass
class DiagnosticReport:
    success: bool
    result: Optional[Any] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    failing_function: Optional[str] = None
    failing_line: Optional[int] = None
    sanitized_locals: Optional[Dict[str, str]] = None

class AgentToolHarness:
    """Executes agent tools with comprehensive diagnostic interception."""

    def __init__(self, sanitize_keys: Optional[List[str]] = None) -> None:
        self.sensitive_keywords = set(sanitize_keys or ["key", "token", "secret", "password"])

    def _sanitize(self, locals_dict: Dict[str, Any]) -> Dict[str, str]:
        """Redacts sensitive values from stack frame local variables."""
        sanitized = {}
        for k, v in locals_dict.items():
            if any(secret in k.lower() for secret in self.sensitive_keywords):
                sanitized[k] = "[REDACTED_SECRET]"
            else:
                sanitized[k] = repr(v)
        return sanitized

    def run(self, tool_func: Callable[..., Any], *args: Any, **kwargs: Any) -> DiagnosticReport:
        """Executes tool_func with automated diagnostic capture upon exception."""
        try:
            result = tool_func(*args, **kwargs)
            return DiagnosticReport(success=True, result=result)
        except Exception as exc:
            exc_type, exc_val, exc_tb = sys.exc_info()
            tb_frames = traceback.extract_tb(exc_tb)
            last_frame = tb_frames[-1]

            # Extract local variables from innermost traceback frame
            current_tb = exc_tb
            while current_tb.tb_next is not None:
                current_tb = current_tb.tb_next
            frame_locals = current_tb.tb_frame.f_locals

            return DiagnosticReport(
                success=False,
                error_type=type(exc).__name__,
                error_message=str(exc),
                failing_function=last_frame.name,
                failing_line=last_frame.lineno,
                sanitized_locals=self._sanitize(frame_locals)
            )

def sample_agent_search_tool(query: str, api_token: str, max_results: int = 5) -> Dict[str, Any]:
    """Sample tool simulating an API failure with sensitive credentials present."""
    if max_results <= 0:
        raise ValueError("max_results must be a positive integer greater than zero")
    return {"query": query, "items": [f"Result for {query} #{i+1}" for i in range(max_results)]}

def demonstrate_agent_error_telemetry() -> None:
    print("\n" + "=" * 70)
    print("SECTION 6: AUTONOMOUS ERROR TELEMETRY FOR AI AGENT TOOLING")
    print("=" * 70)

    harness = AgentToolHarness()

    # Successful call
    ok_report = harness.run(sample_agent_search_tool, "Python AST", api_token="sk-live-992384", max_results=3)
    print("\n1. Successful Tool Invocation Report:")
    print(f"   Success: {ok_report.success}, Items returned: {len(ok_report.result['items'])}")

    # Failing call (triggering ValueError with sensitive token in locals)
    err_report = harness.run(sample_agent_search_tool, "Python AST", api_token="sk-live-992384", max_results=-1)
    print("\n2. Intercepted Tool Crash Report:")
    print(f"   Success:          {err_report.success}")
    print(f"   Error Type:       {err_report.error_type}")
    print(f"   Error Message:    {err_report.error_message}")
    print(f"   Failing Function: {err_report.failing_function}() at line {err_report.failing_line}")
    print(f"   Sanitized Locals: {err_report.sanitized_locals}")
    assert err_report.sanitized_locals is not None
    assert err_report.sanitized_locals["api_token"] == "[REDACTED_SECRET]"
    print("   [✓] Verified: Sensitive credential was properly redacted before telemetry output!")


# =====================================================================
# MAIN ENTRY POINT
# =====================================================================

def main() -> None:
    print("Starting Module 32: Python Debugging Demonstrations...")
    demonstrate_traceback_anatomy()
    demonstrate_chained_exceptions()
    demonstrate_structured_logging()
    demonstrate_frame_introspection()
    demonstrate_scientific_workflow()
    demonstrate_agent_error_telemetry()
    print("\n" + "=" * 70)
    print("All Module 32 Debugging demonstrations executed cleanly and successfully!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
