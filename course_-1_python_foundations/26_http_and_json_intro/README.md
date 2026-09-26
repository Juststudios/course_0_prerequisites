# Topic: HTTP and JSON Introduction

## What You Will Learn
In this module, you will learn:
- How the client-server architecture powers the modern internet and API ecosystem.
- The lifecycle of an HTTP Request and Response (Methods, URLs, Headers, Body, and Status Codes).
- The difference between common HTTP methods: `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.
- How HTTP status code classes signal success (`2xx`), redirection (`3xx`), client errors (`4xx`), and server errors (`5xx`).
- What JSON (JavaScript Object Notation) is and why it became the universal data interchange format for software systems.
- How to serialize Python data structures to JSON strings using `json.dumps()` and parse JSON strings back into Python with `json.loads()`.
- How to read and write JSON files directly with `json.dump()` and `json.load()`.
- How to handle non-serializable objects (sets, datetime objects) using custom JSON encoders.
- How to send real HTTP requests using Python's standard library `urllib.request` without external dependencies.
- How autonomous AI agents communicate with LLMs, fetch external knowledge, and invoke API-based tools via HTTP and JSON.

## Prerequisites
Before tackling this module, you should be familiar with:
- Module 06: Collections (Dictionaries, Lists, Tuples, Sets).
- Module 10: Errors and Exception Handling (`try`, `except`, `finally`).
- Module 11: File I/O and Context Managers (`open()`, `with`).

## The Problem
Imagine you build an AI agent written in Python, but you need to query an image generation service written in Go, store chat history in a database written in C++, and prompt an LLM service running in a distant cloud data center.

How can these completely different software systems share complex structured data?
1. If Python sends its internal memory representations (like Python bytecode or `pickle`), the Go service will crash because it cannot understand Python memory structures. Furthermore, `pickle` executes arbitrary code and is a critical security vulnerability.
2. If systems communicate without a standardized protocol, every API would require bespoke networking code, custom port negotiations, and arbitrary error signaling.

The software world solved this through two open standards:
- **HTTP (Hypertext Transfer Protocol)**: A standardized networking protocol for sending requests and receiving responses across the internet.
- **JSON (JavaScript Object Notation)**: A lightweight, human-readable, language-agnostic text format for serializing structured data.

Together, HTTP and JSON form the lingua franca of internet communication and AI agent engineering.

## Key Terminology
- **Client**: The program initiating a network request (e.g., your Python script or AI agent).
- **Server**: The remote program listening for incoming requests, executing logic, and returning responses.
- **HTTP (Hypertext Transfer Protocol)**: The stateless, application-level protocol governing client-server communication over TCP/IP.
- **Endpoint / URL (Uniform Resource Locator)**: The network address where an API resource lives (e.g., `https://api.openai.com/v1/chat/completions`).
- **HTTP Method (Verb)**: The intended action on the resource (`GET` to read, `POST` to create, `PUT`/`PATCH` to update, `DELETE` to remove).
- **HTTP Status Code**: A 3-digit numeric code returned by the server indicating the outcome (e.g., `200 OK`, `404 Not Found`, `500 Internal Server Error`).
- **Headers**: Key-value metadata sent with requests and responses (e.g., `Content-Type: application/json`, `Authorization: Bearer <token>`).
- **JSON (JavaScript Object Notation)**: A text format representing key-value pairs and ordered lists, universally supported by every major programming language.
- **Serialization (Dumping)**: Converting an in-memory Python object (like a dict) into a JSON-formatted string or byte stream.
- **Deserialization (Loading)**: Parsing a JSON string or byte stream back into in-memory Python dictionaries, lists, strings, and numbers.

## Intuition
Think of sending a certified package through postal delivery:
- **The URL** is the destination mailing address.
- **The HTTP Method** is the instruction stamped on the package: `POST` ("deliver new item"), `GET` ("pick up information"), `DELETE` ("return and destroy").
- **The Headers** are the shipping label on the outside of the envelope: the sender's return address, insurance stamps, priority shipping class, and authentication signature.
- **The Body / Payload** is the actual contents inside the package—written in **JSON**, a universal language that any recipient anywhere in the world can read.
- **The HTTP Status Code** is the signed receipt returned to the sender: `200` ("delivered successfully"), `401` ("sender signature invalid"), `404` ("address does not exist"), or `500` ("post office caught fire").

## Concept
### 1. The HTTP Request-Response Lifecycle
1. The **Client** formats an HTTP request containing:
   - Request Line: `POST /v1/chat/completions HTTP/1.1`
   - Headers: `Host: api.example.com`, `Content-Type: application/json`
   - Body: `{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello"}]}`
2. The **Server** processes the request and responds with:
   - Status Line: `HTTP/1.1 200 OK`
   - Headers: `Content-Type: application/json`, `Content-Length: 154`
   - Body: `{"id": "chatcmpl-123", "choices": [{"message": {"content": "Hi there!"}}]}`

### 2. Python <-> JSON Type Mapping
| Python Data Type | JSON Type | Example |
| :--- | :--- | :--- |
| `dict` | Object | `{"key": "value"}` |
| `list`, `tuple` | Array | `[1, 2, "three"]` |
| `str` | String | `"hello world"` |
| `int`, `float` | Number | `42`, `3.14159` |
| `True` / `False` | Boolean | `true` / `false` |
| `None` | Null | `null` |

Notice that JSON keys **must** be double-quoted strings. Python single quotes (`'key'`) are invalid JSON!

## Syntax
### Working with JSON in Python
```python
import json

data = {
    "agent_name": "Scout",
    "version": 1.2,
    "active": True,
    "tools": ["web_search", "python_repl"],
    "metadata": None
}

# 1. Serialize dict to JSON string:
json_string = json.dumps(data, indent=2)

# 2. Deserialize JSON string to dict:
parsed_dict = json.loads(json_string)

# 3. Write directly to a JSON file:
with open("agent_config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# 4. Read directly from a JSON file:
with open("agent_config.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
```

### Making HTTP Requests with `urllib.request` (Standard Library)
```python
import json
import urllib.request
import urllib.error

url = "https://httpbin.org/post"
payload = {"query": "agent architecture", "max_results": 5}
json_bytes = json.dumps(payload).encode("utf-8")

req = urllib.request.Request(
    url,
    data=json_bytes,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "AutonomousAgent/1.0"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        status = response.status
        response_bytes = response.read()
        response_data = json.loads(response_bytes.decode("utf-8"))
        print(f"Status {status}: {response_data}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
except urllib.error.URLError as e:
    print(f"Network Connection Failed: {e.reason}")
```

## Example
Here is a complete, executable Python example demonstrating local JSON serialization, round-trip parsing, custom encoder handling, and building robust HTTP request handlers:

```python
import json
from datetime import datetime
from typing import Any, Dict

class AgentCustomEncoder(json.JSONEncoder):
    """Custom JSON encoder handling datetime and set objects."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return sorted(list(obj))
        return super().default(obj)

def demonstrate_round_trip() -> None:
    agent_state = {
        "id": "agent-409",
        "roles": {"planner", "coder", "reviewer"},
        "created_at": datetime(2026, 9, 21, 12, 0, 0),
        "status": "online",
        "confidence": 0.985
    }

    # Serialize with custom encoder
    serialized = json.dumps(agent_state, cls=AgentCustomEncoder, indent=2)
    print("Serialized JSON string:")
    print(serialized)

    # Deserialize back to Python dictionary
    restored = json.loads(serialized)
    print(f"\nRestored dictionary keys: {list(restored.keys())}")
    print(f"Restored roles type: {type(restored['roles'])} -> {restored['roles']}")

if __name__ == "__main__":
    demonstrate_round_trip()
```

## Line-by-Line Explanation
1. `class AgentCustomEncoder(json.JSONEncoder)`: Subclasses Python's built-in encoder to teach it how to serialize types not natively supported by JSON.
2. `def default(self, obj: Any) -> Any`: Overrides the hook method called whenever `json.dumps()` encounters an unfamiliar object type.
3. `if isinstance(obj, datetime): return obj.isoformat()`: Converts Python `datetime` into an ISO-8601 string (e.g., `"2026-09-21T12:00:00"`).
4. `if isinstance(obj, set): return sorted(list(obj))`: Converts a Python `set` into a deterministic JSON array.
5. `super().default(obj)`: Falls back to the standard encoder for all other types, properly raising `TypeError` if an unknown type cannot be serialized.
6. `json.dumps(agent_state, cls=AgentCustomEncoder, indent=2)`: Encodes the dictionary into a formatted, human-readable JSON string.
7. `restored = json.loads(serialized)`: Parses the JSON string back into a standard Python `dict`.

## What Python Is Doing
When you execute `json.dumps()` and `urllib.request`:
1. **JSON Serialization**: Python traverses your data structure recursively. It inspects object types against its internal type table. If a key is not a string, it converts it or raises a `TypeError`. It builds a UTF-8 character buffer following strict JSON RFC-8259 syntax specifications.
2. **JSON Deserialization**: Python's C-accelerated scanner scans the string, tokenizes brackets, colons, and literals, checks syntax integrity, and instantiates native Python heap objects (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`).
3. **HTTP Networking**:
   - `urllib.request.Request` constructs the raw HTTP/1.1 byte stream according to RFC 9112.
   - It performs a DNS lookup to resolve the hostname to an IP address.
   - It opens an OS socket (TCP handshake on port 80 or TLS handshake on port 443).
   - It sends the request bytes and waits for the server's response stream.
   - It parses status codes and headers, returning an `HTTPResponse` object wrapping the network socket.

## Common Mistakes
1. **Confusing `load`/`dump` with `loads`/`dumps`**:
   - `dumps` (Dump String) / `loads` (Load String): Operates on Python `str` in memory.
   - `dump` / `load`: Operates on open file streams (`with open(...) as f:`).
   Passing a string to `json.load()` produces an `AttributeError: 'str' object has no attribute 'read'`.
2. **Invalid JSON Formatting in String Literals**:
   JSON requires double quotes around keys and strings. Single quotes (`{'name': 'Bob'}`) cause `json.decoder.JSONDecodeError`.
3. **Serializing Unhandled Types**:
   Attempting to serialize a `set`, `tuple` as dict key, or custom class without an encoder raises `TypeError: Object of type set is not JSON serializable`.
4. **Neglecting to Handle HTTP Errors**:
   Assuming `urllib.request.urlopen()` always succeeds. If the server returns 404 or 500, `urllib` raises `urllib.error.HTTPError`. If there is no internet, it raises `urllib.error.URLError`. Always wrap network calls in `try/except`.
5. **Forgetting to Decode Network Bytes**:
   In Python 3, network responses are raw bytes (`bytes`). Passing raw bytes to functions expecting strings without decoding (`response_bytes.decode('utf-8')`) can lead to subtle encoding errors.

## Real-World Uses
- **RESTful Web APIs**: Every modern cloud API (GitHub, Stripe, Weather, Slack) exposes HTTP endpoints accepting and returning JSON.
- **Microservice Communication**: Internal services communicate using lightweight HTTP/JSON or gRPC.
- **Configuration Files**: Software systems, IDE settings (VSCode `settings.json`), and package definitions (`package.json`) use JSON.
- **Client-Side Storage**: Web browsers use JSON for local storage and caching.

## Connection to AI Agents
HTTP and JSON are fundamental to autonomous AI agents:
- **LLM API Calls**: Agents send HTTP `POST` requests with JSON payloads containing prompts, model names, temperature, and conversation history to OpenAI, Anthropic, or local Ollama servers.
- **Tool Calling (Function Calling)**: When an agent uses external tools, the LLM generates a JSON string containing arguments matching the tool's schema (e.g. `{"location": "Tokyo", "unit": "celsius"}`). The agent parses this JSON and runs the corresponding Python function.
- **Structured Output Generation**: AI agents instruct LLMs to output raw JSON so that response data can be validated and stored directly into databases.
- **Agent-to-Agent Protocols**: In multi-agent frameworks, agents pass JSON messages containing sender ID, recipient ID, message type, and context payloads over HTTP webhooks.

## Practice
1. Create a Python dictionary representing an AI agent with fields: `name`, `capabilities` (list), and `uptime_seconds` (int).
2. Convert it to a formatted JSON string using `json.dumps(..., indent=4)`.
3. Parse the string back into a Python dictionary and verify that the types match.
4. Intentionally introduce an invalid single-quoted string and observe the `json.JSONDecodeError`.

## Challenge
Can you build an HTTP request client that posts a JSON query to a simulated endpoint, captures both success and error responses, parses JSON return payloads, and falls back gracefully when given malformed input? (We will build this in `exercises.py`!)

## Summary
- HTTP is the request-response communication protocol of the web; JSON is the data payload format.
- HTTP methods (`GET`, `POST`, etc.) specify intent; status codes (`200`, `404`, `500`) indicate results.
- `json.dumps()` serializes Python data to JSON strings; `json.loads()` parses JSON strings to Python dicts.
- `json.dump()` and `json.load()` read and write directly to file streams.
- AI agents rely on HTTP and JSON for remote LLM inference, structured tool arguments, and inter-agent coordination.

## What You Should Know Before Moving On
- How to serialize and deserialize Python objects to and from JSON using `json.dumps()` and `json.loads()`.
- How to read and write JSON files with `json.load()` and `json.dump()`.
- The significance of common HTTP status codes (`200`, `400`, `401`, `404`, `500`).
- How to build a custom `JSONEncoder` for datetime and set objects.
- How an AI agent uses JSON to receive structured tool parameters from an LLM.
