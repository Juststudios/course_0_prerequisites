"""Module 11 Solutions"""
import tempfile, os

# Level 2 solution
with open("/tmp/test_mod.txt", "w") as f:
    f.write("hello")
os.unlink("/tmp/test_mod.txt")

# Level 3 solution
def word_count(filepath: str) -> int:
    with open(filepath, "r", encoding="utf-8") as f:
        return len(f.read().split())

# Level 4 solution: change "r" to "w" in the first open()
def save_and_load(data: str) -> str:
    with open("/tmp/demo.txt", "w") as f:   # FIX: "w" not "r"
        f.write(data)
    with open("/tmp/demo.txt", "r") as f:
        return f.read()
