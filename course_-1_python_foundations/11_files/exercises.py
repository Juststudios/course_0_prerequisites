"""Module 11 Exercises — Files"""

# ── Level 1: Understand ──────────────────────────────────────────────────────
# Run this and explain the output:
import tempfile, os
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
    f.write("apple\nbanana\ncherry")
    path = f.name

with open(path, "r") as f:
    lines = f.readlines()
print(lines)   # What does readlines() return?
os.unlink(path)

# ── Level 2: Modify ──────────────────────────────────────────────────────────
# TODO: Rewrite the block below so it uses a context manager (with statement).
# f = open("/tmp/test_mod.txt", "w")
# f.write("hello")
# f.close()

# ── Level 3: Build ──────────────────────────────────────────────────────────
# TODO: Write a function `word_count(filepath)` that returns
#       the number of words in a text file.
def word_count(filepath: str) -> int:
    raise NotImplementedError("Implement word_count()")

# ── Level 4: Debug ──────────────────────────────────────────────────────────
# This code has a bug. Find and fix it.
# def save_and_load(data: str) -> str:
#     with open("/tmp/demo.txt", "r") as f:   # BUG: wrong mode
#         f.write(data)
#     with open("/tmp/demo.txt", "r") as f:
#         return f.read()
