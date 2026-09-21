"""
Module 20: Context Managers

TERM: Context Manager
DEFINITION: An object that sets up a resource when entering a `with` block
            and automatically tears it down when leaving — even on error.
INTUITION: A hotel room: you check in (__enter__), use the room, then
           check out (__exit__) whether or not something goes wrong.
WHY IT EXISTS: Guarantees cleanup — no forgotten file handles, locks, connections.
"""
import contextlib, tempfile, os, time

# ── Built-in examples ────────────────────────────────────────────────────────
# Files (the classic):
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
    f.write("data")
    path = f.name
os.unlink(path)

# ── Implementing __enter__ / __exit__ ────────────────────────────────────────
class Timer:
    """Measures elapsed time in a with block."""

    def __enter__(self):
        self._start = time.perf_counter()
        return self                       # becomes `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self._start
        print(f"  Elapsed: {self.elapsed:.4f}s")
        return False    # False → don't suppress exceptions

with Timer() as t:
    time.sleep(0.1)

print(f"Measured: {t.elapsed:.4f}s")

# ── @contextmanager shortcut ─────────────────────────────────────────────────
@contextlib.contextmanager
def temporary_directory():
    """Create and clean up a temp directory."""
    import tempfile, shutil
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir          # everything in the `with` block runs here
    finally:
        shutil.rmtree(tmpdir) # always cleaned up

with temporary_directory() as d:
    print(f"Working in: {d}")
    # create files, do work...
# d is gone now

# ── Connection to Course 0 ───────────────────────────────────────────────────
# Course 0 uses context managers for:
#   - HTTP sessions (`async with httpx.AsyncClient() as client`)
#   - Database transactions (`with conn:`)
#   - Locks and semaphores in async code
print("\nContext managers lesson complete.")
