"""Module 16 Solutions"""
from dataclasses import dataclass, field

@dataclass
class Color:
    r: int; g: int; b: int
    def to_hex(self) -> str:
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

@dataclass
class ToolSpec:
    name: str
    description: str
    tags: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class FrozenToolSpec:
    name: str
    description: str
