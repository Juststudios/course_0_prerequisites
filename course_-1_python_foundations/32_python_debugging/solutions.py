"""
Module 32 Solutions: Python Debugging and Diagnostic Engineering
================================================================
Reference implementations for all 4 levels of Module 32 exercises.
"""

import re
import sys
import traceback
from typing import Any, Callable, Dict, List, Optional


# =====================================================================
# LEVEL 1: RECALL — Traceback String Parser Solution
# =====================================================================

def parse_traceback_summary(tb_str: str) -> dict[str, Any]:
    """Parses a standard Python traceback text into structured diagnostic metadata."""
    if not tb_str or "Traceback (most recent call last):" not in tb_str:
        raise ValueError("Invalid traceback: missing 'Traceback (most recent call last):' header")

    lines = [ln.strip() for ln in tb_str.strip().splitlines() if ln.strip()]
    if not lines:
        raise ValueError("Empty traceback content")

    # Match all frame lines: File "path/file.py", line 42, in func_name
    frame_matches = list(re.finditer(r'File "([^"]+)", line (\d+), in (\S+)', tb_str))
    if not frame_matches:
        raise ValueError("No stack frames found in traceback")

    innermost_match = frame_matches[-1]
    failing_file_raw = innermost_match.group(1)
    failing_file = failing_file_raw.split("/")[-1].split("\\")[-1]
    failing_line = int(innermost_match.group(2))
    frame_count = len(frame_matches)

    # Last line contains exception name and message
    last_line = lines[-1]
    if ":" in last_line:
        parts = last_line.split(":", 1)
        exc_type = parts[0].strip()
        exc_message = parts[1].strip()
    else:
        exc_type = last_line.strip()
        exc_message = ""

    return {
        "exception_type": exc_type,
        "exception_message": exc_message,
        "failing_file": failing_file,
        "failing_line": failing_line,
        "frame_count": frame_count,
    }


# =====================================================================
# LEVEL 2: MODIFY — Structured Diagnostic Context Logger Solution
# =====================================================================

class StructuredDiagnosticLogger:
    """Refactored logger with level validation, structured context, and exception capture."""

    ALLOWED_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def log(
        self,
        level: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        exc: Optional[Exception] = None,
    ) -> Dict[str, Any]:
        """Logs a message with level validation, context dictionary, and optional exception capture."""
        level_upper = level.upper()
        if level_upper not in self.ALLOWED_LEVELS:
            raise ValueError(f"Invalid log level '{level}'. Must be one of {sorted(self.ALLOWED_LEVELS)}")

        exc_info = None
        if exc is not None:
            exc_info = {
                "type": type(exc).__name__,
                "message": str(exc),
            }

        record = {
            "level": level_upper,
            "message": message,
            "context": dict(context) if context is not None else {},
            "exception": exc_info,
        }
        self.records.append(record)
        return record

    def get_errors(self) -> List[Dict[str, Any]]:
        """Returns all records with level 'ERROR' or 'CRITICAL'."""
        return [r for r in self.records if r["level"] in {"ERROR", "CRITICAL"}]


# =====================================================================
# LEVEL 3: BUILD — Autonomous Diagnostic Tool Runner Solution
# =====================================================================

class DiagnosticToolRunner:
    """Safely executes callables with automated diagnostic interception and secrets redaction."""

    def __init__(self, sensitive_keys: Optional[List[str]] = None) -> None:
        keywords = sensitive_keys or ["key", "token", "secret", "password"]
        self.sensitive_keywords = {k.lower() for k in keywords}

    def _sanitize_locals(self, frame_locals: Dict[str, Any]) -> Dict[str, str]:
        """Redacts values of variables matching any sensitive keyword."""
        sanitized = {}
        for var_name, var_value in frame_locals.items():
            if any(secret in var_name.lower() for secret in self.sensitive_keywords):
                sanitized[var_name] = "[REDACTED]"
            else:
                sanitized[var_name] = repr(var_value)
        return sanitized

    def execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Executes func and returns structured result or diagnostic error payload."""
        try:
            result = func(*args, **kwargs)
            return {"status": "success", "result": result, "error": None}
        except Exception as exc:
            exc_type, exc_val, exc_tb = sys.exc_info()
            tb_frames = traceback.extract_tb(exc_tb)
            last_frame = tb_frames[-1] if tb_frames else None
            failing_function = last_frame.name if last_frame else "unknown"
            failing_line = last_frame.lineno if last_frame else -1

            # Traverse to innermost traceback frame to extract its local variables
            current_tb = exc_tb
            while current_tb is not None and current_tb.tb_next is not None:
                current_tb = current_tb.tb_next
            raw_locals = current_tb.tb_frame.f_locals if current_tb is not None else {}

            sanitized_locals = self._sanitize_locals(raw_locals)

            return {
                "status": "error",
                "result": None,
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "function": failing_function,
                    "line": failing_line,
                    "locals": sanitized_locals,
                },
            }


# =====================================================================
# LEVEL 4: DEBUG — Repaired Batch Ingestion Pipeline Solution
# =====================================================================

class RepairedBatchIngester:
    """The corrected, non-destructive, and diagnostically transparent batch ingester."""

    def ingest(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ingests batch non-destructively, returning processed items and detailed failure records."""
        processed: List[Dict[str, Any]] = []
        failures: List[Dict[str, Any]] = []

        # Iterate without mutating the input list
        for idx, item in enumerate(batch):
            if not isinstance(item, dict):
                failures.append({
                    "index": idx,
                    "error": f"Item at index {idx} must be a dictionary, got {type(item).__name__}",
                    "item": item,
                })
                continue

            if "id" not in item:
                failures.append({
                    "index": idx,
                    "error": "Missing mandatory 'id' key",
                    "item": item,
                })
                continue

            try:
                item_id = int(item["id"])
            except (ValueError, TypeError) as conv_err:
                failures.append({
                    "index": idx,
                    "error": f"Invalid integer value for 'id': {conv_err}",
                    "item": item,
                })
                continue

            payload = item.get("payload")
            if not isinstance(payload, dict):
                failures.append({
                    "index": idx,
                    "error": f"'payload' must be a dictionary, got {type(payload).__name__}",
                    "item": item,
                })
                continue

            if "data" not in payload:
                failures.append({
                    "index": idx,
                    "error": "Missing mandatory 'data' key inside payload",
                    "item": item,
                })
                continue

            processed.append({"id": item_id, "data": payload["data"]})

        return {"processed": processed, "failures": failures}


# =====================================================================
# VERIFICATION RUNNER
# =====================================================================

def verify_module_32() -> None:
    print("Verifying Module 32 Solutions...")

    # --- Test Level 1: parse_traceback_summary ---
    sample_tb = (
        'Traceback (most recent call last):\n'
        '  File "/home/user/agent/pipeline.py", line 42, in run\n'
        '    res = self.step(action)\n'
        '  File "/home/user/agent/tools.py", line 105, in calculate\n'
        '    return a / b\n'
        'ZeroDivisionError: division by zero\n'
    )
    parsed = parse_traceback_summary(sample_tb)
    assert parsed["exception_type"] == "ZeroDivisionError", f"Got {parsed['exception_type']}"
    assert parsed["exception_message"] == "division by zero"
    assert parsed["failing_file"] == "tools.py"
    assert parsed["failing_line"] == 105
    assert parsed["frame_count"] == 2

    # Verify invalid traceback raises ValueError
    try:
        parse_traceback_summary("SyntaxError: invalid syntax")
        assert False, "Should have raised ValueError on missing Traceback header"
    except ValueError:
        pass
    print("  [✓] Level 1 (Recall) passed!")

    # --- Test Level 2: StructuredDiagnosticLogger ---
    logger = StructuredDiagnosticLogger()
    r1 = logger.log("info", "Agent initialized", {"agent_id": "hermes-1"})
    assert r1["level"] == "INFO"
    assert r1["context"]["agent_id"] == "hermes-1"
    assert r1["exception"] is None

    err = KeyError("missing_param")
    r2 = logger.log("error", "Tool execution failed", {"tool": "search"}, exc=err)
    assert r2["level"] == "ERROR"
    assert r2["exception"]["type"] == "KeyError"
    assert r2["exception"]["message"] == "'missing_param'"

    assert len(logger.records) == 2
    errors = logger.get_errors()
    assert len(errors) == 1
    assert errors[0]["level"] == "ERROR"

    # Verify invalid level raises ValueError
    try:
        logger.log("INVALID_LEVEL", "test message")
        assert False, "Should have raised ValueError on invalid level"
    except ValueError:
        pass
    print("  [✓] Level 2 (Modify) passed!")

    # --- Test Level 3: DiagnosticToolRunner ---
    runner = DiagnosticToolRunner()

    # Success case
    def good_tool(x: int, y: int) -> int:
        return x + y

    res_ok = runner.execute(good_tool, 10, 20)
    assert res_ok["status"] == "success"
    assert res_ok["result"] == 30
    assert res_ok["error"] is None

    # Error case with secrets in locals
    def secret_tool(api_key: str, count: int) -> float:
        user_token = "bearer_xyz_9988"
        multiplier = 0
        return count / multiplier

    res_err = runner.execute(secret_tool, api_key="super_secret_val", count=100)
    assert res_err["status"] == "error"
    assert res_err["result"] is None
    err_dict = res_err["error"]
    assert err_dict["type"] == "ZeroDivisionError"
    assert err_dict["function"] == "secret_tool"
    assert err_dict["locals"]["api_key"] == "[REDACTED]"
    assert err_dict["locals"]["user_token"] == "[REDACTED]"
    assert "100" in err_dict["locals"]["count"]
    print("  [✓] Level 3 (Build) passed!")

    # --- Test Level 4: RepairedBatchIngester ---
    ingester = RepairedBatchIngester()
    input_batch = [
        {"id": 1, "payload": {"data": "alpha"}},
        {"id": "2", "payload": {"data": "beta"}},
        "not_a_dict",
        {"id": 4},  # missing payload
        {"id": "bad_id", "payload": {"data": "gamma"}},
        {"id": 5, "payload": {"no_data_key": 123}},
    ]
    batch_copy = list(input_batch)

    summary = ingester.ingest(input_batch)
    # Verify non-destructive
    assert len(input_batch) == len(batch_copy), "Input batch list must not be mutated"
    assert len(summary["processed"]) == 2
    assert summary["processed"][0] == {"id": 1, "data": "alpha"}
    assert summary["processed"][1] == {"id": 2, "data": "beta"}
    assert len(summary["failures"]) == 4
    print("  [✓] Level 4 (Debug) passed!")

    print("All Module 32 solutions verified successfully!\n")


if __name__ == "__main__":
    verify_module_32()
