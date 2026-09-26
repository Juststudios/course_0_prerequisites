"""
Module 30 Solutions: Basic Software Architecture
=================================================
Reference implementations for all 4 levels of Module 30 exercises.
"""

from typing import Callable, Any


# =====================================================================
# LEVEL 1: RECALL — Simple Tool Registry Solution
# =====================================================================

class SimpleRegistry:
    """A minimal callable registry."""
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        """Register a function under the given name."""
        if not callable(func):
            raise TypeError(f"Tool {name!r} must be callable, got {type(func).__name__}")
        self._tools[name] = func

    def get(self, name: str) -> Callable[..., Any]:
        """Retrieve the function registered under name."""
        if name not in self._tools:
            raise KeyError(f"Tool {name!r} is not registered")
        return self._tools[name]

    def has(self, name: str) -> bool:
        """Check if a tool name is registered."""
        return name in self._tools

    def list_tools(self) -> list[str]:
        """Return a sorted list of registered tool names."""
        return sorted(self._tools.keys())


# =====================================================================
# LEVEL 2: MODIFY — Dependency Injection Solution
# =====================================================================

class DefaultConsoleWriter:
    """Writes formatted messages to an internal log."""
    def __init__(self) -> None:
        self.logs: list[str] = []

    def write(self, record: dict[str, Any]) -> None:
        msg = f"[LOG] {record.get('user')}: {record.get('action')}"
        self.logs.append(msg)


class DataProcessor:
    """Refactored processor utilizing Dependency Injection for its writer."""
    def __init__(self, writer: Any | None = None) -> None:
        # Dependency Injection: Accept external writer or fall back to default
        if writer is None:
            self.writer = DefaultConsoleWriter()
        else:
            self.writer = writer

    def process(self, user: str, action: str) -> dict[str, Any]:
        record = {"user": user, "action": action, "processed": True}
        self.writer.write(record)
        return record


# =====================================================================
# LEVEL 3: BUILD — Audited Agent Facade Solution
# =====================================================================

class AuditedAgentFacade:
    """Coordinates tool execution and audit logging."""
    def __init__(self, registry: SimpleRegistry, audit_log: list[dict[str, Any]]) -> None:
        self._registry = registry
        self._audit_log = audit_log

    def execute(self, tool_name: str, **kwargs) -> dict[str, Any]:
        try:
            func = self._registry.get(tool_name)
            result = func(**kwargs)
            log_entry = {
                "tool": tool_name,
                "status": "success",
                "result": result
            }
            self._audit_log.append(log_entry)
            return {"success": True, "result": result}
        except Exception as exc:
            log_entry = {
                "tool": tool_name,
                "status": "error",
                "error": str(exc)
            }
            self._audit_log.append(log_entry)
            return {"success": False, "error": str(exc)}


# =====================================================================
# LEVEL 4: DEBUG — Repaired Plugin Manager Solution
# =====================================================================

class RepairedPluginManager:
    """The corrected, production-ready implementation."""
    def __init__(self, plugins: dict[str, Any] | None = None) -> None:
        # Avoid mutable default argument bug by initializing a new dictionary
        if plugins is None:
            self._plugins: dict[str, Any] = {}
        else:
            self._plugins = dict(plugins)

    def register(self, name: str, plugin: Any) -> None:
        """Registers a plugin, validating that it possesses an execute() method or is callable."""
        has_exec_method = hasattr(plugin, "execute") and callable(getattr(plugin, "execute"))
        is_callable = callable(plugin)

        if not (has_exec_method or is_callable):
            raise TypeError(
                f"Plugin {name!r} must be callable or define an execute() method, got {type(plugin).__name__}"
            )
        self._plugins[name] = plugin

    def execute_plugin(self, name: str, *args, **kwargs) -> Any:
        """Executes the plugin safely, handling both objects with .execute and bare callables."""
        if name not in self._plugins:
            raise KeyError(f"Plugin {name!r} not found in manager")

        plugin = self._plugins[name]
        if hasattr(plugin, "execute") and callable(getattr(plugin, "execute")):
            return plugin.execute(*args, **kwargs)
        return plugin(*args, **kwargs)


# =====================================================================
# VERIFICATION RUNNER
# =====================================================================

def verify_module_30() -> None:
    print("Verifying Module 30 Solutions...")

    # Test Level 1: SimpleRegistry
    reg = SimpleRegistry()
    reg.register("greet", lambda name: f"Hello, {name}!")
    reg.register("add", lambda a, b: a + b)
    assert reg.has("greet") is True
    assert reg.has("missing") is False
    assert reg.get("greet")(name="World") == "Hello, World!"
    assert reg.list_tools() == ["add", "greet"]
    try:
        reg.register("bad_tool", "not_a_function")  # type: ignore
        assert False, "Should have raised TypeError"
    except TypeError:
        pass
    print("  [✓] Level 1 (Recall) passed!")

    # Test Level 2: DataProcessor with Dependency Injection
    # Case A: Default writer
    dp_default = DataProcessor()
    rec1 = dp_default.process("alice", "login")
    assert rec1["processed"] is True
    assert len(dp_default.writer.logs) == 1

    # Case B: Injected custom mock writer
    class MockWriter:
        def __init__(self):
            self.records = []
        def write(self, record):
            self.records.append(record)

    mock = MockWriter()
    dp_injected = DataProcessor(writer=mock)
    dp_injected.process("bob", "query_database")
    assert len(mock.records) == 1
    assert mock.records[0]["user"] == "bob"
    print("  [✓] Level 2 (Modify) passed!")

    # Test Level 3: AuditedAgentFacade
    audit_trail: list[dict[str, Any]] = []
    facade = AuditedAgentFacade(registry=reg, audit_log=audit_trail)

    # Success call
    res_ok = facade.execute("add", a=10, b=25)
    assert res_ok["success"] is True
    assert res_ok["result"] == 35
    assert len(audit_trail) == 1
    assert audit_trail[0]["status"] == "success"

    # Error call (missing tool)
    res_err = facade.execute("non_existent_tool")
    assert res_err["success"] is False
    assert len(audit_trail) == 2
    assert audit_trail[1]["status"] == "error"
    print("  [✓] Level 3 (Build) passed!")

    # Test Level 4: RepairedPluginManager
    mgr1 = RepairedPluginManager()
    mgr2 = RepairedPluginManager()

    # Verify no state bleeding between instances (mutable default bug fix)
    mgr1.register("callable_tool", lambda x: x * 2)
    assert "callable_tool" not in mgr2._plugins

    # Verify class with .execute()
    class CustomPlugin:
        def execute(self, val: int) -> int:
            return val + 100

    mgr1.register("obj_tool", CustomPlugin())
    assert mgr1.execute_plugin("callable_tool", 5) == 10
    assert mgr1.execute_plugin("obj_tool", 5) == 105

    # Verify TypeError on invalid plugin
    try:
        mgr1.register("bad", 12345)
        assert False, "Should have rejected integer plugin"
    except TypeError:
        pass

    # Verify KeyError on missing plugin
    try:
        mgr1.execute_plugin("unknown")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass
    print("  [✓] Level 4 (Debug) passed!")

    print("All Module 30 solutions verified successfully!\n")


if __name__ == "__main__":
    verify_module_30()
