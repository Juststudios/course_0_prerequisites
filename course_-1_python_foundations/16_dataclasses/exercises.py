"""Module 16 Exercises"""
from dataclasses import dataclass, field

# Level 1: What does this print?
@dataclass
class Color:
    r: int; g: int; b: int
print(Color(255, 0, 0))

# Level 2: TODO — add a method `to_hex()` that returns "#RRGGBB"
# (use f"{self.r:02X}")

# Level 3: TODO — create a ToolSpec dataclass with fields:
#   name: str, description: str, tags: list[str]
# then create two ToolSpec instances.
class ToolSpec:
    raise NotImplementedError

# Level 4: TODO — make ToolSpec frozen so it can be used as a dict key.
