"""dependency_injection.py - Demonstrates Dependency Injection (DI) and Inversion of Control for AI agents.

Key concepts demonstrated:
1. Protocol/interface-based component injection (Model, Memory, ToolRegistry).
2. Assembling production vs testing agent configurations without modifying agent core.
3. Hermetic unit testing using injected mocks.
"""

from typing import Protocol, List, Dict, Any
from dataclasses import dataclass, field


# 1. Component Interfaces (Protocols)
class ModelProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class MemoryBackend(Protocol):
    def store(self, key: str, value: str) -> None:
        ...

    def retrieve(self, key: str) -> str | None:
        ...


class ToolDispatcher(Protocol):
    def dispatch(self, tool_name: str, **kwargs: Any) -> str:
        ...


# 2. Concrete Implementations
class MockModelProvider:
    def __init__(self, canned_response: str = "Mock answer") -> None:
        self.canned_response = canned_response
        self.call_count = 0

    def generate(self, prompt: str) -> str:
        self.call_count += 1
        return self.canned_response


class InMemoryMemoryBackend:
    def __init__(self) -> None:
        self._data: Dict[str, str] = {}

    def store(self, key: str, value: str) -> None:
        self._data[key] = value

    def retrieve(self, key: str) -> str | None:
        return self._data.get(key)


class SimpleToolDispatcher:
    def dispatch(self, tool_name: str, **kwargs: Any) -> str:
        if tool_name == "calculator":
            return str(eval(kwargs.get("expr", "0"), {"__builtins__": None}, {}))
        return f"Tool {tool_name} executed"


# 3. Agent Core receiving injected dependencies
class ModularAgent:
    """Agent core decoupled from specific providers via Dependency Injection."""

    def __init__(
        self,
        model: ModelProvider,
        memory: MemoryBackend,
        tools: ToolDispatcher,
        agent_name: str = "ModularAgent"
    ) -> None:
        self.model = model
        self.memory = memory
        self.tools = tools
        self.agent_name = agent_name

    def run_step(self, user_query: str) -> str:
        # Save query to memory
        self.memory.store("last_query", user_query)
        # Call model
        plan = self.model.generate(user_query)
        # Execute tool if required
        if "calc:" in plan:
            expr = plan.split("calc:")[1].strip()
            tool_output = self.tools.dispatch("calculator", expr=expr)
            self.memory.store("last_result", tool_output)
            return f"Answer: {tool_output}"

        self.memory.store("last_result", plan)
        return plan


def main() -> None:
    print("=== Module 11: Dependency Injection Demo ===")

    # Setup test components
    mock_model = MockModelProvider("calc: 10 + 32")
    memory = InMemoryMemoryBackend()
    tools = SimpleToolDispatcher()

    # Inject into agent
    agent = ModularAgent(
        model=mock_model,
        memory=memory,
        tools=tools,
        agent_name="TestAgent"
    )

    # Execute step
    output = agent.run_step("Compute 10 + 32")

    # Verify output and memory
    assert output == "Answer: 42"
    assert mock_model.call_count == 1
    assert memory.retrieve("last_query") == "Compute 10 + 32"
    assert memory.retrieve("last_result") == "42"

    print(f"[OK] Agent executed step via injected components: {output}")
    print(f"[OK] Memory verified: last_result={memory.retrieve('last_result')}")
    print("All tests in dependency_injection.py passed successfully!\n")


if __name__ == "__main__":
    main()
