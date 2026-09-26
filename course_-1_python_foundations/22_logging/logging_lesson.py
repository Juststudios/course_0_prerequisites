"""
Module 22: Logging and Observability
====================================

This lesson explores Python's logging infrastructure, contrasting print-based
debugging with production telemetry. We explore severity levels, handlers,
formatters, hierarchical propagation, exception tracebacks, and structured
JSON logging for autonomous AI agents.

Topics covered:
  1. Why `print()` Fails in Production: The Case for Logging
  2. The 5 Severity Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
  3. The Core Architecture: Loggers, Handlers, and Formatters
  4. Hierarchical Naming and Propagation (`agent.perception.vision`)
  5. Recording Exceptions and Stack Traces with `logger.exception()`
  6. Writing to In-Memory Streams and Files simultaneously
  7. Structured JSON Logging for Modern Observability
  8. AI Agent Application: Complete ReAct Agent Observability Engine
"""

import io
import json
import logging
import sys
import time
from typing import Any, Dict, Optional


# =====================================================================
# 1. Why `print()` Fails in Production: The Case for Logging
# =====================================================================
print("=" * 70)
print("1. WHY `print()` FAILS IN PRODUCTION: THE CASE FOR LOGGING")
print("=" * 70)

# Print lacks severity levels, destination routing, timestamps, and cannot
# be turned off without modifying code. Logging gives full decoupled control.

# Basic root configuration for demonstration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

root_logger = logging.getLogger("demo_root")
root_logger.info("This is an INFO message via Python's logging subsystem.")


# =====================================================================
# 2. The 5 Severity Levels and Threshold Filtering
# =====================================================================
print("\n" + "=" * 70)
print("2. THE 5 SEVERITY LEVELS AND THRESHOLD FILTERING")
print("=" * 70)

# Python defines 5 standard severity levels with numeric integer thresholds:
#   DEBUG:    10
#   INFO:     20
#   WARNING:  30
#   ERROR:    40
#   CRITICAL: 50

level_demo_logger = logging.getLogger("level_demo")
level_demo_logger.setLevel(logging.WARNING)  # Only WARNING, ERROR, CRITICAL will be emitted

print(f"Logger '{level_demo_logger.name}' threshold set to WARNING (30):")
print("Emitting messages across all 5 levels:")
level_demo_logger.debug("  [DEBUG 10] Highly detailed internal state (IGNORED)")
level_demo_logger.info("  [INFO 20] General milestone message (IGNORED)")
level_demo_logger.warning("  [WARNING 30] Resource running low or retry imminent (EMITTED)")
level_demo_logger.error("  [ERROR 40] Failed to reach target endpoint (EMITTED)")
level_demo_logger.critical("  [CRITICAL 50] System fatal error: exiting (EMITTED)")


# =====================================================================
# 3. Core Architecture: Loggers, Handlers, and Formatters
# =====================================================================
print("\n" + "=" * 70)
print("3. CORE ARCHITECTURE: LOGGERS, HANDLERS, AND FORMATTERS")
print("=" * 70)

# A Logger generates LogRecords.
# A Handler sends LogRecords to an output destination (terminal, file, socket).
# A Formatter turns LogRecord metadata into formatted text.

custom_logger = logging.getLogger("custom_subsystem")
custom_logger.setLevel(logging.DEBUG)
custom_logger.propagate = False  # Prevent bubbling up to avoid duplicate prints

# Create a StreamHandler directing to stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)

# Define a custom human-readable formatter
custom_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-7s | [%(name)s:%(lineno)d] -> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
stdout_handler.setFormatter(custom_formatter)
custom_logger.addHandler(stdout_handler)

custom_logger.debug("This DEBUG log is blocked by the handler's INFO threshold.")
custom_logger.info("This INFO log is accepted and nicely formatted!")
custom_logger.warning("This WARNING log alerts the operator!")


# =====================================================================
# 4. Hierarchical Naming and Propagation
# =====================================================================
print("\n" + "=" * 70)
print("4. HIERARCHICAL NAMING AND PROPAGATION")
print("=" * 70)

# Logger names use dots to indicate hierarchy:
# "agent" is the parent of "agent.planner" and "agent.tools"
parent_logger = logging.getLogger("agent")
parent_logger.setLevel(logging.INFO)
parent_logger.propagate = False

parent_stream = io.StringIO()
parent_handler = logging.StreamHandler(parent_stream)
parent_handler.setFormatter(logging.Formatter("[PARENT HANDLER] %(name)s: %(message)s"))
parent_logger.addHandler(parent_handler)

# Child logger inherits from parent
child_logger = logging.getLogger("agent.planner")
# child_logger has no handlers attached directly, so its logs propagate to parent!
child_logger.info("Planner formulated 3 execution sub-goals.")

print(f"Captured by Parent Logger:\n  {parent_stream.getvalue().strip()}")


# =====================================================================
# 5. Recording Exceptions and Stack Traces with `logger.exception()`
# =====================================================================
print("\n" + "=" * 70)
print("5. RECORDING EXCEPTIONS AND STACK TRACES WITH `logger.exception()`")
print("=" * 70)

err_logger = logging.getLogger("error_reporter")
err_logger.setLevel(logging.ERROR)
err_logger.propagate = False

err_stream = io.StringIO()
err_handler = logging.StreamHandler(err_stream)
err_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
err_logger.addHandler(err_handler)

def dangerous_tool_calculation(dividend: int, divisor: int) -> float:
    return dividend / divisor

try:
    dangerous_tool_calculation(100, 0)
except ZeroDivisionError:
    # logger.exception automatically captures exc_info=True (the full traceback!)
    err_logger.exception("Calculation failed in tool runtime!")

err_output = err_stream.getvalue()
print("Captured Exception Log with Full Traceback:")
print(err_output[:300] + "... [traceback continues] ...")


# =====================================================================
# 6. Writing to In-Memory Streams & Files
# =====================================================================
print("\n" + "=" * 70)
print("6. MULTI-DESTINATION LOGGING (MEMORY AND FILE)")
print("=" * 70)

multi_logger = logging.getLogger("multi_dest")
multi_logger.setLevel(logging.DEBUG)
multi_logger.propagate = False

# Memory buffer
mem_buffer = io.StringIO()
mem_h = logging.StreamHandler(mem_buffer)
mem_h.setLevel(logging.DEBUG)
mem_h.setFormatter(logging.Formatter("[MEM] %(message)s"))
multi_logger.addHandler(mem_h)

# Stdout buffer
console_h = logging.StreamHandler(sys.stdout)
console_h.setLevel(logging.WARNING)
console_h.setFormatter(logging.Formatter("[CONSOLE ALERT] %(message)s"))
multi_logger.addHandler(console_h)

multi_logger.debug("Writing debug details to memory buffer only.")
multi_logger.warning("Writing warning to BOTH memory buffer AND console!")

print(f"\nMemory buffer contents:\n{mem_buffer.getvalue().strip()}")


# =====================================================================
# 7. Structured JSON Logging for Modern Observability
# =====================================================================
print("\n" + "=" * 70)
print("7. STRUCTURED JSON LOGGING FOR OBSERVABILITY")
print("=" * 70)

class JsonLogFormatter(logging.Formatter):
    """
    Custom formatter that encodes LogRecord data into valid JSON lines.
    """
    def format(self, record: logging.LogRecord) -> str:
        record_dict = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "line": record.lineno,
        }
        if record.exc_info:
            record_dict["exception"] = self.formatException(record.exc_info)
        # Check for custom extra parameters passed to logger call
        if hasattr(record, "task_id"):
            record_dict["task_id"] = record.task_id
        if hasattr(record, "tokens"):
            record_dict["tokens"] = record.tokens
        return json.dumps(record_dict)

json_logger = logging.getLogger("json_service")
json_logger.setLevel(logging.INFO)
json_logger.propagate = False

json_buf = io.StringIO()
json_h = logging.StreamHandler(json_buf)
json_h.setFormatter(JsonLogFormatter(datefmt="%Y-%m-%dT%H:%M:%SZ"))
json_logger.addHandler(json_h)

json_logger.info("Agent task initiated", extra={"task_id": "task-8492", "tokens": 142})
json_logger.info("Tool execution finished", extra={"task_id": "task-8492", "tokens": 380})

print("Formatted JSON Log Lines:")
for line in json_buf.getvalue().strip().splitlines():
    print(f"  {line}")


# =====================================================================
# 8. AI Agent Observability Case Study: Telemetry & Tracing
# =====================================================================
print("\n" + "=" * 70)
print("8. AI AGENT CASE STUDY: OBSERVABILITY ENGINE")
print("=" * 70)

class AgentTelemetry:
    """
    Observability wrapper for autonomous agents.
    Provides structured logging of thoughts, actions, and observations.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        self.telemetry_stream = io.StringIO()
        handler = logging.StreamHandler(self.telemetry_stream)
        handler.setFormatter(JsonLogFormatter())
        self.logger.addHandler(handler)

    def log_thought(self, thought: str):
        self.logger.debug(thought, extra={"agent_id": self.agent_id, "phase": "thought"})

    def log_action(self, tool_name: str, args: Dict[str, Any]):
        msg = f"Executing tool: {tool_name} with args={args}"
        self.logger.info(msg, extra={"agent_id": self.agent_id, "tool": tool_name})

    def log_error(self, message: str):
        self.logger.error(message, extra={"agent_id": self.agent_id, "phase": "recovery"})

agent_monitor = AgentTelemetry("agent_m4")
agent_monitor.log_thought("Thinking: Reading manifest files to find targets.")
agent_monitor.log_action("run_command", {"CommandLine": "git status", "Cwd": "/home/pearl"})
agent_monitor.log_error("Subprocess returned non-zero exit code 1.")

print(f"Agent Telemetry successfully recorded {len(agent_monitor.telemetry_stream.getvalue().strip().splitlines())} structured events.")

print("\n" + "=" * 70)
print("Module 22 lesson completed successfully!")
print("=" * 70)