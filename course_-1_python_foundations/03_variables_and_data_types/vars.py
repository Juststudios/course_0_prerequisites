"""
Module 03: Variables and Data Types in Python
=============================================
This lesson explores the core mental model of Python variables:
object references (name tags), primitive data types, dynamic vs. strong typing,
type inspection, explicit casting, truthiness, and identity vs. equality.

Run this script directly:
    python3 vars.py
"""

import math
import sys

print("=" * 75)
print("MODULE 03: VARIABLES AND DATA TYPES — OBJECT REFERENCES & PRIMITIVES")
print("=" * 75)


# -----------------------------------------------------------------------------
# Section 1: Variables as Object References (Balloons and Name Tags)
# -----------------------------------------------------------------------------
# In Python, variables are NOT boxes holding bits.
# Variables are symbolic name tags tied to objects floating in heap memory.
# Every object has three essential attributes:
#   1. An Identity (its memory address, accessed with id())
#   2. A Type (what kind of object it is, accessed with type())
#   3. A Value (the data it encapsulates)

print("\n--- [Section 1: Variables as Object References] ---")

score = 100
print(f"score = {score}")
print(f"  Type of score: {type(score).__name__}")
print(f"  Memory address (id): {id(score)}")

# Binding another name to the exact same object:
points = score
print(f"\npoints = score")
print(f"  points value: {points}")
print(f"  Memory address (id) of points: {id(points)}")
print(f"  Do score and points reference the exact same object? {score is points}")

# Reassigning score binds it to a brand new integer object:
score = 250
print(f"\nAfter score = 250:")
print(f"  score value: {score}, id: {id(score)}")
print(f"  points value: {points}, id: {id(points)}")
print(f"  Notice: points still points to 100! score was simply rebound.")


# -----------------------------------------------------------------------------
# Section 2: The Core Primitive Types
# -----------------------------------------------------------------------------
# Python comes with five essential primitive data types.

print("\n--- [Section 2: The Core Primitive Data Types] ---")

# 1. Integer (int): Arbitrary-precision whole numbers
active_agents = 7
large_count = 10 ** 40  # Integers never overflow in Python 3!
print(f"Integer (int): {active_agents}")
print(f"Arbitrary precision integer (10**40):\n  {large_count}")

# 2. Float (float): 64-bit IEEE 754 double precision
temperature = 0.7
learning_rate = 0.00025
scientific_val = 1.602e-19  # Electron charge in Coulombs
print(f"\nFloating-point (float): {temperature}, {learning_rate}")
print(f"Scientific notation float: {scientific_val}")

# 3. String (str): Immutable Unicode sequence
agent_model = "gpt-4-turbo"
multiline_prompt = """You are a helpful assistant.
Always think step-by-step."""
print(f"\nString (str): {agent_model}")
print(f"Multiline string length: {len(multiline_prompt)} characters")

# 4. Boolean (bool): Binary logical states (True / False)
is_authenticated = True
is_blocked = False
print(f"\nBoolean (bool): is_authenticated={is_authenticated}, is_blocked={is_blocked}")
print(f"Under the hood, bool is a subclass of int: True == {int(True)}, False == {int(False)}")

# 5. NoneType (None): The null object / intentional absence of value
last_error_message = None
print(f"\nNoneType: last_error_message={last_error_message}")
print(f"Type: {type(last_error_message).__name__}")


# -----------------------------------------------------------------------------
# Section 3: Dynamic Typing vs. Strong Typing
# -----------------------------------------------------------------------------
# DYNAMIC TYPING means a variable name can refer to an integer at one moment
# and a string or float at a later moment. The type belongs to the object, not the name.
# STRONG TYPING means Python refuses to perform senseless operations between incompatible types.

print("\n--- [Section 3: Dynamic Typing vs. Strong Typing] ---")

dynamic_var = 42
print(f"dynamic_var is initially: {dynamic_var} (type: {type(dynamic_var).__name__})")

dynamic_var = "Now I am a sentence"
print(f"dynamic_var is rebound to: '{dynamic_var}' (type: {type(dynamic_var).__name__})")

dynamic_var = [1, 2, 3]
print(f"dynamic_var is now a list: {dynamic_var} (type: {type(dynamic_var).__name__})")

# Demonstrating Strong Typing:
print("\nDemonstrating Strong Typing:")
a = "50"
b = 50
print(f"a = '{a}' (str), b = {b} (int)")
try:
    # Python refuses to guess whether you want "5050" or 100!
    bad_calc = a + b
except TypeError as err:
    print(f"  Caught expected TypeError: {err}")
    print("  Python will NEVER silently coerce types in arithmetic. You must be explicit!")


# -----------------------------------------------------------------------------
# Section 4: Safe Type Inspection
# -----------------------------------------------------------------------------
# Always prefer isinstance() over type() == ... because isinstance() properly
# handles class inheritance and allows checking multiple types at once.

print("\n--- [Section 4: Safe Type Inspection] ---")

val = 42.0

print(f"Inspecting val = {val}:")
print(f"  Using type(): {type(val)} == float: {type(val) is float}")
print(f"  Using isinstance(val, float): {isinstance(val, float)}")
print(f"  Is val a number (int or float)? {isinstance(val, (int, float))}")
print(f"  Is True an instance of int? {isinstance(True, int)} (because bool inherits from int!)")
print(f"  Is type(True) == int? {type(True) is int} (exact type match fails)")


# -----------------------------------------------------------------------------
# Section 5: Type Casting and Coercion
# -----------------------------------------------------------------------------
# Explicitly converting data from one representation to another using constructors.

print("\n--- [Section 5: Type Casting and Coercion] ---")

raw_input_str = "128"
numeric_val = int(raw_input_str)
float_val = float(numeric_val)
back_to_text = str(float_val)

print(f"Original string: '{raw_input_str}' ({type(raw_input_str).__name__})")
print(f"Cast to int:     {numeric_val} ({type(numeric_val).__name__})")
print(f"Cast to float:   {float_val} ({type(float_val).__name__})")
print(f"Cast to str:     '{back_to_text}' ({type(back_to_text).__name__})")

# Truncation during float-to-int conversion:
pi = 3.9999
truncated_pi = int(pi)  # Discards decimal part, does NOT round!
print(f"\nTruncating float to int: int({pi}) -> {truncated_pi} (truncates towards zero)")


# -----------------------------------------------------------------------------
# Section 6: Truthiness and Falsiness
# -----------------------------------------------------------------------------
# In Python, any value can be evaluated as a boolean in an if-statement or bool().
# The following values are considered FALSY:
#   - None
#   - False
#   - Zero of any numeric type: 0, 0.0, 0j
#   - Any empty sequence or collection: '', (), [], {}, set(), range(0)
# Everything else is TRUTHY.

print("\n--- [Section 6: Truthiness and Falsiness] ---")

test_values = [
    0,
    0.0,
    "",
    "hello",
    [],
    [0],  # Non-empty list containing zero!
    None,
    -1,
    {},
    {"key": "val"},
]

print("Evaluating truthiness of common values:")
for item in test_values:
    evaluated = bool(item)
    label = "TRUTHY" if evaluated else "FALSY"
    print(f"  bool({repr(item):<16}) -> {evaluated!s:<5} ({label})")


# -----------------------------------------------------------------------------
# Section 7: Identity (is) vs. Equality (==)
# -----------------------------------------------------------------------------
# Equality (==): Compares contents / values.
# Identity (is): Compares memory addresses (whether both point to the same object).

print("\n--- [Section 7: Identity (is) vs. Equality (==)] ---")

list_x = [1, 2, 3]
list_y = [1, 2, 3]

print(f"list_x = {list_x}, id = {id(list_x)}")
print(f"list_y = {list_y}, id = {id(list_y)}")
print(f"  list_x == list_y (Equal values?): {list_x == list_y}")
print(f"  list_x is list_y (Same object?):  {list_x is list_y}")

# Small Integer Caching (-5 to 256):
small_1 = 100
small_2 = 100
print(f"\nSmall integers (100):")
print(f"  small_1 is small_2: {small_1 is small_2} (CPython caches integers -5 to 256)")

large_1 = 100_000
large_2 = 100_000
print(f"Large integers (100_000):")
print(f"  large_1 == large_2: {large_1 == large_2}")
print(f"  large_1 is large_2: {large_1 is large_2} (May differ across allocations)")
print("  Rule: Always use '==' to compare values. Use 'is' only for singletons like None!")


# -----------------------------------------------------------------------------
# Section 8: Real-World Scenario — Autonomous Agent State Management
# -----------------------------------------------------------------------------
# Here we put everything together: parsing untyped JSON-like strings from an API,
# casting them to proper types, validating constraints, and maintaining state.

print("\n--- [Section 8: Autonomous Agent State Processing] ---")

def process_agent_action(raw_payload: dict) -> dict:
    """
    Parses and type-validates an incoming action payload for an AI Agent.
    """
    # Extract and cast tool name (string)
    tool_name = str(raw_payload.get("tool", "")).strip()
    if not tool_name:
        raise ValueError("Payload missing valid 'tool' string.")

    # Extract and cast timeout (integer seconds)
    raw_timeout = raw_payload.get("timeout_sec", 30)
    timeout_sec = int(raw_timeout)
    if timeout_sec <= 0:
        raise ValueError("timeout_sec must be a positive integer.")

    # Extract and cast temperature (float between 0.0 and 2.0)
    raw_temp = raw_payload.get("temperature", 0.7)
    temperature = float(raw_temp)
    if not (0.0 <= temperature <= 2.0):
        raise ValueError("temperature must be within [0.0, 2.0].")

    # Extract execution flag (bool)
    is_async = bool(raw_payload.get("is_async", False))

    # Error tracker initialized to None
    last_error = None

    return {
        "tool": tool_name,
        "timeout_sec": timeout_sec,
        "temperature": temperature,
        "is_async": is_async,
        "last_error": last_error,
        "is_ready": True,
    }

incoming_api_payload = {
    "tool": "web_search",
    "timeout_sec": "45",       # string needs casting to int
    "temperature": "0.2",      # string needs casting to float
    "is_async": 1,             # int truthy needs casting to bool
}

processed_state = process_agent_action(incoming_api_payload)
print("Successfully validated and transformed agent state:")
for key, value in processed_state.items():
    print(f"  {key:<14}: {repr(value):<12} (type: {type(value).__name__})")

print("\n" + "=" * 75)
print("LESSON COMPLETE: Variables & Data Types successfully demonstrated.")
print("=" * 75)
