# Module 16: Dataclasses

## Key Terminology
| Term | Definition |
|------|-----------|
| `@dataclass` | Decorator that auto-generates `__init__`, `__repr__`, `__eq__` |
| `field(default_factory=list)` | Required for mutable defaults like lists/dicts |
| `frozen=True` | Makes the dataclass immutable (like a named tuple) |

## Typical Use
```python
@dataclass
class AgentConfig:
    model: str
    temperature: float = 0.7
```
Instead of writing `__init__` by hand.

## Connection to AI Agents
Agent runtimes use dataclasses extensively for configuration, tool parameters, and structured responses.
