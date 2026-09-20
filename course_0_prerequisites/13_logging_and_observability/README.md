# Module 13: Logging, Observability, and Distributed Tracing in AI Agents

## 1. Learning Objectives
By the end of this module, you will be able to:
- Configure Python's standard `logging` module to emit machine-readable structured JSON logs.
- Propagate distributed tracing identifiers (`trace_id`, `span_id`, `parent_span_id`) across complex asynchronous agent workflows.
- Measure and record granular execution latencies for LLM generation, tool dispatch, and memory queries.
- Track cumulative token expenditures (prompt tokens, completion tokens, dollar costs) per request.
- Construct immutable audit records to replay and diagnose non-deterministic agent trajectories.

---

## 2. Why AI Agent Engineers Need This
Autonomous agents are inherently non-deterministic, multi-step systems. In production:
- A user reports: *"The agent gave me an incorrect response 10 minutes ago."*
- Without structured tracing, you have no way to know:
  - Which prompt was sent to the model?
  - Which tools did the agent invoke, and with what arguments?
  - Did a tool fail or return stale data?
  - How many tokens were consumed, and why did step 4 take 12 seconds?

Unstructured `print()` statements cannot be filtered, aggregated, or parsed by observability backends (such as Datadog, Grafana Loki, OpenTelemetry, or LangSmith). Structured JSON logging and span-based distributed tracing provide the x-ray visibility necessary to debug production agent swarms.

---

## 3. Structured Concept Breakdown

### Concept 1: Structured JSON Logging
- **TERM**: Structured JSON Logging
- **DEFINITION**: Emitting log messages as serialized JSON objects containing key-value pairs (timestamp, log level, message, logger name, and contextual attributes) rather than arbitrary plaintext strings.
- **INTUITION**: An itemized bank statement vs a loose pile of handwritten receipts. A bank statement has clear columns for date, merchant, category, and amount, making automated filtering and search effortless.
- **WHY IT EXISTS**: Centralized log aggregators index JSON fields automatically. You can run queries like `level:ERROR AND tool:calculator AND duration_ms > 500` across millions of log lines in seconds.
- **HOW IT WORKS**: A custom `logging.Formatter` subclass overrides `format(record)`. It gathers attributes from `record` and returns `json.dumps(log_record)`.
- **CODE**:
```python
import logging
import json
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "trace_id"):
            log_obj["trace_id"] = record.trace_id
        return json.dumps(log_obj)
```

---

### Concept 2: Trace and Span IDs
- **TERM**: Trace and Span Hierarchy
- **DEFINITION**: A distributed tracing model where a `trace_id` uniquely identifies an entire end-to-end request, and `span_id` identifies individual timed operations within that trace, linked via `parent_span_id`.
- **INTUITION**: A family tree. The overarching family name is the `trace_id`. The grandparent is the root span (user query); the children are intermediate spans (planning, tool execution); the grandchildren are leaf spans (HTTP calls, DB queries).
- **WHY IT EXISTS**: In an agent workflow with 5 steps and 15 tool executions, knowing which tool was called as part of which reasoning turn is impossible without span linkage.
- **HOW IT WORKS**: The agent creates a `trace_id = uuid4()` at request receipt. Each sub-operation enters a span context manager that records a new `span_id`, references `parent_span_id`, and calculates start/end duration.
- **CODE**:
```python
import uuid

class Span:
    def __init__(self, name: str, trace_id: str, parent_id: str | None = None):
        self.span_id = str(uuid.uuid4())[:8]
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.name = name
```

---

### Concept 3: Token Accounting & Cost Tracking
- **TERM**: Token Accounting
- **DEFINITION**: Tracking the exact count of input (prompt) and output (completion) tokens consumed during each model call and calculating cumulative monetary cost.
- **INTUITION**: The taxi meter in a cab. It ticks continuously as you travel, ensuring both passenger and driver know the exact fare and distance accrued.
- **WHY IT EXISTS**: Multi-step agents can easily enter loops that burn through hundreds of thousands of tokens per hour. Real-time accounting triggers budget alerts and enforces per-request spending caps.
- **HOW IT WORKS**: After every LLM completion, the response metadata (e.g. `usage.prompt_tokens`, `usage.completion_tokens`) is recorded in the active span and accumulated into a session billing summary.
- **CODE**:
```python
class TokenAccountant:
    def __init__(self, cost_per_1k_input: float = 0.0015, cost_per_1k_output: float = 0.002):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.cost_in = cost_per_1k_input
        self.cost_out = cost_per_1k_output

    def record(self, prompt_tokens: int, completion_tokens: int):
        self.total_input_tokens += prompt_tokens
        self.total_output_tokens += completion_tokens

    @property
    def total_cost_usd(self) -> float:
        return (self.total_input_tokens / 1000 * self.cost_in) + (self.total_output_tokens / 1000 * self.cost_out)
```

---

### Concept 4: Audit Trails for Tool Execution
- **TERM**: Immutable Tool Audit Trail
- **DEFINITION**: A permanent log capturing every tool call: caller trace, tool name, raw input arguments, returned result, success status, and execution duration.
- **INTUITION**: An aircraft flight data recorder (the "black box"). If an airplane encounters turbulence or an accident, investigators analyze the black box to determine exactly what happened millisecond by millisecond.
- **WHY IT EXISTS**: Enables post-incident analysis (security audits, debugging hallucinations) and offline evaluation (curating fine-tuning datasets from successful agent runs).
- **HOW IT WORKS**: Before and after tool dispatch, the runner constructs an audit dictionary and writes it to persistent storage.
- **CODE**:
```python
def log_audit(trace_id: str, tool: str, args: dict, result: dict, duration_ms: float, success: bool):
    audit_record = {
        "trace_id": trace_id,
        "tool": tool,
        "args": args,
        "result": result,
        "duration_ms": duration_ms,
        "success": success
    }
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Unstructured Print Debugging in Production
- **The Bug**: Using `print(f"Tool called: {x}")` instead of standard logging.
- **The Consequence**: Logs lack timestamps, severity levels, and trace IDs. In concurrent production environments, lines from different user sessions interleave arbitrarily, making debugging impossible.
- **The Fix**: Use Python's standard `logging` library with a structured JSON formatter.

### Anti-Pattern 2: Blind Token Consumption
- **The Bug**: Running an agent loop without tracking token counts.
- **The Consequence**: An unexpected prompt explosion or recursive tool loop triggers thousands of dollars in surprise cloud LLM bills.
- **The Fix**: Enforce token thresholds in the token accountant and terminate runs exceeding the configured budget.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. Why is structured JSON logging preferred over plain text formatting in production?
2. What is the difference between a `trace_id` and a `span_id`?
3. What information should be captured in a tool audit trail?

### Tier 2 (Debugging)
Find the issue in this logging setup:
```python
logger = logging.getLogger("agent")
logger.info(f"User {user_id} called tool {tool} with args {args}")
```
*Hint*: String interpolation forces formatting even when the log level is disabled, and doesn't emit structured JSON fields for log aggregators.

### Tier 3 (Application)
Write a custom `logging.Filter` that injects the current `trace_id` from a `ContextVar` into every log record emitted by any logger.

### Tier 4 (Challenge)
Build a complete `AgentTelemetry` system:
- Emits structured JSON logs.
- Supports hierarchical spans with context managers (`with telemetry.span("execute_tool"): ...`).
- Tracks token consumption and latency per span.
- Formats a comprehensive execution summary report at the end of the agent run.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/13_logging_and_observability/agent_logger.py
python3 course_0_prerequisites/13_logging_and_observability/trace_context.py
```
