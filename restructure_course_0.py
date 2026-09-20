import os
import shutil
from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/course_0_prerequisites")

# Clean old structure
shutil.rmtree(BASE_DIR, ignore_errors=True)
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Create new structure
dirs = [
    "01_python_for_agents",
    "02_async_python",
    "03_context_and_state",
    "04_http_and_networking",
    "05_configuration_and_secrets",
    "06_processes_and_execution",
    "07_sqlite_and_persistence",
    "08_agent_architecture_prerequisites",
    "09_math_bridges",
    "10_mini_agent",
    "10_mini_agent/tests",
    "exercises",
    "solutions",
    "reference"
]

for d in dirs:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

def write_file(path_str, content):
    with open(BASE_DIR / path_str, "w") as f:
        f.write(content.strip() + "\n")

write_file("README.md", """# Course 0: Prerequisites for AI Agent Engineering

Welcome to the foundation of AI Agent Engineering. This course bridges the gap between basic Python programming and building complex AI-agent runtimes like Hermes. 

This is **not** a generic Python course. Every concept taught here is directly tied to a problem you will face when building an agent.

## How These Prerequisites Appear in an Agent Runtime

* **Callable** -> Tools
* **Async/Await** -> Model + tool execution
* **HTTP** -> Provider APIs
* **JSON** -> Requests / structured data
* **SQLite** -> Persistent state
* **ContextVar** -> Scoped profile/request state
* **Registry** -> Tool/plugin discovery
* **Dependency Injection** -> Runtime construction
* **Subprocess** -> Terminal/code execution
* **Facade** -> Simple public runtime interface
""")

write_file("01_python_for_agents/README.md", """# Module 0.1: Python for Agents (Functions, Classes, Types)

## Key Terminology
| Term      | Meaning                                       | Example              |
| --------- | --------------------------------------------- | -------------------- |
| Callable  | An object that can be invoked like a function | `add(2,3)`           |

## Intuition
```text
function -> stored as an object -> placed in registry -> looked up by name -> called with args
```

## Hermes / Agent Connection
A tool in an AI agent is simply represented as a callable Python function. The LLM predicts the tool name and arguments, and the agent runtime invokes the callable.
""")

write_file("01_python_for_agents/functions.py", """
def add(a: int, b: int) -> int:
    return a + b

tools = {
    "add": add
}

result = tools["add"](2, 3)
print(f"Result: {result}")
""")

write_file("02_async_python/README.md", """# Module 0.2: Async Python

## Key Terminology
| Term      | Meaning                                       | Example              |
| --------- | --------------------------------------------- | -------------------- |
| Coroutine | An async function execution unit              | `fetch_data()`       |

## Mathematical Connection
If three operations take A=2s, B=3s, C=1s:
Sequential: 2+3+1 = 6s
Concurrent approximation: max(2,3,1) = 3s
""")

write_file("02_async_python/async_basics.py", """
import asyncio
import time

async def fetch_data(url: str) -> str:
    await asyncio.sleep(0.1) 
    return f"Data from {url}"

async def main():
    start = time.time()
    results = await asyncio.gather(
        fetch_data("api1"),
        fetch_data("api2"),
        fetch_data("api3")
    )
    end = time.time()
    print(f"Results: {results}, Time taken: {end - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
""")

write_file("03_context_and_state/README.md", """# Module 0.3: Context and State

## Key Terminology
| Term      | Meaning                                       | Example              |
| --------- | --------------------------------------------- | -------------------- |
| Context   | Request/task-local execution state            | `request_id`         |

## Hermes / Agent Connection
```text
Request A
 ├── function
 └── tool
       ↳ request_id = A
```
""")

write_file("03_context_and_state/contextvars_demo.py", """
import contextvars
import asyncio

request_id = contextvars.ContextVar("request_id", default="anonymous")

async def deep_function():
    print(f"Deep function running for request: {request_id.get()}")

async def handle_request(req_id: str):
    token = request_id.set(req_id)
    await asyncio.sleep(0.1)
    await deep_function()
    request_id.reset(token)

async def main():
    await asyncio.gather(
        handle_request("req-123"),
        handle_request("req-456")
    )

if __name__ == "__main__":
    asyncio.run(main())
""")

write_file("04_http_and_networking/README.md", """# Module 0.4: HTTP and Networking

## Key Terminology
| Term      | Meaning                                       | Example              |
| --------- | --------------------------------------------- | -------------------- |
| Endpoint  | A network-accessible API location             | `/v1/models`         |
| Payload   | Data sent with a request                      | JSON body            |

## HTTP Breakdown
```text
POST /v1/chat/completions HTTP/1.1
Host: api.example.com
Authorization: Bearer ...
Content-Type: application/json
```
""")

write_file("04_http_and_networking/api_client.py", """
import json

python_dict = {
    "model": "hermes-v1",
    "messages": [{"role": "user", "content": "Hello"}]
}

json_payload = json.dumps(python_dict)
print(f"JSON Payload: {json_payload}")
""")

write_file("07_sqlite_and_persistence/README.md", """# Module 0.7: SQLite and Persistence
""")

write_file("07_sqlite_and_persistence/message_store.py", """
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, role TEXT, content TEXT)")

role = "user"
content = "Hello, Agent!"
conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
conn.commit()

for row in conn.execute("SELECT * FROM messages"):
    print(row)
""")

write_file("09_math_bridges/README.md", """# Module 0.9: Mathematics Bridges

Connects generic math to AI Agent applications. Read the Level 2/3 math courses, then use this bridge to understand their role in LLMs and agents.

## Bridge 1: Expected Value
`E[X] = Σ x P(x)`
Reinforcement Learning agents (like AlphaGo or MCTS planning agents) choose the action with the highest expected reward.
""")

write_file("10_mini_agent/README.md", """# Module 0.10: Mini Agent""")
write_file("10_mini_agent/agent.py", """
import asyncio
import sqlite3
import subprocess
from typing import Callable, Any

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Callable] = {}
        
    def register(self, name: str, func: Callable):
        self.tools[name] = func
        
    def call(self, name: str, **kwargs) -> Any:
        return self.tools[name](**kwargs)

def math_add(a: int, b: int) -> int:
    return a + b

class MiniAgent:
    def __init__(self, name: str, registry: ToolRegistry):
        self.name = name
        self.registry = registry
        self.db = sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE memory (log TEXT)")
        
    def log(self, message: str):
        self.db.execute("INSERT INTO memory (log) VALUES (?)", (message,))
        self.db.commit()
        
    async def run(self, command: str, **kwargs) -> str:
        self.log(f"Running command: {command}")
        await asyncio.sleep(0.1)
        result = self.registry.call(command, **kwargs)
        return f"[{self.name}] executed {command} -> {result}"

async def main():
    registry = ToolRegistry()
    registry.register("add", math_add)
    agent = MiniAgent("Hermes-Lite", registry)
    print(await agent.run("add", a=5, b=10))

if __name__ == "__main__":
    asyncio.run(main())
""")

print("Course 0 generated.")
