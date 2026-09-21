"""Module 21 Exercises"""

# Level 1: Write a test for the `word_count` function from Module 11.
def word_count(text: str) -> int:
    return len(text.split())

def test_word_count_empty():
    raise NotImplementedError   # TODO

# Level 2: Fix the buggy test (it always passes even when the code is wrong).
def test_broken():
    result = 1 + 1
    assert result == 2 or True   # BUG: always True

# Level 3: TODO — write 3 tests for a stack class (push, pop, empty).
class Stack:
    def __init__(self): self._items = []
    def push(self, x): self._items.append(x)
    def pop(self): return self._items.pop()
    def is_empty(self): return len(self._items) == 0

# Level 4: TODO — write a parametrized pytest test for add().
