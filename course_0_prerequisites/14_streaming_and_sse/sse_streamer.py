"""sse_streamer.py - Demonstrates Server-Sent Events (SSE) and tool argument delta accumulation.

Key concepts demonstrated:
1. Generating standard SSE event frames (event: delta, data: {...}\n\n).
2. Streaming consumer parsing data payloads from an SSE stream.
3. Stitching fragmented tool arguments together across multiple deltas.
"""

from typing import AsyncGenerator, Dict, Any, List
import asyncio
import json


async def mock_sse_llm_stream() -> AsyncGenerator[str, None]:
    """Simulates an LLM API emitting Server-Sent Events with thought and tool argument chunks."""
    events = [
        {"type": "thought_delta", "text": "I should compute "},
        {"type": "thought_delta", "text": "the factorial of 5. "},
        {"type": "tool_start", "name": "calculator"},
        {"type": "argument_delta", "chunk": '{"expr'},
        {"type": "argument_delta", "chunk": 'ession": '},
        {"type": "argument_delta", "chunk": '"5 * 4 * '},
        {"type": "argument_delta", "chunk": '3 * 2 * 1"}'},
        {"type": "tool_done"},
        {"type": "finish_reason", "reason": "tool_calls"}
    ]

    for ev in events:
        await asyncio.sleep(0.01)
        # Format as standard SSE block
        yield f"event: agent_event\ndata: {json.dumps(ev)}\n\n"


class SSEEventParser:
    """Consumes an SSE stream and aggregates streaming fragments."""

    def __init__(self) -> None:
        self.thoughts: List[str] = []
        self.active_tool_name: str | None = None
        self.tool_arg_buffer: str = ""
        self.completed_tool_calls: List[Dict[str, Any]] = []

    async def consume(self, sse_stream: AsyncGenerator[str, None]) -> None:
        async for chunk in sse_stream:
            for line in chunk.splitlines():
                line = line.strip()
                if line.startswith("data: "):
                    payload = json.loads(line[len("data: "):])
                    self._handle_payload(payload)

    def _handle_payload(self, payload: Dict[str, Any]) -> None:
        p_type = payload.get("type")
        if p_type == "thought_delta":
            self.thoughts.append(payload["text"])
        elif p_type == "tool_start":
            self.active_tool_name = payload["name"]
            self.tool_arg_buffer = ""
        elif p_type == "argument_delta":
            self.tool_arg_buffer += payload["chunk"]
        elif p_type == "tool_done":
            if self.active_tool_name:
                parsed_args = json.loads(self.tool_arg_buffer)
                self.completed_tool_calls.append({
                    "tool": self.active_tool_name,
                    "arguments": parsed_args
                })
                self.active_tool_name = None
                self.tool_arg_buffer = ""


async def main() -> None:
    print("=== Module 14: Server-Sent Events & Delta Accumulator Demo ===")

    parser = SSEEventParser()
    await parser.consume(mock_sse_llm_stream())

    # Assertions
    full_thought = "".join(parser.thoughts)
    assert full_thought == "I should compute the factorial of 5. "
    print(f"[OK] Reconstructed streamed thoughts: '{full_thought}'")

    assert len(parser.completed_tool_calls) == 1
    tool_call = parser.completed_tool_calls[0]
    assert tool_call["tool"] == "calculator"
    assert tool_call["arguments"]["expression"] == "5 * 4 * 3 * 2 * 1"
    print(f"[OK] Reconstructed tool call from streaming argument chunks: {tool_call}")

    # Evaluate calculation
    result = eval(tool_call["arguments"]["expression"])
    assert result == 120
    print(f"[OK] Evaluated reconstructed tool expression: 5! = {result}")

    print("All tests in sse_streamer.py passed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
