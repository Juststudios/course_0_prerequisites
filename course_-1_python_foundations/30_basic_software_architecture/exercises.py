"""
Module 30 Exercises: Basic Software Architecture
=================================================
Practice applying core software architecture patterns:
  - Level 1: Recall (The Registry Pattern)
  - Level 2: Modify (Refactoring Tight Coupling to Dependency Injection)
  - Level 3: Build (Audited Agent Facade with Multi-Component Orchestration)
  - Level 4: Debug (Fixing Mutable Default Arguments & Validation Traps)
"""

from typing import Callable, Any, Protocol


# =====================================================================
# LEVEL 1: RECALL — Simple Tool Registry
# =====================================================================
# Task: Implement a SimpleRegistry class that maps string names to callables.
# Requirements:
#   1. register(name: str, func: Callable) -> None: Store the callable under 'name'.
#      Raise TypeError if func is not callable.
#   2. get(name: str) -> Callable: Return the callable associated with 'name'.
#      Raise KeyError if 'name' is not registered.
#   3. has(name: str) -> bool: Return True if 'name' exists in the registry, else False.
#   4. list_tools() -> list[str]: Return a sorted list of all registered tool names.

class SimpleRegistry:
    """A minimal callable registry."""
    def __init__(self) -> None:
        # TODO: Initialize internal storage dictionary
        raise NotImplementedError("Level 1: Initialize SimpleRegistry internal storage")

    def register(self, name: str, func: Callable[..., Any]) -> None:
        """Register a function under the given name."""
        # TODO: Validate that func is callable (raise TypeError if not), then store
        raise NotImplementedError("Level 1: Implement register()")

    def get(self, name: str) -> Callable[..., Any]:
        """Retrieve the function registered under name."""
        # TODO: Return the function or raise KeyError if missing
        raise NotImplementedError("Level 1: Implement get()")

    def has(self, name: str) -> bool:
        """Check if a tool name is registered."""
        # TODO: Return True if name is in registry, else False
        raise NotImplementedError("Level 1: Implement has()")

    def list_tools(self) -> list[str]:
        """Return a sorted list of registered tool names."""
        # TODO: Return sorted list of names
        raise NotImplementedError("Level 1: Implement list_tools()")


# =====================================================================
# LEVEL 2: MODIFY — Refactoring Tight Coupling to Dependency Injection
# =====================================================================
# Task: Modify the DataProcessor class below.
# Current problem: DataProcessor currently instantiates its own hardcoded writer
# inside __init__, making it tightly coupled and difficult to test with mocks.
#
# Requirements:
#   1. Modify __init__ to accept an optional 'writer' dependency. If not provided,
#      default to an instance of DefaultConsoleWriter.
#   2. In process_record(), pass the formatted record to self.writer.write(record).
#   3. Ensure any custom writer implementing a write(dict) method can be injected!

class DefaultConsoleWriter:
    """Writes formatted messages to an internal log."""
    def __init__(self) -> None:
        self.logs: list[str] = []

    def write(self, record: dict[str, Any]) -> None:
        msg = f"[LOG] {record.get('user')}: {record.get('action')}"
        self.logs.append(msg)


class DataProcessor:
    """Tightly coupled processor that needs refactoring to Dependency Injection."""
    def __init__(self) -> None:
        # TIGHT COUPLING BUG: Hardcoded instantiation
        # TODO: Modify this constructor to accept writer as an injected dependency!
        self.writer = DefaultConsoleWriter()
        raise NotImplementedError("Level 2: Refactor __init__ to support Dependency Injection")

    def process(self, user: str, action: str) -> dict[str, Any]:
        record = {"user": user, "action": action, "processed": True}
        # TODO: Use self.writer to write the record
        raise NotImplementedError("Level 2: Implement process() with injected writer")


# =====================================================================
# LEVEL 3: BUILD — Audited Agent Facade
# =====================================================================
# Task: Build an AuditedAgentFacade class that ties together a SimpleRegistry
# and an audit log list using Dependency Injection.
#
# Requirements:
#   1. __init__(self, registry: SimpleRegistry, audit_log: list[dict[str, Any]])
#   2. execute(self, tool_name: str, **kwargs) -> dict[str, Any]:
#      - If tool is found in registry:
#          Call tool(**kwargs)
#          Append entry to audit_log:
#            {"tool": tool_name, "status": "success", "result": result}
#          Return {"success": True, "result": result}
#      - If tool raises an exception or is not found:
#          Append entry to audit_log:
#            {"tool": tool_name, "status": "error", "error": str(exception)}
#          Return {"success": False, "error": str(exception)}

class AuditedAgentFacade:
    """Coordinates tool execution and audit logging."""
    def __init__(self, registry: SimpleRegistry, audit_log: list[dict[str, Any]]) -> None:
        # TODO: Store injected registry and audit_log
        raise NotImplementedError("Level 3: Implement AuditedAgentFacade.__init__")

    def execute(self, tool_name: str, **kwargs) -> dict[str, Any]:
        # TODO: Coordinate execution, audit log entry, and error safety
        raise NotImplementedError("Level 3: Implement AuditedAgentFacade.execute")


# =====================================================================
# LEVEL 4: DEBUG — Fixing Mutable Default Arguments & Validation Traps
# =====================================================================
# Task: Debug and repair the BuggyPluginManager class below.
#
# Bugs present in the original code:
#   Bug 1: Default argument plugins={} is mutable, causing instances to share state!
#   Bug 2: register() does not verify if the plugin has an 'execute' method or is callable.
#   Bug 3: execute_plugin() crashes with AttributeError if plugin is not found
#          instead of raising a descriptive KeyError.

class BuggyPluginManager:
    """Contains multiple architectural and Pythonic bugs to identify and fix."""
    def __init__(self, plugins: dict = {}) -> None:  # BUG: Mutable default argument!
        self.plugins = plugins

    def register(self, name: str, plugin: Any) -> None:
        # BUG: Missing validation
        self.plugins[name] = plugin

    def execute_plugin(self, name: str, *args, **kwargs) -> Any:
        # BUG: Crashes with AttributeError or KeyError silently
        plugin = self.plugins[name]
        return plugin.execute(*args, **kwargs)


class RepairedPluginManager:
    """The corrected, production-ready implementation."""
    def __init__(self, plugins: dict[str, Any] | None = None) -> None:
        # TODO: Fix mutable default argument by initializing an independent dictionary
        raise NotImplementedError("Level 4: Fix mutable default argument in RepairedPluginManager")

    def register(self, name: str, plugin: Any) -> None:
        """Registers a plugin, validating that it possesses an execute() method or is callable."""
        # TODO: Validate that plugin has 'execute' method or is callable, else raise TypeError
        raise NotImplementedError("Level 4: Implement robust register validation")

    def execute_plugin(self, name: str, *args, **kwargs) -> Any:
        """Executes the plugin safely, handling both objects with .execute and bare callables."""
        # TODO: Safely retrieve and execute, raising KeyError if name is missing
        raise NotImplementedError("Level 4: Implement safe execute_plugin")
