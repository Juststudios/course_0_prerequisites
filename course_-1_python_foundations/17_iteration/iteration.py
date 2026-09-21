"""
Module 17: Iteration

TERM: Iterable
DEFINITION: Any object Python can loop over (list, str, dict, file, ...).
TERM: Iterator
DEFINITION: An object that remembers its position and produces the next value
            via next().
INTUITION: An iterable is a book; an iterator is a bookmark.
"""

# ── What actually happens in a for loop ─────────────────────────────────────
numbers = [10, 20, 30]
it = iter(numbers)        # create iterator
print(next(it))           # 10
print(next(it))           # 20
print(next(it))           # 30
# next(it) again → StopIteration (end of sequence)

# Python's for loop does exactly this internally:
for n in numbers:         # same as above, but automatic
    print(n)

# ── Custom iterable class ────────────────────────────────────────────────────
class Countdown:
    def __init__(self, start: int):
        self._current = start

    def __iter__(self):     # makes this object iterable
        return self         # the object IS its own iterator here

    def __next__(self) -> int:
        if self._current < 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value

print("\nCountdown: ", list(Countdown(5)))   # [5, 4, 3, 2, 1, 0]

# ── Built-in iteration tools ─────────────────────────────────────────────────
names = ["Alice", "Bob", "Charlie"]

# enumerate gives index + value
for i, name in enumerate(names):
    print(f"{i}: {name}")

# zip combines two sequences
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
