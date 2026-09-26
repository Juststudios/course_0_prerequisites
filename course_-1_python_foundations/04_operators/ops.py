"""
Module 04: Operators in Python
==============================
This lesson explores Python's rich operator ecosystem:
arithmetic, true vs floor division, modulo, chained comparisons,
logical operators and short-circuit evaluation, bitwise flags,
identity vs equality, and precedence rules.

Run this script directly:
    python3 ops.py
"""

import sys

print("=" * 75)
print("MODULE 04: OPERATORS — ARITHMETIC, LOGIC, BITWISE & COMPARISONS")
print("=" * 75)


# -----------------------------------------------------------------------------
# Section 1: Arithmetic Operators & Division Semantics
# -----------------------------------------------------------------------------
# Python distinguishes between TRUE DIVISION (/) and FLOOR DIVISION (//).
# True division always returns a float.
# Floor division rounds towards negative infinity.

print("\n--- [Section 1: Arithmetic Operators & Division] ---")

a = 17
b = 5

print(f"Operands: a = {a}, b = {b}")
print(f"  Addition (a + b):         {a + b}")
print(f"  Subtraction (a - b):      {a - b}")
print(f"  Multiplication (a * b):   {a * b}")
print(f"  True Division (a / b):    {a / b} (Type: {type(a / b).__name__})")
print(f"  Floor Division (a // b):  {a // b} (Type: {type(a // b).__name__})")
print(f"  Modulo / Remainder (a % b): {a % b}")
print(f"  Exponentiation (b ** 3):  {b ** 3}")

# The negative floor division nuance:
print("\nNegative Floor Division Mechanics:")
print(f"   7 // 2  = {7 // 2}   (3.5 rounds down to 3)")
print(f"  -7 // 2  = {-7 // 2}  (-3.5 rounds down towards -infinity to -4!)")
print(f"   7 % 2   = {7 % 2}")
print(f"  -7 % 2   = {-7 % 2}   (Python modulo maintains: a == (a // b) * b + (a % b))")
assert -7 == (-7 // 2) * 2 + (-7 % 2), "Modulo identity invariant"


# -----------------------------------------------------------------------------
# Section 2: Comparison Operators & Chained Comparisons
# -----------------------------------------------------------------------------
# Comparison operators test relationships and produce boolean values.
# Python allows intuitive mathematical chaining like `a < b < c`.

print("\n--- [Section 2: Comparison Operators & Chaining] ---")

x = 25
y = 50
z = 75

print(f"x = {x}, y = {y}, z = {z}")
print(f"  Equality (x == 25):      {x == 25}")
print(f"  Inequality (x != y):     {x != y}")
print(f"  Less than (x < y):       {x < y}")
print(f"  Greater or equal (z >= 75): {z >= 75}")

# Chained comparisons:
print("\nChained Comparisons:")
in_bounds = 10 <= x <= 30
print(f"  Is 10 <= x <= 30? {in_bounds}")

monotonic = x < y < z
print(f"  Is x < y < z strictly increasing? {monotonic}")

# Python evaluates chained comparisons without evaluating the middle operand twice:
print(f"  0 < x < 10: {0 < x < 10}")


# -----------------------------------------------------------------------------
# Section 3: Logical Operators & Short-Circuit Evaluation
# -----------------------------------------------------------------------------
# Python's logical operators: and, or, not
# KEY INSIGHT: 'and' and 'or' return the actual OPERAND that determined the outcome,
# not necessarily a boolean literal!
# SHORT-CIRCUIT: Python stops evaluation as soon as the outcome is known.

print("\n--- [Section 3: Logical Operators & Short-Circuit Evaluation] ---")

# Short-circuit with 'and':
# If the first operand is falsy, it is returned immediately; second operand is NOT touched.
falsy_val = 0
truthy_val = "Active"

result_and = falsy_val and truthy_val
print(f"0 and 'Active' -> {repr(result_and)} (falsy left side returned immediately)")

result_and_2 = "User" and "Admin"
print(f"'User' and 'Admin' -> {repr(result_and_2)} (both truthy, returns last)")

# Short-circuit with 'or':
# If the first operand is truthy, it is returned immediately.
result_or = "Primary" or "Fallback"
print(f"'Primary' or 'Fallback' -> {repr(result_or)} (truthy left side returned immediately)")

result_or_2 = "" or "Default Model"
print(f"'' or 'Default Model' -> {repr(result_or_2)} (falsy left side, returns fallback)")

# Guarding against crashes using short-circuit:
agent_data = None
# This will NOT crash with AttributeError because the left side is False!
safe_check = (agent_data is not None) and (len(agent_data) > 0)
print(f"Safe check on None: {safe_check}")


# -----------------------------------------------------------------------------
# Section 4: Bitwise Operators (Flag Masks & Permissions)
# -----------------------------------------------------------------------------
# Bitwise operators manipulate numbers at the raw binary bit level.
# Common in systems programming, networking, and agent security permissions.

print("\n--- [Section 4: Bitwise Operators & Permission Masks] ---")

# Define permission bits using bitwise left-shift (1 << n):
PERM_READ    = 1 << 0  # 1  (0b0001)
PERM_WRITE   = 1 << 1  # 2  (0b0010)
PERM_EXECUTE = 1 << 2  # 4  (0b0100)
PERM_DELETE  = 1 << 3  # 8  (0b1000)

print("Permission Bit Flags:")
print(f"  READ:    {PERM_READ:04b} ({PERM_READ})")
print(f"  WRITE:   {PERM_WRITE:04b} ({PERM_WRITE})")
print(f"  EXECUTE: {PERM_EXECUTE:04b} ({PERM_EXECUTE})")
print(f"  DELETE:  {PERM_DELETE:04b} ({PERM_DELETE})")

# Combining permissions with bitwise OR (|):
editor_role = PERM_READ | PERM_WRITE
print(f"\nEditor Role (READ | WRITE): {editor_role:04b} ({editor_role})")

# Checking permissions with bitwise AND (&):
has_read = bool(editor_role & PERM_READ)
has_exec = bool(editor_role & PERM_EXECUTE)
print(f"  Does Editor have READ?    {has_read}")
print(f"  Does Editor have EXECUTE? {has_exec}")

# Toggling a permission with bitwise XOR (^):
editor_role ^= PERM_EXECUTE  # Grants EXECUTE
print(f"  After toggling EXECUTE:   {editor_role:04b} (has exec: {bool(editor_role & PERM_EXECUTE)})")
editor_role ^= PERM_EXECUTE  # Revokes EXECUTE
print(f"  After toggling again:     {editor_role:04b} (has exec: {bool(editor_role & PERM_EXECUTE)})")

# Inverting / Bitwise NOT (~):
val = 5  # 0b101
print(f"\nBitwise NOT (~5): {~val} (two's complement: -(5 + 1) = -6)")


# -----------------------------------------------------------------------------
# Section 5: Membership and Identity Operators
# -----------------------------------------------------------------------------
# in / not in: checks membership in a sequence or container
# is / is not: checks physical memory object identity

print("\n--- [Section 5: Membership & Identity Operators] ---")

allowed_tools = ["search", "calculator", "terminal", "python_repl"]
requested_tool = "terminal"

print(f"Allowed tools: {allowed_tools}")
print(f"  Is '{requested_tool}' in allowed_tools? {'terminal' in allowed_tools}")
print(f"  Is 'rm_rf' not in allowed_tools?        {'rm_rf' not in allowed_tools}")

# Identity vs. Equality with lists:
list_a = [10, 20, 30]
list_b = [10, 20, 30]
print(f"\nComparing identical list values: list_a == list_b is {list_a == list_b}")
print(f"Comparing object identity:       list_a is list_b is {list_a is list_b}")
print(f"Identity with None:              requested_tool is not None -> {requested_tool is not None}")


# -----------------------------------------------------------------------------
# Section 6: Augmented Assignment Operators
# -----------------------------------------------------------------------------
# Modify a variable in-place: +=, -=, *=, /=, //=, %=, **=, &=, |=

print("\n--- [Section 6: Augmented Assignment] ---")

counter = 10
print(f"Initial counter: {counter}")
counter += 5   # counter = counter + 5
print(f"  After counter += 5:  {counter}")
counter *= 2   # counter = counter * 2
print(f"  After counter *= 2:  {counter}")
counter //= 4  # counter = counter // 4
print(f"  After counter //= 4: {counter}")
counter **= 2  # counter = counter ** 2
print(f"  After counter **= 2: {counter}")


# -----------------------------------------------------------------------------
# Section 7: Operator Precedence & Parentheses
# -----------------------------------------------------------------------------
# Precedence order (highest to lowest):
#   1. Parentheses: ()
#   2. Exponentiation: **
#   3. Unary signs and bitwise NOT: +x, -x, ~x
#   4. Multiplication, Division, Modulo: *, /, //, %
#   5. Addition, Subtraction: +, -
#   6. Bitwise shifts: <<, >>
#   7. Bitwise AND: &
#   8. Bitwise XOR: ^, OR: |
#   9. Comparisons and Membership: <, <=, >, >=, ==, !=, in, is
#  10. Logical NOT: not
#  11. Logical AND: and
#  12. Logical OR: or

print("\n--- [Section 7: Operator Precedence & Explicit Grouping] ---")

calc_ambiguous = 2 + 3 * 4 ** 2
calc_explicit  = 2 + (3 * (4 ** 2))
print(f"2 + 3 * 4 ** 2 = {calc_ambiguous}")
print(f"With explicit grouping: {calc_explicit} (4**2 = 16; 16*3 = 48; 48+2 = 50)")

bool_precedence = False or True and not False
# Evaluates as: False or (True and (not False)) -> False or (True and True) -> True
print(f"False or True and not False = {bool_precedence}")
print("Best Practice: Always use parentheses to clarify complex logical expressions!")


# -----------------------------------------------------------------------------
# Section 8: Real-World Scenario — AI Agent Safety & Budget Gate
# -----------------------------------------------------------------------------
# Autonomous Agent Gate: validates budget, rate limits, and access permissions.

print("\n--- [Section 8: AI Agent Guardrail & Budget Engine] ---")

def evaluate_agent_call(
    agent_perms: int,
    required_perm: int,
    current_tokens: int,
    token_cost: int,
    max_token_budget: int,
    cooldown_seconds: float,
    min_cooldown: float
) -> dict:
    """
    Evaluates whether an agent tool call is authorized and within budgets.
    """
    # 1. Bitwise permission check
    has_perm = bool(agent_perms & required_perm)

    # 2. Arithmetic token projection
    projected_tokens = current_tokens + token_cost
    is_within_budget = 0 <= projected_tokens <= max_token_budget

    # 3. Comparison cooldown check
    is_cooled_down = cooldown_seconds >= min_cooldown

    # 4. Compound logical decision using short-circuiting
    can_execute = has_perm and is_within_budget and is_cooled_down

    # 5. Calculate remaining quota percentage using true and floor division
    remaining_tokens = max_token_budget - projected_tokens
    budget_pct = (projected_tokens / max_token_budget) * 100
    batches_remaining = remaining_tokens // max(token_cost, 1)

    return {
        "authorized": can_execute,
        "has_perm": has_perm,
        "budget_ok": is_within_budget,
        "cooldown_ok": is_cooled_down,
        "projected_tokens": projected_tokens,
        "budget_pct": round(budget_pct, 2),
        "batches_remaining": batches_remaining,
    }

# Run a test agent call evaluation:
agent_role = PERM_READ | PERM_EXECUTE  # Has read + execute
call_report = evaluate_agent_call(
    agent_perms=agent_role,
    required_perm=PERM_EXECUTE,
    current_tokens=5200,
    token_cost=800,
    max_token_budget=8000,
    cooldown_seconds=1.5,
    min_cooldown=1.0,
)

print("Agent Call Evaluation Report:")
for key, val in call_report.items():
    print(f"  {key:<20}: {val}")

print("\n" + "=" * 75)
print("LESSON COMPLETE: Python Operators successfully demonstrated.")
print("=" * 75)
