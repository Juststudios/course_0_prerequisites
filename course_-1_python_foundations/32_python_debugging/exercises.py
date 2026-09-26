"""
Module 32 Exercises: Python Debugging and Diagnostic Engineering
================================================================
Practice mastering Python debugging techniques and automated diagnostics:
  - Level 1: Recall (Traceback String Parser)
  - Level 2: Modify (Structured Diagnostic Context Logger)
  - Level 3: Build (Autonomous Diagnostic Tool Runner)
  - Level 4: Debug (Repairing a Silent-Failing Batch Ingestion Pipeline)
"""

import sys
import traceback
from typing import Any, Callable, Dict, List, Optional


# =====================================================================
# LEVEL 1: RECALL — Traceback String Parser
# =====================================================================
# Task: Implement parse_traceback_summary(tb_str: str) -> dict[str, Any].
#
# Given a standard formatted Python traceback string (such as the output of
# traceback.format_exc()), extract structured diagnostic metadata:
#
# Requirements:
#   1. Raise ValueError if tb_str is empty or does not contain "Traceback (most recent call last):".
#   2. "exception_type": str — the name of the exception on the last line (e.g. "KeyError").
#   3. "exception_message": str — the error message following the exception type (e.g. "'user_id'").
#      If there is no message (e.g., bare "IndexError"), return an empty string "".
#   4. "failing_file": str — the filename in the innermost frame (e.g., "agent.py").
#   5. "failing_line": int — the line number in the innermost frame.
#   6. "frame_count": int — total number of 'File "..."' frames in the traceback.

def parse_traceback_summary(tb_str: str) -> dict[str, Any]:
    """Parses a standard Python traceback text into structured diagnostic metadata."""
    # TODO: Validate tb_str contains 'Traceback (most recent call last):'
    # TODO: Count frames and identify the innermost frame
    # TODO: Extract exception type, message, failing file, and failing line number
    raise NotImplementedError("Level 1: Implement parse_traceback_summary()")


# =====================================================================
# LEVEL 2: MODIFY — Structured Diagnostic Context Logger
# =====================================================================
# Task: Modify the AdHocLogger below to create a StructuredDiagnosticLogger.
#
# Current problem: AdHocLogger just uses print() directly, losing severity,
# timestamps, structured context dicts, and exception details.
#
# Requirements for StructuredDiagnosticLogger:
#   1. __init__(self) -> None: Initialize an internal records list: list[dict[str, Any]].
#   2. log(self, level: str, message: str, context: dict[str, Any] | None = None,
#          exc: Exception | None = None) -> dict[str, Any]:
#      - Validate that level is one of {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}.
#        Raise ValueError if invalid. Store level in uppercase.
#      - If exc is provided, extract {"type": type(exc).__name__, "message": str(exc)}.
#      - Build record: {
#            "level": level.upper(),
#            "message": message,
#            "context": context or {},
#            "exception": exc_info_dict or None
#        }
#      - Append record to self.records and return it.
#   3. get_errors(self) -> list[dict[str, Any]]:
#      - Return all records with level "ERROR" or "CRITICAL".

class AdHocLogger:
    """Old ad-hoc print logger that needs refactoring."""
    def log(self, msg: str) -> None:
        print(f"DEBUG: {msg}")


class StructuredDiagnosticLogger:
    """Refactored logger with level validation, structured context, and exception capture."""
    def __init__(self) -> None:
        # TODO: Initialize internal records list
        raise NotImplementedError("Level 2: Initialize StructuredDiagnosticLogger.__init__")

    def log(
        self,
        level: str,
        message: str,
        context: Optional[dict[str, Any]] = None,
        exc: Optional[Exception] = None,
    ) -> dict[str, Any]:
        """Logs a message with level validation, context dictionary, and optional exception capture."""
        # TODO: Validate severity level against allowed set
        # TODO: Format exception details if provided
        # TODO: Construct structured record, store in self.records, and return it
        raise NotImplementedError("Level 2: Implement StructuredDiagnosticLogger.log()")

    def get_errors(self) -> list[dict[str, Any]]:
        """Returns all records with level 'ERROR' or 'CRITICAL'."""
        # TODO: Filter self.records for ERROR or CRITICAL entries
        raise NotImplementedError("Level 2: Implement StructuredDiagnosticLogger.get_errors()")


# =====================================================================
# LEVEL 3: BUILD — Autonomous Diagnostic Tool Runner
# =====================================================================
# Task: Build a DiagnosticToolRunner that safely invokes tool functions,
# intercepts any crashes, and compiles a comprehensive diagnostic report.
#
# Requirements:
#   1. __init__(self, sensitive_keys: list[str] | None = None):
#      - Store set of lowercase sensitive keywords. Defaults to:
#        {"key", "token", "secret", "password"}
#   2. execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> dict[str, Any]:
#      - If func(*args, **kwargs) succeeds:
#          Return: {"status": "success", "result": result, "error": None}
#      - If an exception is raised:
#          - Extract exception type (name) and exception message.
#          - Use sys.exc_info() and traceback to find:
#              - failing_function (str): name of the innermost function
#              - failing_line (int): line number of the innermost frame
#          - Extract f_locals from the innermost frame.
#          - Sanitize locals: For any key where any sensitive keyword appears in
#            key.lower(), set value to "[REDACTED]". Otherwise, store repr(value).
#          - Return: {
#                "status": "error",
#                "result": None,
#                "error": {
#                    "type": exc_type_name,
#                    "message": exc_message,
#                    "function": failing_function,
#                    "line": failing_line,
#                    "locals": sanitized_locals
#                }
#            }

class DiagnosticToolRunner:
    """Safely executes callables with automated diagnostic interception and secrets redaction."""
    def __init__(self, sensitive_keys: Optional[list[str]] = None) -> None:
        # TODO: Store sensitive keywords in a set for sanitization
        raise NotImplementedError("Level 3: Implement DiagnosticToolRunner.__init__")

    def execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Executes func and returns structured result or diagnostic error payload."""
        # TODO: Try executing func(*args, **kwargs)
        # TODO: If exception occurs, inspect traceback frames, redact locals, and construct diagnostic report
        raise NotImplementedError("Level 3: Implement DiagnosticToolRunner.execute()")


# =====================================================================
# LEVEL 4: DEBUG — Repairing a Silent-Failing Batch Ingestion Pipeline
# =====================================================================
# Task: Debug and repair the BuggyBatchIngester below.
#
# The original BuggyBatchIngester has 3 critical defects:
#   Defect 1: Bare 'except: pass' silently drops failed records without reporting what failed.
#   Defect 2: Destructively pops elements from the input list (batch.pop(0)), mutating caller state!
#   Defect 3: Crashes on missing keys or wrong types instead of isolating the malformed item.
#
# Requirements for RepairedBatchIngester:
#   1. In ingest(self, batch: list[dict[str, Any]]) -> dict[str, Any]:
#      - Do NOT mutate the input list.
#      - Validate each item:
#          - Must be a dictionary.
#          - Must have key "id" with an int value (or valid integer string).
#          - Must have key "payload" which is a dict.
#      - Return a summary dictionary:
#          {
#              "processed": list_of_successfully_processed_items,
#              "failures": [
#                  {"index": original_index, "error": error_message, "item": item}
#              ]
#          }

class BuggyBatchIngester:
    """Contains multiple bugs: silent exception swallowing and input list destruction."""
    def ingest(self, batch: list) -> dict:
        processed = []
        while len(batch) > 0:
            item = batch.pop(0)  # BUG: Destroys caller's list!
            try:
                item_id = int(item["id"])
                data = item["payload"]["data"]
                processed.append({"id": item_id, "data": data})
            except Exception:
                pass  # BUG: Silently swallows error with no diagnostic trail!
        return {"processed": processed}


class RepairedBatchIngester:
    """The corrected, non-destructive, and diagnostically transparent batch ingester."""
    def ingest(self, batch: list[dict[str, Any]]) -> dict[str, Any]:
        """Ingests batch non-destructively, returning processed items and detailed failure records."""
        # TODO: Process items without mutating input batch
        # TODO: Validate "id" and "payload" safely
        # TODO: Return {"processed": [...], "failures": [...]}
        raise NotImplementedError("Level 4: Implement RepairedBatchIngester.ingest()")
