"""
Module 13: Classes and Object-Oriented Programming — Reference Solutions
=========================================================================
Clean, production-grade solutions for all four exercise tiers.
"""

from typing import Any, Callable, Dict, List, Optional


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
class BankAccount:
    """
    Encapsulates bank account balance state with deposit and withdraw rules.
    """
    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner: str = owner
        self.balance: float = max(0.0, initial_balance)

    def deposit(self, amount: float) -> float:
        if amount > 0:
            self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            return self.balance
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
class ResettableCounter:
    """
    Enhanced counter supporting increment, decrement (clamped at 0), reset,
    and an is_zero property.
    """
    def __init__(self, start: int = 0) -> None:
        self.count: int = max(0, start)

    def increment(self, step: int = 1) -> None:
        self.count += step

    def decrement(self, step: int = 1) -> None:
        self.count = max(0, self.count - step)

    def reset(self) -> None:
        self.count = 0

    @property
    def is_zero(self) -> bool:
        return self.count == 0


# =====================================================================
# Level 3: Build Solution
# =====================================================================
class ToolRegistry:
    """
    Tool registry providing registration, introspection, and dispatch.
    """
    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        if not name or not name.strip():
            raise ValueError("Tool name cannot be empty")
        self._tools[name.strip()] = func

    def has_tool(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> List[str]:
        return sorted(self._tools.keys())

    def call(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found")
        return self._tools[name](**kwargs)

    def __len__(self) -> int:
        return len(self._tools)


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
class IsolatedAgent:
    """
    Fixed agent with properly isolated instance history and class-level instance counter.
    """
    agent_count: int = 0  # Class attribute tracking instances created

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.history: List[str] = []  # Unique to each instance!
        IsolatedAgent.agent_count += 1

    def add_note(self, note: str) -> None:
        self.history.append(note)


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    acct = BankAccount("Alice", 100.0)
    assert acct.balance == 100.0, "Level 1 initial balance failed"
    assert acct.deposit(50.0) == 150.0, "Level 1 deposit failed"
    assert acct.withdraw(70.0) == 80.0, "Level 1 withdraw failed"
    try:
        acct.withdraw(1000.0)
        assert False, "Level 1 did not raise ValueError on overdraft"
    except ValueError as err:
        assert "Insufficient funds" in str(err)

    # Test Level 2
    ctr = ResettableCounter(5)
    assert ctr.is_zero is False, "Level 2 is_zero initial failed"
    ctr.decrement(3)
    assert ctr.count == 2, "Level 2 decrement failed"
    ctr.decrement(10)
    assert ctr.count == 0 and ctr.is_zero is True, "Level 2 clamp at 0 failed"
    ctr.increment(4)
    ctr.reset()
    assert ctr.count == 0 and ctr.is_zero is True, "Level 2 reset failed"

    # Test Level 3
    registry = ToolRegistry()
    assert len(registry) == 0, "Level 3 initial len failed"
    registry.register("add", lambda a, b: a + b)
    registry.register("mul", lambda a, b: a * b)
    assert len(registry) == 2, "Level 3 len after register failed"
    assert registry.has_tool("add") is True, "Level 3 has_tool failed"
    assert registry.list_tools() == ["add", "mul"], "Level 3 list_tools failed"
    assert registry.call("add", a=10, b=5) == 15, "Level 3 call add failed"
    assert registry.call("mul", a=3, b=4) == 12, "Level 3 call mul failed"
    try:
        registry.call("missing_tool")
        assert False, "Level 3 did not raise KeyError on missing tool"
    except KeyError as err:
        assert "not found" in str(err)

    # Test Level 4
    # Reset count before test
    IsolatedAgent.agent_count = 0
    a1 = IsolatedAgent("Agent-1")
    a2 = IsolatedAgent("Agent-2")
    assert IsolatedAgent.agent_count == 2, f"Level 4 agent_count failed: {IsolatedAgent.agent_count}"
    a1.add_note("Note for Agent 1")
    assert len(a1.history) == 1, "Level 4 a1 history failed"
    assert len(a2.history) == 0, "Level 4 a2 history leaked from a1!"

    print("Module 13: All Level 1-4 solutions verified successfully!")
