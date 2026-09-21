"""
Module 33: Integrated Project — Mini Agent Skeleton

This project demonstrates every concept from Modules 1-32 working together.
It is intentionally simple — the goal is ARCHITECTURE, not intelligence.

Flow:
  User Input (JSON string)
      ↓
  Agent.run(input_json)
      ↓
  JSON parsing
      ↓
  ToolRegistry.call(tool_name, **kwargs)
      ↓
  Result
      ↓
  Persistence (SQLite)
      ↓
  JSON response
"""
import json, sqlite3, logging, asyncio
from dataclasses import dataclass
from typing import Callable, Any, Optional

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("mini_agent")

# ── Configuration ────────────────────────────────────────────────────────────
@dataclass
class AgentConfig:
    name: str = "Hermes-Lite"
    db_path: str = ":memory:"

# ── Tool Registry ────────────────────────────────────────────────────────────
class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        self._tools[name] = func
        logger.info(f"Registered tool: {name!r}")

    def call(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name!r}")
        return self._tools[name](**kwargs)

# ── Memory / Persistence ─────────────────────────────────────────────────────
class Memory:
    def __init__(self, db_path: str):
        self._conn = sqlite3.connect(db_path)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                tool    TEXT,
                result  TEXT
            )
        """)
        self._conn.commit()

    def save(self, tool: str, result: Any) -> None:
        self._conn.execute(
            "INSERT INTO history (tool, result) VALUES (?, ?)",
            (tool, str(result))
        )
        self._conn.commit()

    def all(self) -> list[tuple]:
        return self._conn.execute("SELECT * FROM history").fetchall()

# ── Agent ────────────────────────────────────────────────────────────────────
class Agent:
    def __init__(self, config: AgentConfig, registry: ToolRegistry, memory: Memory):
        self.config   = config
        self.registry = registry
        self.memory   = memory

    async def run(self, input_json: str) -> str:
        try:
            req = json.loads(input_json)
            tool_name: str = req["tool"]
            kwargs: dict   = req.get("args", {})
        except (json.JSONDecodeError, KeyError) as e:
            return json.dumps({"error": f"Invalid request: {e}"})

        try:
            result = self.registry.call(tool_name, **kwargs)
            self.memory.save(tool_name, result)
            return json.dumps({"result": result})
        except KeyError as e:
            return json.dumps({"error": str(e)})
        except Exception as e:
            logger.error(f"Tool {tool_name!r} failed: {e}")
            return json.dumps({"error": str(e)})

# ── Tool definitions ─────────────────────────────────────────────────────────
def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b

def echo(message: str) -> str:
    return message

# ── Main ─────────────────────────────────────────────────────────────────────
async def main():
    config   = AgentConfig()
    registry = ToolRegistry()
    memory   = Memory(config.db_path)

    registry.register("add",      add)
    registry.register("multiply", multiply)
    registry.register("echo",     echo)

    agent = Agent(config, registry, memory)

    requests = [
        '{"tool": "add",      "args": {"a": 5, "b": 3}}',
        '{"tool": "multiply", "args": {"a": 4, "b": 7}}',
        '{"tool": "echo",     "args": {"message": "Hello from Hermes-Lite!"}}',
        '{"tool": "unknown"}',
        'INVALID JSON',
    ]

    print(f"\n=== {config.name} ===")
    for req in requests:
        response = await agent.run(req)
        print(f"  {req[:50]:<50} → {response}")

    print(f"\nHistory ({len(memory.all())} entries):")
    for row in memory.all():
        print(f"  {row}")

if __name__ == "__main__":
    asyncio.run(main())
