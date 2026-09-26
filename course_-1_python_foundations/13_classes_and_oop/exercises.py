"""
Module 13: Classes and Object-Oriented Programming — Exercises
===============================================================
Complete each of the four levels below to master classes, instance state,
dunder methods, encapsulation, and composition in Python.
"""

from typing import Any, Callable, Dict, List, Optional


# =====================================================================
# Level 1: Recall
# =====================================================================
class BankAccount:
    """
    Recall Exercise:
    Classes encapsulate instance state using `self`.
    Implement a simple bank account class:
    - __init__(self, owner: str, initial_balance: float = 0.0):
      Stores `owner` and `balance`.
    - deposit(self, amount: float) -> float:
      Adds amount to balance (if amount > 0) and returns new balance.
    - withdraw(self, amount: float) -> float:
      Subtracts amount from balance if amount <= balance and amount > 0,
      returning new balance. If insufficient funds, raises ValueError("Insufficient funds").

    # TODO: Implement BankAccount class methods.
    """
    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        # TODO: Initialize instance attributes
        raise NotImplementedError("Level 1: Implement BankAccount.__init__().")

    def deposit(self, amount: float) -> float:
        # TODO: Implement deposit
        raise NotImplementedError("Level 1: Implement BankAccount.deposit().")

    def withdraw(self, amount: float) -> float:
        # TODO: Implement withdraw
        raise NotImplementedError("Level 1: Implement BankAccount.withdraw().")


# =====================================================================
# Level 2: Modify
# =====================================================================
class ResettableCounter:
    """
    Modify Exercise:
    Enhance the existing counter implementation:
    1. Add a `decrement(step: int = 1)` method that reduces count by `step`
       (preventing count from going below 0 — clamp at 0).
    2. Add a `reset()` method that sets count back to 0.
    3. Add a `@property` named `is_zero` that returns True if count is 0, else False.

    # TODO: Add decrement, reset, and is_zero property to ResettableCounter.
    """
    def __init__(self, start: int = 0) -> None:
        self.count: int = start

    def increment(self, step: int = 1) -> None:
        self.count += step

    def decrement(self, step: int = 1) -> None:
        # TODO: Decrease count by step, clamping at 0
        raise NotImplementedError("Level 2: Implement ResettableCounter.decrement().")

    def reset(self) -> None:
        # TODO: Reset count to 0
        raise NotImplementedError("Level 2: Implement ResettableCounter.reset().")

    @property
    def is_zero(self) -> bool:
        # TODO: Return True if count is 0, else False
        raise NotImplementedError("Level 2: Implement ResettableCounter.is_zero property.")


# =====================================================================
# Level 3: Build
# =====================================================================
class ToolRegistry:
    """
    Build Exercise:
    Build an OOP ToolRegistry used by an AI Agent:
    - __init__(self): initializes an internal dictionary `self._tools`
    - register(self, name: str, func: Callable[..., Any]) -> None:
      registers a tool by name. If name is empty, raise ValueError.
    - has_tool(self, name: str) -> bool:
      returns True if tool is registered, else False.
    - list_tools(self) -> List[str]:
      returns a sorted list of registered tool names.
    - call(self, name: str, **kwargs: Any) -> Any:
      calls the tool with kwargs. If tool not found, raise KeyError(f"Tool '{name}' not found").
    - __len__(self) -> int:
      returns the number of registered tools.

    # TODO: Implement the full ToolRegistry class.
    """
    def __init__(self) -> None:
        # TODO: Initialize internal registry state
        raise NotImplementedError("Level 3: Implement ToolRegistry.__init__().")

    def register(self, name: str, func: Callable[..., Any]) -> None:
        # TODO: Register tool
        raise NotImplementedError("Level 3: Implement ToolRegistry.register().")

    def has_tool(self, name: str) -> bool:
        # TODO: Check tool presence
        raise NotImplementedError("Level 3: Implement ToolRegistry.has_tool().")

    def list_tools(self) -> List[str]:
        # TODO: Return sorted tool names
        raise NotImplementedError("Level 3: Implement ToolRegistry.list_tools().")

    def call(self, name: str, **kwargs: Any) -> Any:
        # TODO: Dispatch tool call
        raise NotImplementedError("Level 3: Implement ToolRegistry.call().")

    def __len__(self) -> int:
        # TODO: Return tool count
        raise NotImplementedError("Level 3: Implement ToolRegistry.__len__().")


# =====================================================================
# Level 4: Debug
# =====================================================================
class IsolatedAgent:
    """
    Debugging Exercise:
    The following agent class suffers from the classic Python mutable class attribute bug:
    `history = []` was declared at the class level instead of inside `__init__`.
    As a result, appending to one agent's history contaminates ALL other agents!
    Additionally, `agent_count` should be a proper class-level attribute that tracks
    the total number of agent instances created.

    Buggy implementation:
        class IsolatedAgent:
            history = []  # BUG: Shared mutable class attribute!
            agent_count = 0

            def __init__(self, name: str):
                self.name = name
                # BUG: does not increment agent_count on class or isolate history
                self.history = IsolatedAgent.history

            def add_note(self, note: str):
                self.history.append(note)

    # TODO: Fix the class so that each instance has its own isolated `self.history = []`,
    # while `IsolatedAgent.agent_count` properly tracks the total instances instantiated.
    """
    agent_count: int = 0

    def __init__(self, name: str) -> None:
        # TODO: Fix mutable history bug and properly track instance creation count
        raise NotImplementedError("Level 4: Fix bugs in IsolatedAgent class.")

    def add_note(self, note: str) -> None:
        # TODO: Add note to this instance's history
        raise NotImplementedError("Level 4: Implement IsolatedAgent.add_note().")


if __name__ == "__main__":
    print("Module 13 Exercises loaded successfully.")
    print("To test your solutions, implement the functions above or run solutions.py.")
