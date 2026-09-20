"""trace_context.py - Distributed tracing spans and token cost accounting for AI agents.

Key concepts demonstrated:
1. Hierarchical span management (trace_id, span_id, parent_span_id).
2. Measuring granular execution latencies with high-resolution timers.
3. Token usage accounting and monetary cost estimation.
"""

from typing import List, Dict, Any, Optional
import time
import uuid


class Span:
    """Represents a discrete timed operation in an agent trace."""

    def __init__(self, name: str, trace_id: str, parent_id: Optional[str] = None) -> None:
        self.span_id = str(uuid.uuid4())[:8]
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.name = name
        self.start_time: float = 0.0
        self.duration_ms: float = 0.0
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.metadata: Dict[str, Any] = {}

    def __enter__(self) -> "Span":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        self.duration_ms = (time.perf_counter() - self.start_time) * 1000.0
        self.metadata["error"] = str(exc_val) if exc_val else None
        return False

    def record_tokens(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens


class AgentTraceRecorder:
    """Records and aggregates spans and token metrics across an agent request."""

    def __init__(self, trace_id: Optional[str] = None) -> None:
        self.trace_id = trace_id or str(uuid.uuid4())[:12]
        self.spans: List[Span] = []
        self._span_stack: List[str] = []

    def start_span(self, name: str) -> Span:
        parent_id = self._span_stack[-1] if self._span_stack else None
        span = Span(name, self.trace_id, parent_id)
        self.spans.append(span)
        return span

    def span(self, name: str):
        """Context manager creating and pushing a span onto the hierarchy stack."""
        tracer = self

        class SpanContext:
            def __enter__(self):
                self.s = tracer.start_span(name)
                tracer._span_stack.append(self.s.span_id)
                self.s.__enter__()
                return self.s

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.s.__exit__(exc_type, exc_val, exc_tb)
                tracer._span_stack.pop()
                return False

        return SpanContext()

    def get_summary(self) -> Dict[str, Any]:
        """Calculates total latency, token usage, and dollar costs."""
        total_in = sum(s.input_tokens for s in self.spans)
        total_out = sum(s.output_tokens for s in self.spans)
        total_duration = sum(s.duration_ms for s in self.spans)

        # Standard pricing estimate ($0.0015 / 1k input, $0.002 / 1k output)
        cost_usd = (total_in / 1000.0 * 0.0015) + (total_out / 1000.0 * 0.002)

        return {
            "trace_id": self.trace_id,
            "total_spans": len(self.spans),
            "total_duration_ms": round(total_duration, 2),
            "total_input_tokens": total_in,
            "total_output_tokens": total_out,
            "estimated_cost_usd": round(cost_usd, 6),
            "spans": [
                {
                    "name": s.name,
                    "span_id": s.span_id,
                    "parent_id": s.parent_id,
                    "duration_ms": round(s.duration_ms, 2),
                    "tokens": s.input_tokens + s.output_tokens
                }
                for s in self.spans
            ]
        }


def main() -> None:
    print("=== Module 13: Distributed Trace Context & Token Accounting Demo ===")

    recorder = AgentTraceRecorder("trace_test_root_101")

    # Simulate an agent reasoning step with nested spans
    with recorder.span("root_step") as root_span:
        time.sleep(0.01)

        # Child span: LLM reasoning
        with recorder.span("llm_reasoning") as llm_span:
            time.sleep(0.02)
            llm_span.record_tokens(input_tokens=150, output_tokens=35)

        # Child span: Tool dispatch
        with recorder.span("execute_tool_calculator") as tool_span:
            time.sleep(0.01)

    summary = recorder.get_summary()

    # Assertions
    assert summary["trace_id"] == "trace_test_root_101"
    assert summary["total_spans"] == 3
    assert summary["total_input_tokens"] == 150
    assert summary["total_output_tokens"] == 35
    assert summary["estimated_cost_usd"] > 0.0

    # Verify hierarchy
    spans = summary["spans"]
    root = spans[0]
    llm = spans[1]
    tool = spans[2]

    assert root["parent_id"] is None
    assert llm["parent_id"] == root["span_id"]
    assert tool["parent_id"] == root["span_id"]

    print("[OK] Span hierarchy correctly linked child spans to parent span.")
    print(f"[OK] Token accounting verified: {summary['total_input_tokens']} in, {summary['total_output_tokens']} out.")
    print(f"[OK] Estimated cost: ${summary['estimated_cost_usd']}")
    print("All tests in trace_context.py passed successfully!\n")


if __name__ == "__main__":
    main()
