"""
Module 07: Control Flow — Conditionals, Loops, and Decision Logic in Python
==========================================================================

Control flow is how a program decides what instructions to execute, when to repeat
them, and when to halt. Without control flow, programs would execute linearly from top
to bottom like a rigid grocery list. With control flow, your code can evaluate dynamic
conditions, respond to user inputs, process streams of data, and implement autonomous
decision cycles (the heartbeat of AI agents).

This lesson explores:
  1. Truthiness and Boolean Expressions
  2. Conditional Branching (if, elif, else)
  3. Conditional Expressions (Ternary Operator)
  4. Definite Iteration (for loops, range, sequence traversal)
  5. Loop Utilities (enumerate, zip)
  6. Indefinite Iteration (while loops, sentinel patterns)
  7. Loop Control (break, continue, pass)
  8. The `for...else` and `while...else` Constructs
  9. Real-World AI Agent Decision & Dispatch Loop
"""

print("=" * 70)
print("MODULE 07: CONTROL FLOW IN PYTHON")
print("=" * 70)


# ==============================================================================
# SECTION 1: Truthiness and Boolean Expressions
# ==============================================================================
print("\n--- 1. Truthiness and Boolean Evaluations ---")

# In Python, any object can be tested for truth value (truthiness).
# The following values are considered FALSY:
#   - None
#   - False
#   - Zero of any numeric type: 0, 0.0, 0j
#   - Any empty sequence or collection: '', (), [], {}, set(), range(0)
# Everything else is considered TRUTHY.

falsy_candidates = [None, False, 0, 0.0, "", [], {}, set()]
print("Demonstrating falsy values:")
for item in falsy_candidates:
    is_truthy = bool(item)
    print(f"  Value: {repr(item):<10} -> bool(): {is_truthy}")

# Truthiness allows elegant, idiomatic checks without explicit comparisons:
user_prompt = ""
if not user_prompt:
    print("  Prompt is empty! (Checked using `not user_prompt` idiomatic truthiness)")

user_prompt = "What is the capital of France?"
if user_prompt:
    print(f"  Prompt received: '{user_prompt}' (Truthy string)")


# ==============================================================================
# SECTION 2: Conditional Branching (if, elif, else)
# ==============================================================================
print("\n--- 2. Conditional Branching (if / elif / else) ---")

# Python evaluates branches sequentially from top to bottom.
# As soon as one branch evaluates to True, its block runs, and Python skips all
# subsequent elif and else branches.

confidence_score = 0.82

print(f"Evaluating agent confidence score: {confidence_score}")
if confidence_score >= 0.90:
    action = "Execute action directly without verification"
elif confidence_score >= 0.70:
    action = "Execute action and log reasoning for audit"
elif confidence_score >= 0.40:
    action = "Ask user for confirmation before proceeding"
else:
    action = "Reject proposal; confidence too low"

print(f"  Decision outcome: {action}")

# Nested conditionals allow hierarchical reasoning:
tool_available = True
rate_limit_exceeded = False

if tool_available:
    if not rate_limit_exceeded:
        print("  Status: Tool is ready and rate limit is within bounds.")
    else:
        print("  Status: Tool available, but rate limit hit. Backing off.")
else:
    print("  Status: Tool not found in registry.")


# ==============================================================================
# SECTION 3: Conditional Expressions (Ternary Operator)
# ==============================================================================
print("\n--- 3. Conditional Expressions (Ternary Operator) ---")

# Syntax: <value_if_true> if <condition> else <value_if_false>
# Useful for concise variable assignments based on a single condition.

token_count = 3500
token_limit = 4096

context_status = "CRITICAL" if token_count > 3000 else "NORMAL"
print(f"Tokens: {token_count}/{token_limit} -> Status: {context_status}")

# Safe division example:
items_processed = 0
total_duration = 12.5
items_per_second = (items_processed / total_duration) if total_duration > 0 else 0.0
print(f"Processing throughput: {items_per_second:.2f} items/sec")


# ==============================================================================
# SECTION 4: Definite Iteration (for loops and range)
# ==============================================================================
print("\n--- 4. Definite Iteration (for loops) ---")

# `range(start, stop, step)` generates integers up to but excluding stop:
print("Counting steps with range(1, 6):")
for step_num in range(1, 6):
    print(f"  Processing step {step_num}")

# Traversing collections directly (no indexing required):
agent_roles = ["planner", "coder", "reviewer", "tester"]
print("\nIterating over list of roles:")
for role in agent_roles:
    print(f"  Active agent role: {role.upper()}")

# Iterating over key-value pairs in a dictionary:
tool_registry = {
    "calculator": "Performs arithmetic expressions",
    "web_search": "Retrieves real-time search engine results",
    "file_reader": "Reads raw text from local filesystem"
}

print("\nIterating over tool dictionary items:")
for tool_name, tool_desc in tool_registry.items():
    print(f"  Tool [{tool_name}]: {tool_desc}")


# ==============================================================================
# SECTION 5: Loop Utilities (enumerate and zip)
# ==============================================================================
print("\n--- 5. Loop Utilities: enumerate() and zip() ---")

# `enumerate(iterable, start=0)` gives both index and value:
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain binary search."},
    {"role": "assistant", "content": "Binary search is a divide-and-conquer algorithm..."}
]

print("Indexed conversation history using enumerate():")
for idx, msg in enumerate(messages, start=1):
    print(f"  [{idx}] {msg['role'].upper()}: {msg['content'][:30]}...")

# `zip(*iterables)` pairs items from multiple iterables element-by-element:
model_names = ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"]
context_windows = [128000, 200000, 1000000]
cost_per_m_tokens = [5.00, 3.00, 3.50]

print("\nCombining model specs using zip():")
for model, window, cost in zip(model_names, context_windows, cost_per_m_tokens):
    print(f"  Model: {model:<18} | Window: {window:>7,} tokens | Cost: ${cost:.2f}/M")


# ==============================================================================
# SECTION 6: Indefinite Iteration (while loops)
# ==============================================================================
print("\n--- 6. Indefinite Iteration (while loops) ---")

# `while` repeats as long as its condition evaluates to True.
# Always ensure the loop variable changes toward termination to prevent infinite loops!

retry_attempt = 0
max_retries = 3
simulated_network_success = False

print("Simulating retry loop with exponential backoff:")
while retry_attempt < max_retries:
    retry_attempt += 1
    backoff_delay = 2 ** (retry_attempt - 1)
    print(f"  Attempt {retry_attempt}/{max_retries} (Backoff: {backoff_delay}s)...")
    
    # Simulate success on the 3rd attempt:
    if retry_attempt == 3:
        simulated_network_success = True
        print("  -> Connection established successfully!")
        break

if not simulated_network_success:
    print("  -> Network request failed after all attempts.")


# ==============================================================================
# SECTION 7: Loop Control Statements (break, continue, pass)
# ==============================================================================
print("\n--- 7. Loop Control (break, continue, pass) ---")

# `break`: Immediately exits the nearest enclosing loop.
# `continue`: Skips the rest of the current iteration and jumps to the next.
# `pass`: Null statement (placeholder that does nothing).

task_queue = [
    {"task_id": "T1", "type": "valid", "payload": "Analyze log file"},
    {"task_id": "T2", "type": "heartbeat", "payload": "ping"},
    {"task_id": "T3", "type": "poison_pill", "payload": "FATAL: shutdown command"},
    {"task_id": "T4", "type": "valid", "payload": "Generate summary report"}
]

print("Processing task queue with break and continue:")
for task in task_queue:
    if task["type"] == "heartbeat":
        # Skip heartbeat pings without terminating loop
        print(f"  [Task {task['task_id']}] Heartbeat received -> skipping via `continue`")
        continue

    if task["type"] == "poison_pill":
        # Emergency stop
        print(f"  [Task {task['task_id']}] Poison pill encountered -> halting loop via `break`!")
        break

    print(f"  [Task {task['task_id']}] Executed: {task['payload']}")


# ==============================================================================
# SECTION 8: Loop else Clause (for...else and while...else)
# ==============================================================================
print("\n--- 8. The `for...else` Construct ---")

# In Python, an `else` block attached to a loop executes ONLY IF the loop
# completes naturally (without being interrupted by a `break` statement).
# This eliminates clunky boolean flag variables like `found = False`.

def search_tool_in_catalog(target_tool: str, catalog: list[str]) -> None:
    print(f"Searching for '{target_tool}' in catalog...")
    for item in catalog:
        if item == target_tool:
            print(f"  -> Found '{target_tool}'! Immediate break.")
            break
    else:
        # Runs ONLY if the loop ran to completion without hitting `break`:
        print(f"  -> Notice: '{target_tool}' was NOT found in the catalog (loop else triggered).")

sample_catalog = ["code_interpreter", "web_browser", "sql_executor"]
search_tool_in_catalog("web_browser", sample_catalog)
search_tool_in_catalog("image_generator", sample_catalog)


# ==============================================================================
# SECTION 9: Comprehensive AI Agent Reasoning & Execution Loop
# ==============================================================================
print("\n--- 9. Real-World AI Agent ReAct Decision Loop ---")

# A typical autonomous AI agent runs in an observation-thought-action loop.
# It iteratively calls tools until it reaches the goal or exhausts its step budget.

max_iterations = 5
step = 0
agent_memory = []
goal_achieved = False

simulated_tool_responses = {
    1: {"thought": "I need to inspect the database schema.", "action": "inspect_schema", "result": "Table: users(id, name, email)"},
    2: {"thought": "I need to query active user count.", "action": "run_sql", "result": "COUNT = 42"},
    3: {"thought": "I now have the answer to user's question.", "action": "finish", "result": "There are 42 active users."}
}

print("Initiating autonomous agent ReAct loop:")
while step < max_iterations:
    step += 1
    print(f"\n[Agent Step {step}/{max_iterations}]")
    
    agent_step_data = simulated_tool_responses.get(step)
    if not agent_step_data:
        print("  No further actions produced by reasoning engine.")
        break

    print(f"  Thought: {agent_step_data['thought']}")
    print(f"  Action : {agent_step_data['action']}")
    
    # Branching based on action type:
    if agent_step_data["action"] == "finish":
        print(f"  Final Answer: {agent_step_data['result']}")
        goal_achieved = True
        break
    else:
        agent_memory.append(agent_step_data["result"])
        print(f"  Observation logged: {agent_step_data['result']}")

if goal_achieved:
    print("\nAgent finished successfully within iteration budget.")
else:
    print("\nWarning: Agent reached maximum iterations without completing the goal.")

print("\n" + "=" * 70)
print("MODULE 07 LESSON COMPLETE — ALL FLOW SAMPLES EXECUTED SUCCESSFULLY")
print("=" * 70)
