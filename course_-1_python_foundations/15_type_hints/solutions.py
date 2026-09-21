"""Module 15 Solutions"""
from typing import Optional, Callable, Any

def double(x: float) -> float:
    return x * 2

def lookup(registry: dict[str, Callable], tool_name: str) -> Optional[Callable]:
    return registry.get(tool_name)

def apply_all(fns: list[Callable[[Any], Any]], value: Any) -> list[Any]:
    return [fn(value) for fn in fns]

def maybe_run(tool: Optional[Callable[[str], Any]], arg: str) -> Optional[Any]:
    if tool is None:
        return None
    return tool(arg)
