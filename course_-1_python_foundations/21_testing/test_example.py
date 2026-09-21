"""Example pytest test file — run with: pytest test_example.py -v"""

def add(a, b):
    return a + b

def test_add_basic():
    assert add(2, 3) == 5

def test_add_floats():
    assert abs(add(0.1, 0.2) - 0.3) < 1e-9

def test_add_strings():
    assert add("hello", " world") == "hello world"

import pytest

def test_raises_on_none():
    with pytest.raises(TypeError):
        add(None, 1)
