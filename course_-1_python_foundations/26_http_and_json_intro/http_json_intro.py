"""
Module 26: HTTP and JSON Introduction for Python & AI Agents
============================================================

This lesson covers the fundamentals of HTTP communication and JSON data interchange.

JSON (JavaScript Object Notation) is the ubiquitous data format used by modern
APIs, databases, and LLMs. HTTP (Hypertext Transfer Protocol) is the request-response
networking protocol that connects clients to servers.

Together, HTTP and JSON enable Python applications and autonomous AI agents to:
1. Query remote Large Language Models (LLMs) via REST APIs.
2. Receive and parse structured function-calling parameters.
3. Fetch real-time web telemetry and third-party API data.
4. Serialize and persist agent memory and state configurations.

Sections in this Lesson:
------------------------
1. JSON Fundamentals: Serializing and Deserializing Python Data (`dumps`, `loads`).
2. File-Based JSON Persistence (`dump`, `load`).
3. Handling Complex Types with Custom `JSONEncoder` and `object_hook`.
4. Robust Parsing & Exception Handling with `JSONDecodeError`.
5. HTTP Protocol Mechanics: Anatomy of Requests, Verbs, Headers, and Status Codes.
6. Performing HTTP Requests with Python's Standard Library `urllib.request`.
7. Real-World AI Agent Application: Parsing LLM Tool Call Payloads.
"""

import datetime
import http.server
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Section 1: In-Memory JSON Serialization and Deserialization
# ============================================================================

def demonstrate_json_basics() -> None:
    """
    Demonstrates json.dumps() (serialization) and json.loads() (deserialization).
    """
    print("=" * 70)
    print("1. IN-MEMORY JSON SERIALIZATION & DESERIALIZATION")
    print("=" * 70)

    # Standard Python data structure
    agent_profile = {
        "name": "Nexus-7",
        "model": "gpt-4o",
        "version": 2.1,
        "is_active": True,
        "capabilities": ["code_generation", "web_search", "math_analysis"],
        "max_context_tokens": 128000,
        "temperature": 0.2,
        "fallback_model": None,
    }

    # 1. Serialize to JSON string with pretty indentation and sorted keys
    json_string = json.dumps(agent_profile, indent=2, sort_keys=True)
    print("Serialized JSON String (Human-Readable):")
    print(json_string)

    # 2. Deserialize JSON string back to native Python types
    restored_dict = json.loads(json_string)
    print("\nDeserialized Python Dictionary:")
    print(f"   Agent Name: {restored_dict['name']}")
    print(f"   Capabilities Type: {type(restored_dict['capabilities']).__name__} (count: {len(restored_dict['capabilities'])})")
    print(f"   Fallback Model: {restored_dict['fallback_model']} (Type: {type(restored_dict['fallback_model']).__name__})")
    print(f"   Restored matches original? {restored_dict == agent_profile}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 2: File-Based JSON I/O
# ============================================================================

def demonstrate_file_json_io() -> None:
    """
    Demonstrates json.dump() and json.load() using an in-memory string stream (io.StringIO).
    """
    import io

    print("=" * 70)
    print("2. FILE-BASED JSON PERSISTENCE (dump / load)")
    print("=" * 70)

    config_data = {
        "system_prompt": "You are a helpful software engineering assistant.",
        "timeout_seconds": 30,
        "retry_limit": 3,
        "endpoints": {
            "primary": "https://api.openai.com/v1",
            "fallback": "https://api.anthropic.com/v1"
        }
    }

    # Simulate writing to a file using an in-memory text stream
    stream = io.StringIO()
    json.dump(config_data, stream, indent=4)
    print("Wrote configuration data to text stream.")

    # Rewind stream to the beginning
    stream.seek(0)

    # Read back from stream using json.load()
    loaded_config = json.load(stream)
    print("Loaded configuration from stream:")
    print(f"   Primary Endpoint: {loaded_config['endpoints']['primary']}")
    print(f"   Retry Limit: {loaded_config['retry_limit']}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 3: Handling Non-Standard Types with Custom JSONEncoder
# ============================================================================

class CustomAgentEncoder(json.JSONEncoder):
    """
    Custom JSON encoder extending Python's default encoder to serialize
    sets, datetimes, and custom objects.
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, (set, frozenset)):
            return sorted(list(obj))
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)


class AgentTask:
    """Represents a discrete agent task with metadata."""
    def __init__(self, task_id: str, title: str, tags: set, created_at: datetime.datetime):
        self.task_id = task_id
        self.title = title
        self.tags = tags
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "tags": self.tags,
            "created_at": self.created_at,
        }


def demonstrate_custom_encoder() -> None:
    """
    Demonstrates encoding complex types that standard json.dumps cannot serialize.
    """
    print("=" * 70)
    print("3. CUSTOM JSON ENCODERS FOR COMPLEX TYPES")
    print("=" * 70)

    task = AgentTask(
        task_id="TASK-881",
        title="Audit Security Vulnerabilities",
        tags={"security", "audit", "high_priority"},
        created_at=datetime.datetime(2026, 9, 21, 14, 30, 0),
    )

    # Serialize using CustomAgentEncoder
    serialized_task = json.dumps(task, cls=CustomAgentEncoder, indent=2)
    print("Serialized custom AgentTask object:")
    print(serialized_task)
    print("-" * 70 + "\n")


# ============================================================================
# Section 4: Safe Parsing & JSONDecodeError Handling
# ============================================================================

def safe_parse_json(raw_text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Safely parses potentially malformed JSON text, such as raw LLM output.
    Returns (data, None) on success or (None, error_message) on failure.
    """
    try:
        data = json.loads(raw_text)
        return data, None
    except json.JSONDecodeError as exc:
        error_msg = f"JSONDecodeError at line {exc.lineno}, col {exc.colno}: {exc.msg}"
        return None, error_msg


def demonstrate_safe_parsing() -> None:
    """
    Demonstrates error handling when parsing invalid or malformed JSON.
    """
    print("=" * 70)
    print("4. SAFE JSON PARSING & EXCEPTION RECOVERY")
    print("=" * 70)

    # Valid JSON
    valid_input = '{"status": "ok", "agent_id": "M5"}'
    data, err = safe_parse_json(valid_input)
    print(f"Valid Input Result: {data} (Error: {err})")

    # Malformed JSON (trailing comma, unquoted keys, single quotes)
    malformed_input = "{'status': 'error', 'agent_id': 'M5',}"
    data, err = safe_parse_json(malformed_input)
    print(f"Malformed Input Result: {data}")
    print(f"   -> Caught: {err}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 5 & 6: HTTP Client-Server Mechanics with urllib
# ============================================================================

class MockAPIServer(http.server.BaseHTTPRequestHandler):
    """
    A lightweight, in-process HTTP server simulating a remote API endpoint.
    Handles GET and POST requests with JSON payloads.
    """
    def log_message(self, format: str, *args: Any) -> None:
        # Suppress default server console logging to keep lesson output clean
        pass

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/api/status":
            response_payload = {
                "server_status": "healthy",
                "uptime": 99.99,
                "timestamp": "2026-09-21T15:30:00Z"
            }
            body = json.dumps(response_payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found"}')

    def do_POST(self) -> None:
        if self.path == "/api/agent/dispatch":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            try:
                request_data = json.loads(post_body.decode("utf-8"))
                agent_name = request_data.get("agent_name", "Unknown")
                task = request_data.get("task", "None")

                response_payload = {
                    "status": "dispatched",
                    "execution_id": "EXEC-99201",
                    "assigned_agent": agent_name,
                    "task_summary": task,
                }
                body = json.dumps(response_payload).encode("utf-8")
                self.send_response(201)  # 201 Created
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except json.JSONDecodeError:
                self.send_response(400)  # 400 Bad Request
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON body"}')
        else:
            self.send_response(404)
            self.end_headers()


def demonstrate_http_communication() -> None:
    """
    Demonstrates sending HTTP GET and POST requests using urllib.request
    against an in-memory local mock HTTP server.
    """
    print("=" * 70)
    print("5 & 6. HTTP REQUEST/RESPONSE CYCLE (urllib.request)")
    print("=" * 70)

    # Start local test HTTP server on an OS-assigned ephemeral port (port 0)
    server = http.server.HTTPServer(("127.0.0.1", 0), MockAPIServer)
    port = server.server_address[1]
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    base_url = f"http://127.0.0.1:{port}"
    print(f"Mock HTTP Server running locally on {base_url}")

    # 1. Perform HTTP GET Request
    get_url = f"{base_url}/api/status"
    req_get = urllib.request.Request(get_url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req_get, timeout=5) as response:
        status_code = response.status
        content_type = response.headers.get("Content-Type")
        raw_bytes = response.read()
        parsed_body = json.loads(raw_bytes.decode("utf-8"))
        print(f"\nGET {get_url}:")
        print(f"   Status: {status_code} OK")
        print(f"   Header Content-Type: {content_type}")
        print(f"   Parsed Payload: {parsed_body}")

    # 2. Perform HTTP POST Request with JSON Body
    post_url = f"{base_url}/api/agent/dispatch"
    post_payload = {"agent_name": "Auditor-M5", "task": "Verify milestone compliance"}
    post_bytes = json.dumps(post_payload).encode("utf-8")

    req_post = urllib.request.Request(
        post_url,
        data=post_bytes,
        headers={"Content-Type": "application/json", "User-Agent": "AgentMaster/2.0"},
        method="POST"
    )

    with urllib.request.urlopen(req_post, timeout=5) as response:
        status_code = response.status
        raw_bytes = response.read()
        parsed_body = json.loads(raw_bytes.decode("utf-8"))
        print(f"\nPOST {post_url}:")
        print(f"   Status: {status_code} Created")
        print(f"   Response Payload: {parsed_body}")

    # Shut down mock server cleanly
    server.shutdown()
    server.server_close()
    server_thread.join()
    print("-" * 70 + "\n")


# ============================================================================
# Section 7: AI Agent Tool Call Parsing & Execution
# ============================================================================

def execute_agent_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Dispatches a validated tool invocation to its corresponding handler."""
    if tool_name == "calculator":
        expr = arguments.get("expression", "0")
        # Safe math evaluation for simple arithmetic
        try:
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expr):
                return "Error: Unsupported characters in calculation"
            return f"Result: {eval(expr)}"  # nosec
        except Exception as e:
            return f"Math Error: {e}"
    elif tool_name == "search_knowledge":
        query = arguments.get("query", "")
        return f"Found 3 articles matching '{query}'"
    else:
        return f"Unknown tool: {tool_name}"


def demonstrate_agent_tool_pipeline() -> None:
    """
    Demonstrates how an AI agent processes structured function/tool call JSON
    emitted by an LLM completion.
    """
    print("=" * 70)
    print("7. AI AGENT TOOL CALL PARSER")
    print("=" * 70)

    # Simulated LLM response containing structured tool calls in JSON format
    llm_output_sample = """{
        "id": "call_abc123",
        "type": "function",
        "function": {
            "name": "calculator",
            "arguments": "{\\"expression\\": \\"(15 * 4) + 12\\"}"
        }
    }"""

    # Parse high-level LLM envelope
    envelope = json.loads(llm_output_sample)
    tool_name = envelope["function"]["name"]
    raw_args_string = envelope["function"]["arguments"]

    # Parse nested JSON arguments string
    tool_args = json.loads(raw_args_string)
    print(f"Detected Tool Call: {tool_name}")
    print(f"Parsed Tool Arguments: {tool_args}")

    # Dispatch tool execution
    result = execute_agent_tool(tool_name, tool_args)
    print(f"Tool Execution Output: {result}")
    print("-" * 70 + "\n")


# ============================================================================
# Main Demonstration Runner
# ============================================================================

def main() -> None:
    print("Starting Module 26: HTTP and JSON Introduction\n")
    demonstrate_json_basics()
    demonstrate_file_json_io()
    demonstrate_custom_encoder()
    demonstrate_safe_parsing()
    demonstrate_http_communication()
    demonstrate_agent_tool_pipeline()
    print("Module 26 demonstration completed successfully!")


if __name__ == "__main__":
    main()
