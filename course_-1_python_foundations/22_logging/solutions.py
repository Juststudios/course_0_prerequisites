"""
Module 22: Logging — Reference Solutions
=========================================

Complete, verified reference solutions for all four exercise tiers.
"""

import io
import json
import logging
from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def get_logging_level_constants() -> Dict[str, int]:
    """
    Returns standard logging level threshold values:
      DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50
    """
    return {
        "DEBUG": logging.DEBUG,       # 10
        "INFO": logging.INFO,         # 20
        "WARNING": logging.WARNING,   # 30
        "ERROR": logging.ERROR,       # 40
        "CRITICAL": logging.CRITICAL, # 50
    }


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def setup_memory_logger(name: str, level: int = logging.INFO) -> Tuple[logging.Logger, io.StringIO]:
    """
    Configures an in-memory logger writing to an io.StringIO buffer.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Clear any pre-existing handlers
    logger.handlers.clear()

    buffer = io.StringIO()
    handler = logging.StreamHandler(buffer)
    handler.setLevel(level)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, buffer


# =====================================================================
# Level 3: Build Solution
# =====================================================================
class SimpleJsonFormatter(logging.Formatter):
    """
    Custom Formatter producing valid single-line JSON log strings.
    """
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "agent_id"):
            payload["agent_id"] = record.agent_id
        return json.dumps(payload)


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def log_agent_crash_safe(logger: logging.Logger, error_message: str, exc: Exception) -> None:
    """
    Corrected crash logger:
      - Uses ERROR level
      - Employs exc_info=exc to preserve full traceback
    """
    logger.error(error_message, exc_info=exc)


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    levels = get_logging_level_constants()
    assert levels == {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }, f"Level 1 failed: {levels}"

    # Test Level 2
    mem_logger, stream = setup_memory_logger("test_agent_logger", level=logging.WARNING)
    mem_logger.info("This info log should be filtered out")
    mem_logger.warning("This warning should be captured")
    mem_logger.error("This error should be captured")

    lines = stream.getvalue().strip().splitlines()
    assert len(lines) == 2, f"Expected 2 lines, got {len(lines)}: {lines}"
    assert lines[0] == "WARNING: This warning should be captured"
    assert lines[1] == "ERROR: This error should be captured"

    # Test Level 3
    json_formatter = SimpleJsonFormatter()
    # Create mock LogRecord
    rec = logging.LogRecord(
        name="agent.reasoning",
        level=logging.INFO,
        pathname="agent.py",
        lineno=42,
        msg="Found solution to problem",
        args=(),
        exc_info=None,
    )
    rec.agent_id = "agent_007"
    formatted_json = json_formatter.format(rec)
    parsed = json.loads(formatted_json)
    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "agent.reasoning"
    assert parsed["message"] == "Found solution to problem"
    assert parsed["agent_id"] == "agent_007"

    # Test Level 4
    crash_logger, crash_stream = setup_memory_logger("crash_test", level=logging.DEBUG)
    # Re-attach custom handler with exc_info formatting
    crash_logger.handlers[0].setFormatter(logging.Formatter("%(levelname)s: %(message)s\n%(exc_text)s"))
    try:
        raise ValueError("Simulated invalid tool schema")
    except ValueError as e:
        log_agent_crash_safe(crash_logger, "Tool execution aborted", e)

    crash_output = crash_stream.getvalue()
    assert "ERROR: Tool execution aborted" in crash_output
    assert "ValueError: Simulated invalid tool schema" in crash_output
    assert "Traceback" in crash_output

    print("Module 22: All Level 1-4 solutions verified successfully!")
