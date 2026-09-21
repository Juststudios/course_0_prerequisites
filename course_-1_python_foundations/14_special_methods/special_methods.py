"""
Module 14: Special Methods (Dunder Methods)

TERM: Special Method / Dunder Method
DEFINITION: Methods with double-underscore names (__init__, __str__, __call__)
            that Python invokes automatically in response to built-in operations.
INTUITION: They let your objects "speak Python" — behave like built-in types.
"""

class Tool:
    """A callable tool object."""

    def __init__(self, name: str, func):
        self.name = name
        self._func = func

    def __str__(self) -> str:
        """Called by str() and print()."""
        return f"Tool({self.name!r})"

    def __repr__(self) -> str:
        """Called in the REPL and for debugging."""
        return f"Tool(name={self.name!r})"

    def __call__(self, *args, **kwargs):
        """Makes the object callable: tool(2, 3)  ← works!"""
        print(f"  [Tool:{self.name}] called")
        return self._func(*args, **kwargs)

    def __len__(self) -> int:
        """len(tool) → length of the name (just for demo)."""
        return len(self.name)


add_tool = Tool("add", lambda a, b: a + b)

print(str(add_tool))        # __str__
print(repr(add_tool))       # __repr__
print(add_tool(3, 4))       # __call__  ← 7
print(len(add_tool))        # __len__   ← 3 (length of "add")

# ── Why __call__ matters for agents ─────────────────────────────────────────
# An agent runtime stores tools in a registry.
# Any callable works — a plain function OR a class with __call__.
# This flexibility is why "callable" is more general than "function."
registry = {"add": add_tool}
result = registry["add"](10, 20)
print(f"Via registry: {result}")
