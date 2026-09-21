"""Module 17 Solutions"""

class Take:
    def __init__(self, iterable, n):
        self._iter = iter(iterable)
        self._remaining = n
    def __iter__(self):
        return self
    def __next__(self):
        if self._remaining <= 0:
            raise StopIteration
        self._remaining -= 1
        return next(self._iter)

def interleave(a, b):
    for x, y in zip(a, b):
        yield x
        yield y
