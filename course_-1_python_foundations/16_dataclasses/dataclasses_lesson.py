"""
Module 16: Dataclasses

TERM: Dataclass
DEFINITION: A class automatically given __init__, __repr__, and __eq__ based
            on its field annotations.
WHY IT EXISTS: Writing boilerplate __init__ for every config/data class is tedious.
"""
from dataclasses import dataclass, field
from typing import Optional

# ── Basic dataclass ──────────────────────────────────────────────────────────
@dataclass
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)
print(p)           # Point(x=3.0, y=4.0)  ← __repr__ auto-generated
print(p.x, p.y)   # attribute access

# ── Agent configuration ──────────────────────────────────────────────────────
@dataclass
class AgentConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024
    timeout: float = 30.0
    tags: list[str] = field(default_factory=list)  # mutable defaults need field()
    api_key: Optional[str] = None

cfg = AgentConfig(model="hermes-v1")
print(cfg)
cfg.temperature = 0.9
print(f"Updated temperature: {cfg.temperature}")

# ── Why not just use a plain dict? ───────────────────────────────────────────
# dict:      cfg["model"]      → no autocomplete, easy typos
# dataclass: cfg.model         → autocomplete, IDE checks type
print("\nDataclasses lesson complete.")
