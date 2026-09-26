"""
Module 06 Solutions
"""

# Level 1:
# 1. Lists are mutable; tuples are immutable.
# 2. A set.

# Level 2:
def modify_list(lst: list) -> list:
    lst.append(5)
    if 1 in lst:
        lst.remove(1)
    return lst

# Level 3:
def count_chars(text: str) -> dict:
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    return counts

# Level 4:
def merge_dicts(d1: dict, d2: dict) -> dict:
    # We want d1 to take precedence.
    return d2 | d1
