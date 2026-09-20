"""tool_decorator.py - Production-style @tool decorator with schema generation.

Demonstrates:
1. Decorator pattern preserving metadata with @functools.wraps.
2. Automated OpenAI-compatible JSON schema generation from docstrings & annotations.
3. Centralized ToolRegistry pattern for agent execution dispatch.
"""

from typing import Callable, Any, Dict, List, Optional
import functools
import inspect
import json


class ToolRegistry:
    """Central registry mapping tool names to registered callables and their schemas."""

    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._schemas: Dict[str, Dict[str, Any]] = {}

    def register(self, func: Optional[Callable[..., Any]] = None, *, name: Optional[str] = None):
        """Decorator to register a tool callable into this registry."""
        def decorator(target_func: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or target_func.__name__
            schema = self._generate_schema(target_func, tool_name)

            @functools.wraps(target_func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return target_func(*args, **kwargs)

            # Store callable and schema
            self._tools[tool_name] = wrapper
            self._schemas[tool_name] = schema
            wrapper.tool_schema = schema  # type: ignore[attr-defined]
            wrapper.tool_name = tool_name  # type: ignore[attr-defined]
            return wrapper

        if func is None:
            return decorator
        return decorator(func)

    def execute(self, tool_name: str, **arguments: Any) -> Any:
        """Executes a registered tool by name with provided arguments."""
        if tool_name not in self._tools:
            available = list(self._tools.keys())
            raise KeyError(f"Tool '{tool_name}' not found. Available tools: {available}")
        return self._tools[tool_name](**arguments)

    def get_schemas(self) -> List[Dict[str, Any]]:
        """Returns all registered tool schemas formatted for LLM function calling."""
        return list(self._schemas.values())

    def _generate_schema(self, func: Callable[..., Any], tool_name: str) -> Dict[str, Any]:
        """Inspects function signatures and docstrings to create an OpenAI-compatible function schema."""
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or f"Execute {tool_name}"

        # Type mapping from Python primitives to JSON schema types
        type_mapping = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        properties: Dict[str, Any] = {}
        required: List[str] = []

        for param_name, param in sig.parameters.items():
            if param_name in ("self", "cls"):
                continue
            py_type = param.annotation
            json_type = type_mapping.get(py_type, "string")
            properties[param_name] = {
                "type": json_type,
                "description": f"Parameter {param_name}",
            }
            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": doc.split("\n\n")[0],  # First paragraph as description
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }


# Global registry instance
default_registry = ToolRegistry()
tool = default_registry.register


# Example tool definitions
@tool
def fetch_weather(city: str, metric: bool = True) -> str:
    """Fetches the current weather for a specified city.

    Args:
        city: The name of the city.
        metric: Whether to return temperatures in Celsius.
    """
    unit = "Celsius" if metric else "Fahrenheit"
    temp = 21 if metric else 70
    return f"The weather in {city} is currently {temp}° {unit}, Clear Sky."


@tool(name="execute_sql_query")
def run_sql(query: str, limit: int = 10) -> str:
    """Executes a read-only query against the agent analytics database."""
    return f"Simulated execution of: '{query}' with limit {limit}. Returned 2 rows."


def main() -> None:
    print("=== Module 01: Tool Decorator & Registry Demo ===")

    # 1. Verify registered schemas
    schemas = default_registry.get_schemas()
    print(f"Registered {len(schemas)} tools.")
    assert len(schemas) == 2, "Expected 2 registered tools"

    weather_schema = schemas[0]
    assert weather_schema["function"]["name"] == "fetch_weather"
    assert "city" in weather_schema["function"]["parameters"]["properties"]
    assert "city" in weather_schema["function"]["parameters"]["required"]
    assert "metric" not in weather_schema["function"]["parameters"]["required"]

    print("OpenAI-Compatible Tool Schemas:")
    print(json.dumps(schemas, indent=2))

    # 2. Dispatch tool calls through registry
    res1 = default_registry.execute("fetch_weather", city="Berlin", metric=True)
    assert "Berlin" in res1 and "21° Celsius" in res1
    print(f"[OK] Dispatch fetch_weather: {res1}")

    res2 = default_registry.execute("execute_sql_query", query="SELECT * FROM runs", limit=5)
    assert "SELECT * FROM runs" in res2
    print(f"[OK] Dispatch execute_sql_query: {res2}")

    # 3. Verify error handling on unregistered tool
    try:
        default_registry.execute("unknown_tool", query="abc")
        raise AssertionError("Should have raised KeyError")
    except KeyError as err:
        print(f"[OK] Caught expected dispatch error: {err}")

    print("All tool decorator tests passed successfully!\n")


if __name__ == "__main__":
    main()
