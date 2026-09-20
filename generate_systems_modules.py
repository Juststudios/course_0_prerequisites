from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/course_0_prerequisites")
def write_file(path_str, content):
    p = BASE_DIR / path_str
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        f.write(content.strip() + "\n")

# --- 05 HTTP AND JSON ---
write_file("05_http_and_apis/README.md", """
# Module 0.7 & 0.8: HTTP, APIs, and JSON

## Terminology
* **Client:** The program making the request.
* **Server:** The program returning the response.
* **Endpoint:** The URL where the API lives.
* **Payload:** The JSON data sent in the request body.

## Intuition
```text
Client -> Network -> Server
```

## HTTP Mathematics / Networking Reasoning
* **Latency:** Time required for a request/response round trip.
* **Throughput:** Amount of data/work completed per unit time.
* **Timeouts:** Connect timeout (TCP handshake), read timeout (waiting for first byte), total timeout.

## Agent Connection
Agents communicate with LLMs (like OpenAI/Anthropic) using HTTP POST requests containing JSON payloads.
```text
Python object -> JSON -> HTTP Request -> HTTP Response -> JSON -> Python object
```
""")

write_file("05_http_and_apis/api_client.py", """
import json

# Simulated payload
python_dict = {
    "model": "hermes-v1",
    "messages": [{"role": "user", "content": "Hello"}]
}

# Convert Python to JSON string
json_payload = json.dumps(python_dict)
print(f"JSON Payload (String): {json_payload}")

# Convert JSON string back to Python
parsed_dict = json.loads(json_payload)
print(f"Parsed back to Python dict: {parsed_dict['model']}")

# Agent Note: When using `httpx`, you can just pass `json=python_dict`
# and it automatically handles the json.dumps and Content-Type headers!
""")

# --- 06 CONFIGURATION ---
write_file("06_configuration/README.md", """
# Module 0.9: Configuration and Environment Variables

## Terminology
* **Environment Variable:** Variables passed to the process by the OS.
* **Secret:** Sensitive configuration (like API keys) that should never be in source code.

## Agent Connection
Agents need configuration (which LLM to use) and secrets (API keys). Hardcoding these is dangerous.
""")

# --- 07 SUBPROCESSES ---
write_file("07_subprocesses/README.md", """
# Module 0.10: Subprocesses

## Terminology
* **Process:** A running program.
* **Standard Output (stdout):** Where normal prints go.
* **Standard Error (stderr):** Where errors go.

## Agent Connection
```text
Agent -> Tool -> Child process -> Program -> stdout/stderr -> Agent
```
Agents often run external code (like Python interpreters or shell scripts) via subprocesses as tools.
""")

write_file("07_subprocesses/subprocess_basics.py", """
import subprocess

# Run a simple echo command in a child process
try:
    result = subprocess.run(
        ["echo", "Hello from child process!"], 
        capture_output=True, 
        text=True,
        timeout=5.0
    )
    print(f"stdout: {result.stdout.strip()}")
    print(f"Return code: {result.returncode}")
except subprocess.TimeoutExpired:
    print("The subprocess took too long and was killed.")
""")

# --- 08 SQLITE ---
write_file("08_sqlite/README.md", """
# Module 0.11: SQLite

## Terminology
* **Database / Table / Row / Column:** Relational data structures.
* **Primary Key:** Unique identifier for a row.
* **Parameterized SQL:** Safe way to pass variables into SQL.

## Mathematical / Data Concept - Relational Data
```text
Table
 ↓
Rows = records
Columns = attributes
```

## Agent Connection
Agents need to remember past conversations. A local SQLite database is the perfect lightweight memory store.
""")

write_file("08_sqlite/sqlite_basics.py", """
import sqlite3

# Connect to in-memory database
conn = sqlite3.connect(":memory:")

# Create table
conn.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, role TEXT, content TEXT)")

# Use parameterized SQL (?) to prevent SQL injection attacks!
role = "user"
content = "Hello, Agent!"
conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
conn.commit()

# Retrieve
for row in conn.execute("SELECT * FROM messages"):
    print(row)
""")

# --- 09 ARCHITECTURE ---
write_file("09_software_architecture/README.md", """
# Module 0.12: Software Architecture

## Terminology
* **Facade:** A simpler interface over complicated internals.
* **Registry:** A central mapping of names to components.
* **Dependency Injection:** Dependencies are supplied from outside rather than hardcoded.

## Agent Connection
Agents are complex. If you don't use DI and Registries, your agent code will become unmaintainable spaghetti. 

```python
# Dependency Injection Example:
agent = Agent(
    model=model_instance,
    tools=tool_registry,
    memory=sqlite_memory,
)
```
""")

print("Systems modules generated.")
