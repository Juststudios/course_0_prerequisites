# Module 19: Decorators

## Key Terminology
| Term | Definition |
|------|-----------|
| **Decorator** | A function that wraps another function to extend its behaviour |
| **`@decorator`** | Syntactic sugar for `func = decorator(func)` |
| **`functools.wraps`** | Preserves the original function's `__name__` and `__doc__` |
| **`*args, **kwargs`** | Capture any positional and keyword arguments |

## The Pattern
```python
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # do something before
        result = func(*args, **kwargs)
        # do something after
        return result
    return wrapper
```

## Connection to AI Agents
Agent runtimes use decorators to register tools (`@agent.tool`), add retry logic, rate-limit calls, validate inputs, and log invocations.
