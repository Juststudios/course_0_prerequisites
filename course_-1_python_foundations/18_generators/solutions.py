"""Module 18 Solutions"""

# Level 2: create a new generator each time
def evens():
    return (x for x in range(0, 10, 2))
print(list(evens()))   # [0, 2, 4, 6, 8]
print(list(evens()))   # [0, 2, 4, 6, 8] — fresh generator

# Level 3:
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Level 4:
def chunk(iterable, size: int):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf
