"""
Module 06: Collections in Python
================================
This lesson provides a comprehensive, hands-on exploration of Python's
primary built-in collection types: lists, tuples, sets, and dictionaries.
We examine mutability, indexing, hashability, set operations, reference
aliasing, and realistic data architectures for AI agents.

Run this script directly:
    python3 collections_demo.py
"""

import copy
import sys
import time

print("=" * 75)
print("MODULE 06: COLLECTIONS — LISTS, TUPLES, SETS, AND DICTIONARIES")
print("=" * 75)


# -----------------------------------------------------------------------------
# Section 1: Lists — Ordered and Mutable Sequences
# -----------------------------------------------------------------------------
# Lists are dynamically sized arrays holding arbitrary Python objects.
# They maintain insertion order and can be modified in-place.

print("\n--- [Section 1: Lists — Ordered, Mutable Sequences] ---")

tasks = ["plan_architecture", "write_unit_tests"]
print(f"Initial tasks: {tasks} (len={len(tasks)})")

# Appending to the end: O(1) amortized
tasks.append("implement_feature")
print(f"After .append('implement_feature'): {tasks}")

# Extending with multiple items:
tasks.extend(["run_linter", "deploy_service"])
print(f"After .extend([...]): {tasks}")

# Inserting at a specific index: O(N) because elements must shift
tasks.insert(1, "review_requirements")
print(f"After .insert(1, 'review_requirements'): {tasks}")

# Removing and returning an item via .pop():
completed_task = tasks.pop(0)  # removes first task
last_task = tasks.pop()        # removes last task
print(f"Popped first: '{completed_task}'")
print(f"Popped last:  '{last_task}'")
print(f"Remaining tasks: {tasks}")

# In-place sorting and reversal:
scores = [45, 12, 89, 33, 71]
print(f"\nOriginal scores: {scores}")
scores.sort()
print(f"After .sort():   {scores}")
scores.reverse()
print(f"After .reverse():{scores}")


# -----------------------------------------------------------------------------
# Section 2: Tuples — Ordered, Immutable Records
# -----------------------------------------------------------------------------
# Tuples are immutable sequences. Once created, their size and contents
# cannot be altered. They protect data from accidental mutation.

print("\n--- [Section 2: Tuples — Ordered, Immutable Records] ---")

# Defining tuples:
empty_tuple = ()
single_element = ("important_config",)  # Trailing comma is mandatory!
agent_spec = ("Agent-Hermes", 3, 0.95, "ACTIVE")

print(f"Single-element tuple: {single_element} (Type: {type(single_element).__name__})")
print(f"Agent specification:  {agent_spec}")

# Tuple Unpacking:
name, priority, accuracy, status = agent_spec
print(f"Unpacked values: name='{name}', priority={priority}, accuracy={accuracy:.2f}, status='{status}'")

# Immutability Demonstration:
try:
    # Attempting to reassign a tuple element raises TypeError:
    agent_spec[0] = "Agent-Ares"
except TypeError as err:
    print(f"Caught expected TypeError: {err}")
    print("Tuples are strictly immutable!")


# -----------------------------------------------------------------------------
# Section 3: Sets — Unordered Collections of Unique Elements
# -----------------------------------------------------------------------------
# Sets contain only unique, hashable objects. They automatically eliminate
# duplicates and support powerful mathematical set algebra.

print("\n--- [Section 3: Sets — Unique Collections & Set Algebra] ---")

# Automatic deduplication:
raw_tokens = ["apple", "banana", "apple", "cherry", "banana", "date"]
unique_tokens = set(raw_tokens)
print(f"Raw tokens list:    {raw_tokens} (len={len(raw_tokens)})")
print(f"Deduplicated set:   {unique_tokens} (len={len(unique_tokens)})")

# Adding and removing:
allowed_roles = {"user", "assistant", "system"}
allowed_roles.add("function")
allowed_roles.discard("unknown")  # discard doesn't raise KeyError if missing!
print(f"Allowed roles: {allowed_roles}")

# Set Algebra Operations:
team_a_skills = {"python", "sql", "docker", "fastapi"}
team_b_skills = {"python", "kubernetes", "fastapi", "react"}

print(f"\nTeam A Skills: {team_a_skills}")
print(f"Team B Skills: {team_b_skills}")

# Union (|): All skills across both teams
union_skills = team_a_skills | team_b_skills
print(f"  Union (|):                {union_skills}")

# Intersection (&): Shared skills
shared_skills = team_a_skills & team_b_skills
print(f"  Intersection (&):         {shared_skills}")

# Difference (-): In A but not in B
unique_to_a = team_a_skills - team_b_skills
print(f"  Difference (A - B):       {unique_to_a}")

# Symmetric Difference (^): In either A or B, but not both
symmetric_diff = team_a_skills ^ team_b_skills
print(f"  Symmetric Difference (^): {symmetric_diff}")


# -----------------------------------------------------------------------------
# Section 4: Dictionaries — Key-Value Mappings
# -----------------------------------------------------------------------------
# Dictionaries map unique, immutable keys to arbitrary values.
# In Python 3.7+, dictionaries maintain insertion order.

print("\n--- [Section 4: Dictionaries — Key-Value Mappings] ---")

agent_profile = {
    "agent_id": "agent-007",
    "model": "gpt-4o",
    "temperature": 0.2,
    "max_retries": 3,
    "is_enabled": True,
}

print("Agent Profile dictionary:")
for k, v in agent_profile.items():
    print(f"  {k:<14}: {v}")

# Safe lookups using .get():
# Direct indexing d["missing"] raises KeyError! .get() returns default.
timeout_val = agent_profile.get("timeout_sec", 60)
print(f"\nSafe lookup for 'timeout_sec': {timeout_val} (used fallback default 60)")

# Updating and popping:
agent_profile.update({"temperature": 0.5, "timeout_sec": 45})
removed_retries = agent_profile.pop("max_retries")
print(f"Popped 'max_retries': {removed_retries}")
print(f"Updated profile: {agent_profile}")

# Dictionary views:
print(f"Keys view:   {list(agent_profile.keys())}")
print(f"Values view: {list(agent_profile.values())}")


# -----------------------------------------------------------------------------
# Section 5: Hashability & Dictionary Keys
# -----------------------------------------------------------------------------
# In Python, an object is hashable if it has an invariant hash value.
# Only immutable objects (int, float, str, tuple of immutables) can be dict keys or set items.

print("\n--- [Section 5: Hashability & Dictionary Keys] ---")

valid_key_int = 100
valid_key_str = "coordinates"
valid_key_tuple = (10, 20)

sample_dict = {
    valid_key_int: "integer key",
    valid_key_str: "string key",
    valid_key_tuple: "tuple key",
}
print(f"Sample dict with hashable keys: {sample_dict}")
print(f"Hash value of tuple (10, 20): {hash(valid_key_tuple)}")

try:
    # Lists are mutable and unhashable:
    sample_dict[[1, 2]] = "list key"
except TypeError as err:
    print(f"Caught expected TypeError: {err}")
    print("Lists cannot be dictionary keys because they are mutable!")


# -----------------------------------------------------------------------------
# Section 6: Mutability and The Reference Aliasing Trap
# -----------------------------------------------------------------------------
# Assigning a variable does NOT copy the container; it creates an alias!
# Always use .copy() or copy.deepcopy() when independent copies are needed.

print("\n--- [Section 6: The Aliasing Trap vs. Deep Copying] ---")

# The Aliasing Trap:
original_list = [1, 2, [3, 4]]
alias_list = original_list  # Same reference!
alias_list.append(5)

print(f"After modifying alias_list:")
print(f"  original_list: {original_list} (Modified!)")
print(f"  alias_list:    {alias_list}")
print(f"  original_list is alias_list? {original_list is alias_list}")

# Shallow copy vs Deep copy:
shallow_copied = original_list.copy()
deep_copied = copy.deepcopy(original_list)

# Modifying the nested list inside shallow copy:
shallow_copied[2].append(999)
print(f"\nAfter mutating nested list inside shallow copy:")
print(f"  original_list:  {original_list} (Nested element was mutated!)")
print(f"  shallow_copied: {shallow_copied}")
print(f"  deep_copied:    {deep_copied} (Completely isolated!)")


# -----------------------------------------------------------------------------
# Section 7: Performance Trade-offs: List vs. Set/Dict Lookups
# -----------------------------------------------------------------------------
# 'item in list' is O(N) linear time search.
# 'item in set' or 'key in dict' is O(1) constant time hash lookup.

print("\n--- [Section 7: Performance — O(N) vs. O(1) Membership] ---")

large_list = list(range(100_000))
large_set = set(large_list)
target_item = 99_999

# Time list lookup:
t0 = time.perf_counter()
found_in_list = target_item in large_list
t_list = (time.perf_counter() - t0) * 1000

# Time set lookup:
t0 = time.perf_counter()
found_in_set = target_item in large_set
t_set = (time.perf_counter() - t0) * 1000

print(f"Lookup {target_item} in 100,000 items:")
print(f"  List lookup (O(N)): {t_list:.4f} ms")
print(f"  Set lookup  (O(1)): {t_set:.4f} ms")
print("  Rule: For high-frequency membership testing, always use sets!")


# -----------------------------------------------------------------------------
# Section 8: Real-World Scenario — AI Agent Architecture
# -----------------------------------------------------------------------------
# Practical architecture integrating all 4 collections:
# - List: Message history
# - Set: Visited URLs / Nodes
# - Tuple: Execution coordinate / Model configuration
# - Dict: Tool registry

print("\n--- [Section 8: Autonomous Agent Architecture Integration] ---")

class MiniAgentSession:
    def __init__(self, agent_name: str, model_config: tuple):
        # Tuple: Immutable configuration
        self.model_name, self.temperature, self.seed = model_config
        self.agent_name = agent_name

        # List: Sequential conversation history
        self.history = [
            {"role": "system", "content": f"You are {agent_name} running {self.model_name}."}
        ]

        # Set: Visited documents / URL deduplication
        self.visited_ids = set()

        # Dict: Tool registry
        self.tool_registry = {}

    def register_tool(self, name: str, description: str, handler):
        """Registers a callable tool in the agent dictionary."""
        self.tool_registry[name] = {"description": description, "handler": handler}

    def add_user_message(self, text: str):
        """Appends a user message to the conversation list."""
        self.history.append({"role": "user", "content": text})

    def execute_tool(self, tool_name: str, argument: str) -> str:
        """Executes a registered tool if authorized."""
        if tool_name not in self.tool_registry:
            raise KeyError(f"Tool '{tool_name}' is not registered.")
        handler = self.tool_registry[tool_name]["handler"]
        result = handler(argument)
        self.history.append({"role": "tool", "name": tool_name, "content": result})
        return result

    def trim_history(self, max_messages: int):
        """Trims context window keeping system prompt and most recent messages."""
        if len(self.history) > max_messages:
            system_msg = self.history[0]
            recent_msgs = self.history[-(max_messages - 1):]
            self.history = [system_msg] + recent_msgs


# Instantiate and test the Agent session:
session = MiniAgentSession("DataAgent", ("claude-3-5-sonnet", 0.1, 42))
session.register_tool("echo", "Echos back text", lambda s: f"ECHO: {s}")
session.register_tool("length", "Counts characters", lambda s: str(len(s)))

session.add_user_message("Analyze system metrics.")
out1 = session.execute_tool("echo", "System OK")
out2 = session.execute_tool("length", "System OK")

print(f"Agent configured: {session.agent_name} using {session.model_name}")
print(f"Registered tools: {list(session.tool_registry.keys())}")
print(f"Total messages in history: {len(session.history)}")
for msg in session.history:
    print(f"  [{msg.get('role').upper()}]: {msg.get('content')}")

print("\n" + "=" * 75)
print("LESSON COMPLETE: Python Collections successfully demonstrated.")
print("=" * 75)
