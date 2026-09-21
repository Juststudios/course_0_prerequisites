"""
Module 19: Decorators

TERM: Decorator
DEFINITION: A function that takes another function and returns a new,
            enhanced version of it.
INTUITION: A decorator is a wrapper — like putting bubble-wrap around a gift.
           The gift (original function) is unchanged; the wrapper adds behaviour.
"""
import time, functools

# ── Step 1: functions are objects ────────────────────────────────────────────
def greet():
    print("Hello!")

fn = greet          # store function in a variable — no ()
fn()                # call it via the variable

# ── Step 2: a function that takes a function ─────────────────────────────────
def make_louder(func):
    """Wraps func so its name is printed before calling it."""
    def wrapper(*args, **kwargs):
        print(f"  [CALLING {func.__name__}]")
        result = func(*args, **kwargs)
        print(f"  [DONE {func.__name__}]")
        return result
    return wrapper

def add(a, b):
    return a + b

loud_add = make_louder(add)
print(loud_add(2, 3))

# ── Step 3: the @ syntax ─────────────────────────────────────────────────────
def timer(func):
    """Measure how long a function takes."""
    @functools.wraps(func)          # preserves __name__ and __doc__
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(0.1)
    return a + b

print(slow_add(3, 4))

# ── Step 4: practical decorator — retry ─────────────────────────────────────
def retry(max_attempts: int = 3):
    """Retry a function up to max_attempts times on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  Attempt {attempt} failed: {e}")
            raise RuntimeError(f"{func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network hiccup")
    return "Success!"

try:
    print(unreliable())
except RuntimeError as e:
    print(e)

print("\nDecorators lesson complete.")
