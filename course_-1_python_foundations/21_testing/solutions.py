"""Module 21 Solutions"""
import pytest

def word_count(text: str) -> int:
    return len(text.split())

def test_word_count_empty():
    assert word_count("") == 0

def test_word_count_single():
    assert word_count("hello") == 1

def test_word_count_sentence():
    assert word_count("hello world foo") == 3

class Stack:
    def __init__(self): self._items = []
    def push(self, x): self._items.append(x)
    def pop(self): return self._items.pop()
    def is_empty(self): return len(self._items) == 0

def test_stack_push_pop():
    s = Stack()
    s.push(1)
    assert s.pop() == 1

def test_stack_empty():
    assert Stack().is_empty()

def test_stack_not_empty_after_push():
    s = Stack(); s.push("x")
    assert not s.is_empty()

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3), (0, 0, 0), (-1, 1, 0)
])
def test_add(a, b, expected):
    assert a + b == expected
