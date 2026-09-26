"""
Module 16: Python Dataclasses — Exercises
==========================================
Complete each of the four levels below to master dataclasses, field configuration,
mutable default factories, immutability, and post-init validation.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
# Recall Exercise:
# Create an RGBColor dataclass with:
#   r: int, g: int, b: int
# And a method `to_hex(self) -> str` that formats the color as an uppercase hex string:
#   e.g. RGBColor(255, 0, 128).to_hex() -> "#FF0080"
# (Use format specifier :02X for each channel).

# TODO: Define RGBColor dataclass with r, g, b and to_hex()
@dataclass
class RGBColor:
    r: int
    g: int
    b: int

    def to_hex(self) -> str:
        # TODO: Implement to_hex returning #RRGGBB format
        raise NotImplementedError("Level 1: Implement RGBColor.to_hex().")


# =====================================================================
# Level 2: Modify
# =====================================================================
# Modify Exercise:
# In an AI Agent configuration dataclass, enforce domain rules using `__post_init__`:
# 1. `model_name`: str (must not be empty string or all whitespace; raise ValueError if empty)
# 2. `temperature`: float = 0.7 (must be between 0.0 and 2.0 inclusive; raise ValueError if outside)
# 3. `max_tokens`: int = 2048 (must be strictly positive; raise ValueError if <= 0)
# 4. `tags`: List[str] = field(default_factory=list) (must use default_factory!)

@dataclass
class ValidatedAgentConfig:
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 2048
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # TODO: Add validation rules for model_name, temperature, and max_tokens
        raise NotImplementedError("Level 2: Implement ValidatedAgentConfig.__post_init__().")


# =====================================================================
# Level 3: Build
# =====================================================================
# Build Exercise:
# Build an immutable, hashable tool definition dataclass for an agent catalog:
# Class: FrozenToolSpec
# Settings: frozen=True
# Fields:
#   - name: str
#   - category: str
#   - timeout_sec: float = 30.0
#   - permissions: Tuple[str, ...] = field(default_factory=tuple)
#
# Methods:
#   - summary(self) -> str: returns f"[{self.category.upper()}] {self.name} ({self.timeout_sec}s)"
#
# Because it is frozen and contains only hashable fields, it must be usable
# as a dictionary key or in a set!

# TODO: Implement the FrozenToolSpec dataclass
class FrozenToolSpec:
    # TODO: Decorate with @dataclass(frozen=True) and declare typed fields and summary()
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("Level 3: Implement FrozenToolSpec with frozen=True.")


# =====================================================================
# Level 4: Debug
# =====================================================================
# Debugging Exercise:
# The dataclass below attempts to track an agent's memory state, but contains two bugs:
#   1. BUG: `memory: List[str] = []` causes a ValueError in Python because mutable
#      defaults cannot be instantiated directly in dataclasses!
#   2. BUG: `api_key: str` was placed AFTER fields with defaults, which violates Python's
#      field ordering rules (non-default fields must come before default fields).
#
# Fix the class definition so it compiles, uses field(default_factory=list),
# and correctly orders all attributes.

# TODO: Fix the bugs in AgentSessionState so it instantiates cleanly
@dataclass
class AgentSessionState:
    # TODO: Fix field ordering and mutable default factory
    session_id: str
    # BUG: api_key should be before defaults or given a default
    # BUG: memory must use default_factory=list
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("Level 4: Fix AgentSessionState definition.")


if __name__ == "__main__":
    print("Module 16 Exercises loaded successfully.")
    print("To test your solutions, implement the classes above or run solutions.py.")
