"""
Module 06 Exercises — Collections

Level 1: Recall
1. What is the difference between a list and a tuple?
2. Which collection type requires all items to be unique?
"""

# Level 2: Modify
# TODO: Modify this list to append the number 5, then remove the number 1.
def modify_list(lst: list) -> list:
    # lst.append(...)
    raise NotImplementedError("Implement modify_list")

# Level 3: Build
# TODO: Write a function that takes a string and returns a dictionary 
# counting how many times each character appears.
def count_chars(text: str) -> dict:
    raise NotImplementedError("Implement count_chars")

# Level 4: Debug
# TODO: Find the bug and fix it. We want to combine two dictionaries,
# but keeping the value from d1 if there is a conflict.
def merge_dicts(d1: dict, d2: dict) -> dict:
    # return d1 | d2   # BUG: d1 | d2 keeps the value from d2 on conflict!
    raise NotImplementedError("Fix the bug")
