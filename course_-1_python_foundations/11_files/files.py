"""
Module 11: Files

TERM: File
DEFINITION: A named location on disk that stores data persistently.
INTUITION: Like a notebook — you can open it, read it, write in it, then close it.
WHY IT EXISTS: Programs need to save data between runs.
"""

# ── Reading a file with 'with' (context manager) ────────────────────────────
# 'with' automatically closes the file even if an error occurs.
# This is called "resource management."

import tempfile, os

# Create a temporary file for demonstration
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
    tmp.write("Hello, Python!\nLine 2\nLine 3")
    tmp_path = tmp.name

print("=== Reading the whole file ===")
with open(tmp_path, "r", encoding="utf-8") as f:
    content = f.read()
print(content)

print("\n=== Reading line by line ===")
with open(tmp_path, "r", encoding="utf-8") as f:
    for line in f:
        print(repr(line))   # repr shows \n explicitly

print("\n=== Appending to a file ===")
with open(tmp_path, "a", encoding="utf-8") as f:
    f.write("\nAppended line")

with open(tmp_path, "r") as f:
    print(f.read())

os.unlink(tmp_path)
print("\nDone. File cleaned up.")

# ── Common Mistakes ──────────────────────────────────────────────────────────
# BAD:  f = open("data.txt")    # if an error occurs, file is never closed
# GOOD: with open("data.txt") as f:  ...
# BAD:  open("data.txt", "w")   # erases contents immediately!
# GOOD: use "a" to append, "r" to read, "w" to (over)write

# ── Connection to AI Agents ──────────────────────────────────────────────────
# Agents write logs, read configuration files, and save conversation history
# to disk — all using the same file primitives you just learned.
