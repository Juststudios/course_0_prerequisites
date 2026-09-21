"""Module 32: Python Debugging"""

# ── Reading a traceback ───────────────────────────────────────────────────────
# Tracebacks read from BOTTOM to TOP.
# The bottom line tells you WHAT went wrong.
# The lines above tell you WHERE and HOW you got there.

# Example traceback:
# Traceback (most recent call last):
#   File "agent.py", line 42, in run
#     result = registry.call(tool_name, **kwargs)
#   File "registry.py", line 15, in call
#     return self._tools[name](**kwargs)
# KeyError: 'search'
#
# Bottom: KeyError: 'search'  ← the problem
# Above:  registry.py line 15  ← where it happened
# Above:  agent.py line 42     ← what called it

# ── Systematic debugging workflow ───────────────────────────────────────────
# 1. Observe: what is the incorrect behaviour?
# 2. Reproduce: can you make it happen reliably?
# 3. Read traceback: what type of error? what line?
# 4. Locate: narrow down to the failing code
# 5. Understand: WHY is this happening?
# 6. Fix: make the minimal change
# 7. Test: does it pass? did you break anything else?

# ── print() debugging ────────────────────────────────────────────────────────
def buggy(data):
    print(f"  DEBUG: data={data!r}, type={type(data).__name__}")   # add temporarily
    return data["key"]

try:
    buggy({"key": "value"})
    buggy("oops")            # str has no key "key"
except (KeyError, TypeError) as e:
    print(f"Error: {e}")

# ── pdb: built-in interactive debugger ───────────────────────────────────────
# Insert `breakpoint()` (Python 3.7+) in your code to drop into pdb.
# Key commands:
#   n   → next line
#   s   → step into function
#   p x → print x
#   q   → quit
print("\nDebugging lesson complete.")
