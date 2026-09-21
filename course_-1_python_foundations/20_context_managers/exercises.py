"""Module 20 Exercises"""
import contextlib

# Level 1: What happens if an exception occurs inside a `with` block?
# Does __exit__ still get called?

# Level 2: TODO — implement a context manager `Indenter` that tracks
# nesting depth. Each `with Indenter() as ind:` increases depth by 1.
class Indenter:
    depth = 0
    def __enter__(self):
        raise NotImplementedError
    def __exit__(self, *args):
        raise NotImplementedError

# Level 3: TODO — write a @contextmanager `suppress_errors(*exc_types)`
# that catches the given exception types and continues silently.
@contextlib.contextmanager
def suppress_errors(*exc_types):
    raise NotImplementedError

# Level 4: TODO — implement a database transaction context manager
# that calls conn.commit() on success or conn.rollback() on error.
@contextlib.contextmanager
def transaction(conn):
    raise NotImplementedError
