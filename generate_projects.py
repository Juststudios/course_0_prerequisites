from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/course_0_prerequisites")
def write_file(path_str, content):
    p = BASE_DIR / path_str
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        f.write(content.strip() + "\n")

# --- INTEGRATED PRACTICE (MINI AGENT) ---
write_file("projects/mini_agent/README.md", """
# Module 0.15: Mini Agent Prerequisite Project

## Minimal Tool-Capable Agent Skeleton

This is NOT a real LLM agent. It is a skeleton demonstrating how the software architecture, Python concepts (Classes, Callables, Async), and systems (SQLite, Subprocesses) wire together.

```text
User Input -> Agent Object -> Tool Registry -> Tool Selection -> Tool Execution -> Result -> Response
```
""")

write_file("projects/mini_agent/agent_skeleton.py", """
import asyncio
import sqlite3
import subprocess
from typing import Callable, Any

# 1. TOOL REGISTRY
class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Callable] = {}
        
    def register(self, name: str, func: Callable):
        self.tools[name] = func
        
    def call(self, name: str, **kwargs) -> Any:
        if name not in self.tools:
            return f"Error: Tool {name} not found."
        try:
            return self.tools[name](**kwargs)
        except Exception as e:
            return f"Error executing {name}: {e}"

# 2. SOME TOOLS (Callables)
def math_add(a: int, b: int) -> int:
    return a + b

def run_shell(cmd: str) -> str:
    # Subprocess execution
    try:
        res = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=2.0)
        return res.stdout.strip()
    except Exception as e:
        return str(e)

# 3. AGENT CLASS (Dependency Injection)
class MiniAgent:
    def __init__(self, name: str, registry: ToolRegistry):
        self.name = name
        self.registry = registry
        # SQLite Memory
        self.db = sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE memory (log TEXT)")
        
    def log(self, message: str):
        self.db.execute("INSERT INTO memory (log) VALUES (?)", (message,))
        self.db.commit()
        
    async def run(self, command: str, **kwargs) -> str:
        self.log(f"Running command: {command} with args: {kwargs}")
        
        # Simulated async delay
        await asyncio.sleep(0.1)
        
        # Execute tool
        result = self.registry.call(command, **kwargs)
        
        self.log(f"Result: {result}")
        return f"[{self.name}] executed {command} -> {result}"

# 4. EXECUTION
async def main():
    registry = ToolRegistry()
    registry.register("add", math_add)
    registry.register("shell", run_shell)
    
    agent = MiniAgent("Hermes-Lite", registry)
    
    # Concurrent execution using asyncio
    results = await asyncio.gather(
        agent.run("add", a=5, b=10),
        agent.run("shell", cmd="echo Hello_World")
    )
    
    for r in results:
        print(r)

if __name__ == "__main__":
    asyncio.run(main())
""")

# --- ASSESSMENTS ---
write_file("assessments/README.md", """
# Course 0 Final Assessment

## Terminology
Define the following terms in your own words:
1. Callable
2. Coroutine
3. ContextVar
4. Dependency Injection

## Code Reading
Explain what this snippet does:
```python
async def fetch_all(urls):
    return await asyncio.gather(*(fetch(u) for u in urls))
```

## Mathematics
Calculate the Expected Value for a tool that succeeds (value=10) with 80% probability, and fails (value=0) with 20% probability.

## Architecture
Identify the architectural pattern here:
```python
tools = {"search": web_search, "calc": calculator}
```
""")

print("Projects and Assessments generated.")
