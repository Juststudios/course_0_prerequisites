"""
Module 13: Classes and Object-Oriented Programming

TERM: Class
DEFINITION: A blueprint for creating objects that have shared attributes and behaviour.
TERM: Object / Instance
DEFINITION: A concrete thing created from a class blueprint.
INTUITION: A class is like a cookie cutter; each cookie you cut is an object.
WHY IT EXISTS: To group related data and behaviour together, and to create
               multiple independent copies of a thing.
"""

# ── Step 1: Simplest possible class ─────────────────────────────────────────
class Dog:
    def __init__(self, name: str, breed: str):
        self.name = name     # attribute — belongs to this instance
        self.breed = breed

    def speak(self) -> str:
        return f"{self.name} says: Woof!"

fido = Dog("Fido", "Labrador")
rex  = Dog("Rex",  "German Shepherd")
print(fido.speak())
print(rex.speak())
print(f"fido is not rex: {fido is not rex}")   # True — independent objects

# ── Step 2: A more realistic Agent-like class ────────────────────────────────
class SimpleAgent:
    """A minimal agent that dispatches requests to registered tools."""

    def __init__(self, name: str):
        self.name = name
        self._tools: dict = {}          # private by convention (_prefix)
        self._history: list = []

    def register_tool(self, tool_name: str, func) -> None:
        self._tools[tool_name] = func

    def run(self, tool_name: str, **kwargs):
        if tool_name not in self._tools:
            raise KeyError(f"Unknown tool: {tool_name!r}")
        result = self._tools[tool_name](**kwargs)
        self._history.append({"tool": tool_name, "result": result})
        return result

    def history(self) -> list:
        return list(self._history)   # return a copy


def add(a, b):
    return a + b

agent = SimpleAgent("Hermes-Lite")
agent.register_tool("add", add)
print(f"\n{agent.name} computed: {agent.run('add', a=5, b=3)}")
print(f"History: {agent.history()}")

# ── Step 3: Inheritance ──────────────────────────────────────────────────────
class LoggingAgent(SimpleAgent):
    """Same as SimpleAgent but prints every tool call."""
    def run(self, tool_name: str, **kwargs):
        print(f"  [LOG] Calling {tool_name!r} with {kwargs}")
        return super().run(tool_name, **kwargs)

la = LoggingAgent("Verbose-Agent")
la.register_tool("add", add)
la.run("add", a=10, b=20)

# ── Composition vs Inheritance ───────────────────────────────────────────────
# Prefer composition ("has-a") over inheritance ("is-a") for flexibility.
# Agent HAS-A ToolRegistry  ← better
# Agent IS-A ToolRegistry   ← fragile
print("\nClasses lesson complete.")
