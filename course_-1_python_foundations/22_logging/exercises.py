"""
Module 22: Logging — Exercises
===============================

Practice severity levels, custom handlers, formatters, and structured JSON logging.
Complete the four progressive exercise levels below.
"""

import io
import json
import logging
from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
def get_logging_level_constants() -> Dict[str, int]:
    """
    Recall Exercise:
    Return a dictionary mapping the 5 standard logging level names
    ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL") to their exact
    integer threshold values defined in Python's `logging` module.

    # TODO: Return the dictionary of standard level integer values.
    """
    # TODO: Replace the line below with your dictionary
    raise NotImplementedError("Level 1: Implement get_logging_level_constants().")


# =====================================================================
# Level 2: Modify
# =====================================================================
def setup_memory_logger(name: str, level: int = logging.INFO) -> Tuple[logging.Logger, io.StringIO]:
    """
    Modify / Adapt Exercise:
    Create and configure a dedicated logger that writes log output to an
    in-memory `io.StringIO` buffer for testing or inspection.

    Requirements:
    - Obtain or create a logger with the given `name`.
    - Set the logger's level to `level`.
    - Set `logger.propagate = False` to prevent messages leaking to root handlers.
    - Clear any existing handlers on the logger to ensure a clean state.
    - Create an `io.StringIO` stream buffer.
    - Create a `logging.StreamHandler` directing to the stream buffer.
    - Attach a `logging.Formatter` with format: `"%(levelname)s: %(message)s"`.
    - Add the handler to the logger.
    - Return a tuple `(logger, stream_buffer)`.
    """
    # TODO: Implement setup_memory_logger
    raise NotImplementedError("Level 2: Implement setup_memory_logger().")


# =====================================================================
# Level 3: Build
# =====================================================================
class SimpleJsonFormatter(logging.Formatter):
    """
    Build Exercise:
    Implement a custom `logging.Formatter` subclass that outputs every
    `LogRecord` as a valid single-line JSON string.

    Requirements:
    - Output must be a valid JSON string (parseable by `json.loads`).
    - The JSON object must contain at least the following keys:
        - "level": record.levelname (e.g. "INFO", "ERROR")
        - "logger": record.name
        - "message": record.getMessage()
    - If `record.exc_info` is present, include an "exception" key containing
      the formatted traceback string (use `self.formatException(record.exc_info)`).
    - If a custom attribute `agent_id` is present on the record, include it
      as "agent_id" in the JSON object.
    """
    def format(self, record: logging.LogRecord) -> str:
        # TODO: Implement the JSON formatting logic
        raise NotImplementedError("Level 3: Implement SimpleJsonFormatter.format().")


# =====================================================================
# Level 4: Debug
# =====================================================================
def log_agent_crash_safe(logger: logging.Logger, error_message: str, exc: Exception) -> None:
    """
    Debug Exercise:
    The following function is intended to log an error message along with the
    full exception traceback so that on-call engineers can diagnose the failure.

    However, the buggy implementation below suffers from multiple critical bugs:
      1. It only logs `str(exc)`, completely throwing away the stack trace.
      2. It uses `logger.debug` instead of `logger.error` or `logger.exception`.
      3. It attempts to concatenate strings rather than using logging arguments.

    Buggy code:
        def log_agent_crash_safe(logger, error_message, exc):
            # BUG: Logs at debug level, loses stack trace!
            logger.debug(error_message + ": " + str(exc))

    # TODO: Fix log_agent_crash_safe so that it logs at ERROR level,
    # passes error_message, and includes exc_info=exc so the full traceback is preserved.
    """
    # TODO: Implement the corrected function
    raise NotImplementedError("Level 4: Fix log_agent_crash_safe().")


if __name__ == "__main__":
    print("Module 22 Exercises loaded successfully.")
    print("Complete the TODOs and verify your work with solutions.py.")
