# Module 33: Integrated Projects

## Project 7 — Mini Agent Skeleton
This is your bridge into Course 0. It demonstrates:

| Concept | Where Used |
|---------|-----------|
| Dataclass | `AgentConfig` |
| Classes | `ToolRegistry`, `Memory`, `Agent` |
| Type Hints | Throughout |
| Async/Await | `Agent.run()` |
| JSON | Input/output serialization |
| SQLite | `Memory.save()` and history |
| Logging | `logger.info/error` |
| Exceptions | Graceful error handling |
| Registry pattern | `ToolRegistry` |
| Dependency Injection | `Agent.__init__` receives its deps |

## How to Run
```bash
python3 mini_agent.py
```

## What's Next
In Course 0, you will learn:
- How the HTTP client replaces the JSON string input
- How ContextVars scopes state per request
- How async HTTP calls replace `asyncio.sleep`
- How a real tool registry handles schemas and validation
