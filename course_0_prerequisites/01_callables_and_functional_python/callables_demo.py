"""callables_demo.py - Demonstrates callables, closures, and introspection for AI agents.

Concepts demonstrated:
1. Standard function callables vs. lambda expressions.
2. Stateful callable classes implementing __call__.
3. Closures capturing parameterized runtime configuration.
4. Programmatic signature introspection using `inspect`.
"""

from typing import Callable, Any, Dict
import inspect


def basic_calculator(operation: str, x: float, y: float) -> float:
    """Performs a mathematical operation on two float operands."""
    if operation == "add":
        return x + y
    elif operation == "sub":
        return x - y
    elif operation == "mul":
        return x * y
    elif operation == "div":
        if y == 0:
            raise ZeroDivisionError("Division by zero in calculator tool.")
        return x / y
    else:
        raise ValueError(f"Unsupported operation: {operation}")


class StatefulSearchTool:
    """A callable class that preserves search count state and query history."""

    def __init__(self, search_domain: str):
        self.search_domain = search_domain
        self.call_history: list[str] = []

    def __call__(self, query: str) -> str:
        """Executes a simulated search within the configured domain."""
        self.call_history.append(query)
        return (
            f"Found 3 articles in [{self.search_domain}] for query '{query}'. "
            f"Total queries so far: {len(self.call_history)}"
        )


def make_scoped_rate_limiter(max_calls: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Closure demonstrating state encapsulation for agent tool rate limiting."""
    calls_remaining = max_calls

    def rate_limiter_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        def inner(*args: Any, **kwargs: Any) -> Any:
            nonlocal calls_remaining
            if calls_remaining <= 0:
                raise RuntimeError(f"Rate limit exceeded: {func.__name__} allowed only {max_calls} invocations.")
            calls_remaining -= 1
            return func(*args, **kwargs)

        return inner

    return rate_limiter_wrapper


def introspect_callable(func: Callable[..., Any]) -> Dict[str, Any]:
    """Inspects a callable and returns a clean dictionary description for LLM tools."""
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or "No documentation provided."

    parameters = {}
    for name, param in sig.parameters.items():
        parameters[name] = {
            "type": param.annotation.__name__ if hasattr(param.annotation, "__name__") else str(param.annotation),
            "default": None if param.default is inspect.Parameter.empty else param.default,
            "required": param.default is inspect.Parameter.empty,
        }

    return {
        "name": getattr(func, "__name__", type(func).__name__),
        "description": doc,
        "parameters": parameters,
        "return_type": sig.return_annotation.__name__ if hasattr(sig.return_annotation, "__name__") else str(sig.return_annotation),
    }


def main() -> None:
    print("=== Module 01: Callables & Functional Python Demo ===")

    # 1. Test basic function callable
    assert callable(basic_calculator), "basic_calculator must be callable"
    calc_res = basic_calculator("add", 15.0, 27.0)
    assert calc_res == 42.0, f"Expected 42.0, got {calc_res}"
    print(f"[OK] basic_calculator('add', 15.0, 27.0) = {calc_res}")

    # 2. Test stateful class callable
    search_tool = StatefulSearchTool("engineering_docs")
    assert callable(search_tool), "search_tool instance must be callable"
    res1 = search_tool("python async")
    res2 = search_tool("contextvars")
    assert len(search_tool.call_history) == 2
    assert "Total queries so far: 2" in res2
    print(f"[OK] StatefulSearchTool history: {search_tool.call_history}")

    # 3. Test closure rate limiter
    limiter = make_scoped_rate_limiter(max_calls=2)

    def simple_action(x: int) -> int:
        return x * 2

    limited_action = limiter(simple_action)
    assert limited_action(5) == 10
    assert limited_action(10) == 20
    try:
        limited_action(15)
        raise AssertionError("Rate limit should have triggered!")
    except RuntimeError as err:
        print(f"[OK] Caught expected rate limit: {err}")

    # 4. Test introspection
    meta = introspect_callable(basic_calculator)
    assert meta["name"] == "basic_calculator"
    assert "operation" in meta["parameters"]
    assert meta["parameters"]["operation"]["required"] is True
    print(f"[OK] Introspected basic_calculator parameters: {list(meta['parameters'].keys())}")
    print("All assertions passed cleanly!\n")


if __name__ == "__main__":
    main()
