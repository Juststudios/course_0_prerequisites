# Module 20: Context Managers

## Key Terminology
| Term | Definition |
|------|-----------|
| **Context manager** | Object with `__enter__` and `__exit__` |
| **`with X as y:`** | Enter X, bind result to y, exit X when done |
| **`__enter__`** | Called on entry; return value becomes `as` variable |
| **`__exit__`** | Called on exit; receives exception info (or `None, None, None`) |
| **`@contextmanager`** | Decorator to write a context manager as a generator |

## Guarantee
`__exit__` is always called — even if an exception is raised. This is the key advantage over manual cleanup code.

## Connection to AI Agents
In Course 0 you will see:
```python
async with httpx.AsyncClient() as client:
    response = await client.post(...)
```
The `AsyncClient` is an async context manager — same idea, but with `__aenter__` and `__aexit__`.
