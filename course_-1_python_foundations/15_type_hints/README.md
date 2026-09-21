# Module 15: Type Hints

## Key Terminology
| Annotation | Meaning |
|-----------|---------|
| `name: str` | `name` is expected to be a string |
| `-> int` | The function returns an integer |
| `list[str]` | A list where every element is a string |
| `dict[str, int]` | Keys are strings, values are integers |
| `Optional[str]` | Either a string or `None` |
| `Callable[[str], int]` | A callable taking `str`, returning `int` |
| `Any` | Any type (opt-out of type checking) |

## Important: Runtime Enforcement
Python does NOT automatically enforce type hints:
```python
def add(a: int, b: int) -> int:
    return a + b
add("hello", "world")   # works at runtime! Returns "helloworld"
```
Use **mypy** or **pyright** to catch type errors statically.
