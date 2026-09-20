# Module 14: Streaming, Generators, and Server-Sent Events (SSE)

## 1. Learning Objectives
By the end of this module, you will be able to:
- Contrast synchronous generator functions with asynchronous generators (`async def ... yield`).
- Iterate over live token streams using `async for` loops.
- Explain and implement the Server-Sent Events (SSE) text protocol (`event:`, `data:`, `\n\n`).
- Emulate real-time token streaming interfaces with simulated model inference latency.
- Accumulate and stitch together fragmented tool call argument chunks emitted across streaming deltas into complete, valid JSON payloads.

---

## 2. Why AI Agent Engineers Need This
Generating a complete multi-paragraph reasoning trajectory or tool call with a large language model can take anywhere from 5 to 30 seconds.
- If an agent uses a non-streaming interface, the end user stares at a frozen screen or spinner with zero feedback, wondering if the service has crashed.
- With **streaming**, tokens appear on the user's screen within 200 milliseconds of generation, creating a responsive and engaging user experience.

However, streaming introduces unique engineering challenges for agents:
- Tool calls are not delivered as a single monolithic JSON object; they arrive as dozens of tiny streaming fragments (e.g. `{"arg`, `ument`, `s": "{"expr`, `": "1+1"}`).
- The agent runtime must simultaneously stream human-readable thoughts to the user while buffering and assembling tool call delta fragments into valid JSON before invoking tools.

---

## 3. Structured Concept Breakdown

### Concept 1: Asynchronous Generators
- **TERM**: Asynchronous Generator
- **DEFINITION**: A coroutine function that produces a sequence of values lazily over time using the `yield` statement, iterated asynchronously with `async for`.
- **INTUITION**: A conveyor belt that unloads one package at a time whenever the receiver is ready, pausing when waiting for new packages from the warehouse.
- **WHY IT EXISTS**: A regular function must compute all results and return a complete list in memory (`return all_tokens`). Asynchronous generators allow an LLM client to deliver each token the exact millisecond it is sampled from the neural network.
- **HOW IT WORKS**: When `yield item` is executed inside an `async def` function, execution pauses and control returns to the consumer's `async for` loop. When the loop asks for the next item (`__anext__()`), execution resumes immediately after the `yield`.
- **CODE**:
```python
import asyncio
from typing import AsyncGenerator

async def stream_tokens(text: str) -> AsyncGenerator[str, None]:
    for word in text.split():
        await asyncio.sleep(0.05)  # Simulated model latency
        yield word + " "
```

---

### Concept 2: Server-Sent Events (SSE) Protocol
- **TERM**: Server-Sent Events (SSE)
- **DEFINITION**: A lightweight, unidirectional HTTP streaming protocol defined by W3C where the server pushes UTF-8 text events formatted with `data:` lines terminated by double newlines (`\n\n`).
- **INTUITION**: A live ticker tape in a stock exchange. The tape continuously spews out printed text updates without the client needing to ask for each individual price.
- **WHY IT EXISTS**: WebSockets are bidirectional and heavy (requiring protocol upgrades, custom proxies). SSE works over standard HTTP/1.1 or HTTP/2 GET/POST connections with automatic reconnection and built-in text framing.
- **HOW IT WORKS**: The server sends headers: `Content-Type: text/event-stream` and `Cache-Control: no-cache`. Each event chunk adheres to:
  ```http
  event: delta
  data: {"content": "Hello"}

  ```
  The double newline `\n\n` signals the end of the event frame.
- **CODE**:
```python
def format_sse_event(data: dict, event_type: str = "message") -> str:
    import json
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
```

---

### Concept 3: Streaming Delta Accumulation
- **TERM**: Delta Accumulation
- **DEFINITION**: Buffering and concatenating sequential fragments (deltas) of tool call names and argument strings until the stream signals completion (`finish_reason: "tool_calls"`).
- **INTUITION**: Assembling a jigsaw puzzle as pieces arrive in the mail one by one. You cannot solve or use the puzzle until all pieces are snapped into place.
- **WHY IT EXISTS**: LLMs stream tool arguments as raw string chunks:
  - Chunk 1: `{"expression": `
  - Chunk 2: `"15 * `
  - Chunk 3: `4"}`
  Parsing any single chunk with `json.loads` will crash with `JSONDecodeError`. The runtime must accumulate all chunks into a complete string buffer.
- **HOW IT WORKS**: The runtime initializes `buffer = ""`. For each delta, `buffer += delta.arguments`. When `finish_reason == "tool_calls"`, the complete `buffer` is passed to `json.loads()`.
- **CODE**:
```python
class ToolCallAccumulator:
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.argument_buffer = ""

    def append_chunk(self, chunk: str):
        self.argument_buffer += chunk

    def finalize(self) -> dict:
        import json
        return json.loads(self.argument_buffer)
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Parsing Incomplete Streaming Chunks as JSON
- **The Bug**: Calling `json.loads(chunk)` on individual streaming token deltas.
- **The Consequence**: Every streaming chunk throws a `JSONDecodeError`, crashing the streaming listener.
- **The Fix**: Accumulate fragments into a string buffer; parse only upon stream completion.

### Anti-Pattern 2: Unbuffered Network Flushes
- **The Bug**: Emitting SSE tokens without flushing or disabling HTTP response buffering in intermediate proxies (e.g. Nginx).
- **The Consequence**: Nginx buffers the entire response until all 500 tokens have finished generating, completely negating the benefit of streaming for the end user.
- **The Fix**: Include the header `X-Accel-Buffering: no` in SSE responses to force reverse proxies to immediately forward chunks.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What character sequence marks the end of an SSE message block?
2. Which keyword is used to iterate over an asynchronous generator in Python?
3. What MIME type is required in the `Content-Type` header for an SSE endpoint?

### Tier 2 (Debugging)
Find the flaw in this streaming consumer:
```python
async def consume_stream(stream_gen):
    full_text = ""
    for token in stream_gen:  # What is the syntax error here?
        full_text += token
    return full_text
```
*Hint*: `stream_gen` is an async generator; you must use `async for token in stream_gen:`.

### Tier 3 (Application)
Write an async generator `sse_parser(raw_sse_lines: AsyncGenerator[str, None])` that buffers incoming lines, extracts the payload after `data: `, and yields parsed JSON objects whenever a double newline is encountered.

### Tier 4 (Challenge)
Build a `StreamingReActAgent` interface:
- Streams `<thought>` tokens live to the console.
- Buffers `<action>` JSON fragments silently in the background.
- Once the action buffer is complete, executes the tool and streams the tool observation.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/14_streaming_and_sse/async_token_stream.py
python3 course_0_prerequisites/14_streaming_and_sse/sse_streamer.py
```
