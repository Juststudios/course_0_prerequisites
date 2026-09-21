"""
Module 18: Generators

TERM: Generator
DEFINITION: A function that uses `yield` to produce a sequence of values
            lazily — one at a time, on demand.
INTUITION: Instead of cooking the entire meal and plating it all at once,
           you cook one bite at a time as the guest eats.
WHY IT EXISTS: Memory efficiency — you never store the entire sequence.
"""
import time

# ── Simple generator ─────────────────────────────────────────────────────────
def count_up(start: int, stop: int):
    """Yields integers from start to stop-1."""
    current = start
    while current < stop:
        yield current       # pause here; resume on next()
        current += 1

gen = count_up(1, 5)
print(type(gen))            # <class 'generator'>
print(next(gen))            # 1
print(next(gen))            # 2
print(list(gen))            # [3, 4]  — rest consumed

# ── Lazy evaluation saves memory ─────────────────────────────────────────────
# BAD for 1 billion numbers:
# numbers = list(range(1_000_000_000))   # uses ~8 GB RAM!
#
# GOOD:
numbers = range(1_000_000_000)           # generator-like, uses ~100 bytes
print(sum(x for x in numbers if x % 2 == 0 and x < 100))   # works fine

# ── Simulating a streaming LLM response ─────────────────────────────────────
def fake_llm_stream(text: str):
    """Simulates a streaming LLM token-by-token response."""
    for word in text.split():
        time.sleep(0.05)   # simulate network latency
        yield word + " "

print("\nStreaming: ", end="", flush=True)
for token in fake_llm_stream("Hello I am an AI agent"):
    print(token, end="", flush=True)
print()

# ── Generator expression (compact syntax) ────────────────────────────────────
squares = (x**2 for x in range(10))   # NOT a list! A generator.
print("\nSquares:", list(squares))
print("\nGenerators lesson complete.")
