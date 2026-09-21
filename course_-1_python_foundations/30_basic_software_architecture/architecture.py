"""Module 30: Basic Software Architecture"""

# ── Registry Pattern ─────────────────────────────────────────────────────────
class Registry:
    """Maps names to callables."""
    def __init__(self):
        self._items: dict = {}
    def register(self, name: str, impl):
        self._items[name] = impl
    def get(self, name: str):
        return self._items.get(name)

# ── Facade Pattern ───────────────────────────────────────────────────────────
class AgentFacade:
    """Simple public interface hiding internal complexity."""
    def __init__(self, registry: Registry):
        self._registry = registry
    def run(self, tool_name: str, **kwargs):
        tool = self._registry.get(tool_name)
        if not tool:
            return {"error": f"Unknown tool: {tool_name}"}
        return {"result": tool(**kwargs)}

# ── Dependency Injection ─────────────────────────────────────────────────────
# Instead of creating dependencies inside a class (tight coupling),
# pass them in from outside (loose coupling → easier to test).

class Agent:
    def __init__(self, registry: Registry, facade: AgentFacade):
        self.registry = registry   # injected
        self.facade   = facade     # injected

# Demo:
reg = Registry()
reg.register("add", lambda a, b: a + b)
facade = AgentFacade(reg)
agent  = Agent(reg, facade)

print(agent.facade.run("add", a=3, b=4))
print(agent.facade.run("unknown_tool"))
print("\nArchitecture lesson complete. Course 0 expands all these patterns.")
