# Module 14: Special Methods (Dunders)

## Key Terminology
| Method | Triggered by |
|--------|-------------|
| `__init__` | `MyClass()` — construction |
| `__str__` | `str(obj)` or `print(obj)` |
| `__repr__` | REPL display and debugging |
| `__call__` | `obj(args)` — makes object callable |
| `__len__` | `len(obj)` |

## The `__call__` Method
```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
print(double(5))   # → 10
```
`double` behaves exactly like a function. This is why agent tools can be either plain functions or callable objects.
