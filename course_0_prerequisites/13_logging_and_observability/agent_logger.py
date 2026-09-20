"""agent_logger.py - Structured JSON logging with contextual trace attributes for AI agents.

Key concepts demonstrated:
1. Custom logging.Formatter outputting compliant JSON lines.
2. Contextual log filtering to inject task-local trace IDs.
3. Capturing structured exceptions and extra key-value pairs.
"""

from typing import Any, Dict
from datetime import datetime, timezone
import logging
import json
import io
import contextvars

# ContextVar for active trace ID
trace_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id_var", default="trace_none")


class JSONLogFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": getattr(record, "trace_id", "trace_none"),
        }

        # Include extra attributes if provided in record.__dict__
        if hasattr(record, "extra_data"):
            log_entry["data"] = record.extra_data

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class TraceContextFilter(logging.Filter):
    """Automatically injects the current ContextVar trace_id into every record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = trace_id_var.get()
        return True


def setup_agent_logger(stream: io.StringIO | None = None) -> logging.Logger:
    """Creates a configured logger that outputs structured JSON."""
    logger = logging.getLogger("agent.core")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = logging.StreamHandler(stream)
    handler.setFormatter(JSONLogFormatter())
    handler.addFilter(TraceContextFilter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def main() -> None:
    print("=== Module 13: Structured JSON Logging Demo ===")

    log_buffer = io.StringIO()
    logger = setup_agent_logger(log_buffer)

    # 1. Log with default trace_id
    logger.info("Initializing agent runtime.")

    # 2. Log within a scoped trace context
    token = trace_id_var.set("trace_req_778899")
    logger.info("Starting multi-step ReAct trajectory.", extra={"extra_data": {"user_id": "user_42"}})
    logger.warning("Tool execution took longer than expected: 450ms")

    try:
        raise ValueError("Simulated network timeout")
    except ValueError:
        logger.error("Failed to connect to tool gateway", exc_info=True)

    trace_id_var.reset(token)
    logger.info("Agent runtime shutdown complete.")

    # Parse and assert emitted JSON lines
    raw_logs = log_buffer.getvalue().strip().splitlines()
    assert len(raw_logs) == 5, f"Expected 5 log lines, got {len(raw_logs)}"

    parsed_logs = [json.loads(line) for line in raw_logs]

    # Verify first line
    assert parsed_logs[0]["message"] == "Initializing agent runtime."
    assert parsed_logs[0]["trace_id"] == "trace_none"

    # Verify scoped trace line
    assert parsed_logs[1]["trace_id"] == "trace_req_778899"
    assert parsed_logs[1]["data"]["user_id"] == "user_42"

    # Verify exception capture
    assert "exception" in parsed_logs[3]
    assert "ValueError: Simulated network timeout" in parsed_logs[3]["exception"]

    print("Emitted Structured JSON Logs:")
    for line in raw_logs:
        print(line)

    print("\n[OK] All structured JSON logging assertions verified successfully!\n")


if __name__ == "__main__":
    main()
