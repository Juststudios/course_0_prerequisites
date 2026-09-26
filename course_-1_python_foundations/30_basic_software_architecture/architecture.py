"""
Module 30: Basic Software Architecture
=======================================
A deep-dive tutorial demonstrating core architectural design patterns for Python
applications and autonomous AI agents:
  1. Tight Coupling vs. Loose Coupling
  2. Dependency Injection (DI) & Swappable Storage
  3. The Tool Registry Pattern with Dynamic Introspection
  4. The Adapter Pattern for Legacy Tool Compatibility
  5. The Facade Pattern for Unified Agent Interfaces
  6. An End-to-End Orchestrated Multi-Component System

Architecture is not about writing more code; it is about organizing code so that
each component has one clear responsibility, dependencies are explicit, and testing
is completely frictionless.
"""

from typing import Callable, Any, Protocol, runtime_checkable
import inspect
import time
import json


# =====================================================================
# 1. TIGHT COUPLING VS. LOOSE COUPLING
# =====================================================================
# In a tightly coupled design, a class creates all its own dependencies directly.
# This makes it impossible to unit test without hitting real disks or databases.

class TightlyCoupledAgent:
    """Antipattern: Directly instantiates hardcoded dependencies."""
    def __init__(self):
        # HARDCODED: If this file does not exist or permissions fail, the agent crashes!
        # Moreover, automated unit tests cannot easily intercept these file writes.
        self.log_filename = "agent_monolith.log"
        self.state_db = {}  # Hardcoded in-memory state

    def record_action(self, action: str, result: str) -> None:
        self.state_db[action] = result
        # Direct side effect tied to physical file system
        # (Commented out to prevent pollution during lessons, but shows the trap)
        # with open(self.log_filename, "a") as f: f.write(...)


# =====================================================================
# 2. DEPENDENCY INJECTION & ABSTRACT CONTRACTS
# =====================================================================
# Loose coupling: The agent specifies WHAT it needs via a protocol or interface,
# and the caller INJECTS the actual implementation from the outside.

@runtime_checkable
class StorageBackend(Protocol):
    """Structural protocol defining the contract for any storage engine."""
    def set(self, key: str, value: Any) -> None:
        ...

    def get(self, key: str) -> Any:
        ...

    def has(self, key: str) -> bool:
        ...


class InMemoryStorage:
    """Fast, ephemeral storage backend ideal for unit testing."""
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def has(self, key: str) -> bool:
        return key in self._store

    def dump_all(self) -> dict[str, Any]:
        return dict(self._store)


class JsonFileStorageMock:
    """Simulated file-based storage showing swappability."""
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._buffer: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._buffer[key] = value

    def get(self, key: str) -> Any:
        return self._buffer.get(key)

    def has(self, key: str) -> bool:
        return key in self._buffer


# =====================================================================
# 3. THE TOOL REGISTRY PATTERN
# =====================================================================
# In an AI Agent system, an LLM selects tools by string name (e.g., 'calculator').
# Rather than a fragile 'if tool == "calc": ... elif ...' ladder, a Registry
# stores callables, inspects their parameter signatures, and validates execution.

class ToolRegistry:
    """Central catalog for agent tools supporting dynamic registration & discovery."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}
        self._metadata: dict[str, dict[str, Any]] = {}

    def register(self, name: str, func: Callable[..., Any], description: str = "") -> None:
        """Registers a callable tool and inspects its signature."""
        if not callable(func):
            raise TypeError(f"Tool {name!r} must be callable, got {type(func).__name__}")

        # Extract argument signature for inspection
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        self._tools[name] = func
        self._metadata[name] = {
            "description": description or func.__doc__ or "No description provided.",
            "parameters": param_names,
        }

    def execute(self, name: str, **kwargs) -> Any:
        """Dispatches an execution call to the registered tool."""
        if name not in self._tools:
            raise KeyError(f"Tool {name!r} is not registered. Available: {list(self._tools.keys())}")

        func = self._tools[name]
        return func(**kwargs)

    def list_tools(self) -> dict[str, dict[str, Any]]:
        """Returns a snapshot of all registered tools and their metadata."""
        return dict(self._metadata)


# =====================================================================
# 4. THE ADAPTER PATTERN
# =====================================================================
# Suppose we have a legacy or 3rd-party function that does not match our
# expected keyword-argument calling convention. An Adapter translates between them.

def legacy_tax_service(amount_cents: int, region_code: str) -> int:
    """A legacy function expecting cents and returning integer cents."""
    rate = 0.15 if region_code == "US" else 0.20
    return int(amount_cents * rate)


class TaxServiceAdapter:
    """Adapts legacy_tax_service into standard agent friendly keyword parameters."""
    def __init__(self, service_func: Callable[[int, str], int]):
        self._service = service_func

    def __call__(self, amount: float, region: str = "US") -> float:
        """Translates dollars (float) to cents (int) and back to dollars."""
        amount_cents = int(amount * 100)
        tax_cents = self._service(amount_cents, region)
        return round(tax_cents / 100.0, 2)


# =====================================================================
# 5. THE FACADE PATTERN
# =====================================================================
# A Facade wraps complex internal subsystems (registry, storage, auditing)
# providing a clean, one-stop interface for external consumers.

class AgentFacade:
    """Unified, high-level facade orchestrating tools, memory, and auditing."""

    def __init__(self, registry: ToolRegistry, memory: StorageBackend):
        # Dependencies are injected via the constructor
        self._registry = registry
        self._memory = memory
        self._call_count = 0

    def run_action(self, tool_name: str, **kwargs) -> dict[str, Any]:
        """Executes a tool, stores the result in memory, and returns a structured envelope."""
        self._call_count += 1
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            raw_result = self._registry.execute(tool_name, **kwargs)
            envelope = {
                "status": "success",
                "tool": tool_name,
                "input": kwargs,
                "result": raw_result,
                "timestamp": timestamp,
            }
        except Exception as err:
            envelope = {
                "status": "error",
                "tool": tool_name,
                "input": kwargs,
                "error": f"{type(err).__name__}: {str(err)}",
                "timestamp": timestamp,
            }

        # Persist action record to injected storage
        history_key = f"action_{self._call_count:04d}"
        self._memory.set(history_key, envelope)

        return envelope

    def get_history(self) -> dict[str, Any]:
        """Exposes stored actions without revealing underlying storage mechanisms."""
        if hasattr(self._memory, "dump_all"):
            return self._memory.dump_all()
        return {"note": "Storage backend does not support direct dumping."}


# =====================================================================
# 6. DEMONSTRATION & VERIFICATION PIPELINE
# =====================================================================

def define_sample_tools(registry: ToolRegistry) -> None:
    """Helper populating the registry with sample mathematical and text tools."""

    def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
        """Calculates compound interest: A = P(1 + r)^t"""
        return round(principal * ((1.0 + rate) ** years), 2)

    def format_agent_summary(agent_name: str, tasks_done: int) -> str:
        """Formats a human-readable telemetry summary."""
        return f"Agent {agent_name!r} successfully completed {tasks_done} operational tasks."

    # Direct registration
    registry.register(
        "compound_interest",
        calculate_compound_interest,
        description="Calculates compound growth over time given principal, annual rate, and years."
    )
    registry.register(
        "format_summary",
        format_agent_summary,
        description="Generates a formatted telemetry string for an agent."
    )

    # Registering adapted legacy tool
    tax_adapter = TaxServiceAdapter(legacy_tax_service)
    registry.register(
        "calculate_tax",
        tax_adapter,
        description="Calculates sales tax on dollar amounts using adapted legacy service."
    )


def main() -> None:
    print("=" * 70)
    print("MODULE 30: BASIC SOFTWARE ARCHITECTURE IN ACTION")
    print("=" * 70)

    # Step 1: Initialize decoupled components (Composition Root)
    print("\n[1] Initializing Decoupled Components...")
    registry = ToolRegistry()
    storage = InMemoryStorage()

    # Step 2: Register tools
    print("\n[2] Registering Tools into ToolRegistry...")
    define_sample_tools(registry)

    # Inspect registry catalog
    catalog = registry.list_tools()
    print(f"    Registered {len(catalog)} tools:")
    for name, meta in catalog.items():
        print(f"      - {name:<20} args: {meta['parameters']} | {meta['description']}")

    # Step 3: Instantiate the Facade with Injected Dependencies
    print("\n[3] Creating AgentFacade with Injected Registry & InMemoryStorage...")
    agent = AgentFacade(registry=registry, memory=storage)

    # Step 4: Execute actions through the Facade
    print("\n[4] Executing Actions via AgentFacade...")

    # Action 1: Compound interest calculation
    res1 = agent.run_action("compound_interest", principal=1000.0, rate=0.07, years=5)
    print(f"    Action 1 Output: {json.dumps(res1)}")

    # Action 2: Adapted tax service
    res2 = agent.run_action("calculate_tax", amount=250.50, region="US")
    print(f"    Action 2 Output: {json.dumps(res2)}")

    # Action 3: Text formatting
    res3 = agent.run_action("format_summary", agent_name="Atlas-1", tasks_done=2)
    print(f"    Action 3 Output: {json.dumps(res3)}")

    # Action 4: Intentional failure to demonstrate error handling
    res4 = agent.run_action("unknown_tool", query="hello")
    print(f"    Action 4 (Error Case): {json.dumps(res4)}")

    # Step 5: Verify Persistent State in Injected Storage
    print("\n[5] Inspecting Memory Persistence via Facade...")
    history = agent.get_history()
    print(f"    Total Recorded Actions in Storage: {len(history)}")
    for key, record in history.items():
        print(f"      [{key}] Status: {record['status']:<7} | Tool: {record['tool']}")

    print("\n" + "=" * 70)
    print("ARCHITECTURE SUMMARY:")
    print("  - Registry decoupled tool definitions from execution.")
    print("  - Storage was injected, allowing effortless in-memory testability.")
    print("  - Adapter standardized an incompatible legacy interface.")
    print("  - Facade provided a clean single entry point for all caller requests.")
    print("=" * 70)


if __name__ == "__main__":
    main()
