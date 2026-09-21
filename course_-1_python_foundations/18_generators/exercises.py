"""Module 18 Exercises"""

# Level 1: What is the difference between [x*2 for x in range(5)]
#          and (x*2 for x in range(5))?

# Level 2: TODO — fix this: the generator is consumed and then reused
def evens():
    return (x for x in range(0, 10, 2))
gen = evens()
print(list(gen))
print(list(gen))   # BUG: prints [] because gen is exhausted

# Level 3: TODO — write a generator `fibonacci()` that yields
# Fibonacci numbers indefinitely.
def fibonacci():
    raise NotImplementedError

# Level 4: TODO — write a generator `chunk(iterable, size)` that
# yields lists of `size` elements from the iterable.
def chunk(iterable, size: int):
    raise NotImplementedError
