"""Module 15 Exercises — Type Hints"""
from typing import Optional, Callable, Any

# Level 1: What type hint should go in the blank?
def double(x: ___) -> ___:   # TODO: fill in
    return x * 2

# Level 2: TODO — add correct type hints to this function
def lookup(registry, tool_name):
    return registry.get(tool_name)

# Level 3: TODO — write a function `apply_all` that takes
# a list of Callables and a value, and returns a list of results.
def apply_all(fns, value):
    raise NotImplementedError

# Level 4: TODO — annotate fully with Callable and Optional
def maybe_run(tool, arg):
    if tool is None:
        return None
    return tool(arg)
