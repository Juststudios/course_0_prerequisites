"""Module 20 Solutions"""
import contextlib

class Indenter:
    depth = 0
    def __enter__(self):
        Indenter.depth += 1
        return self
    def __exit__(self, *args):
        Indenter.depth -= 1
        return False

@contextlib.contextmanager
def suppress_errors(*exc_types):
    try:
        yield
    except exc_types:
        pass

@contextlib.contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
