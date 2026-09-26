# Control Flow in Python

## What You Will Learn
In this module, you will master Python's control flow mechanisms:
- How Python evaluates truthiness across all fundamental data types.
- How to make decisions using `if`, `elif`, and `else` conditional blocks.
- How to write compact conditional expressions (ternary operators).
- How to perform definite iteration over sequences and ranges using `for` loops.
- How to pair indices and values using `enumerate()` and aggregate parallel lists using `zip()`.
- How to handle indefinite iteration safely using `while` loops without creating infinite execution locks.
- How to fine-tune loop behavior with `break`, `continue`, and `pass`.
- How Python's unique `for...else` and `while...else` constructs work and why they eliminate clunky boolean flag variables.
- How autonomous AI agents use control flow to implement observe-think-act reasoning cycles.

## Prerequisites
Before beginning this module, you should be comfortable with:
- Basic Python syntax and variable assignment (`x = 10`).
- Core data types: integers, floats, strings, booleans, lists, and dictionaries.
- Comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) and boolean logic (`and`, `or`, `not`).

## The Problem
A program without control flow is a straight highway: it starts at line 1, executes line 2, line 3, and terminates at the bottom. While predictable, a strictly linear script is helpless in the real world:
- It cannot adapt when a web server responds with an HTTP 429 "Rate Limit Exceeded" instead of HTTP 200 "OK".
- It cannot parse a batch of 10,000 documents without repeating the exact same code 10,000 times.
- It cannot build an AI agent that monitors incoming user messages, decides which tool to invoke, re-tries failed network queries, or terminates when a goal is satisfied.

Real programs must diverge, loop, pause, and recover based on changing inputs and environmental conditions. Control flow provides the nervous system that transforms static scripts into adaptive, intelligent software.

## Key Terminology
- **Control Flow**: The order in which individual statements, instructions, or function calls are executed or evaluated in a program.
- **Branching**: Directing program execution along one of multiple distinct paths based on the evaluation of a boolean condition.
- **Truthiness**: The boolean value (`True` or `False`) that an arbitrary Python object resolves to when evaluated in a conditional context.
- **Iteration**: The repetition of a sequence of computer programming instructions, either a specified number of times (definite) or until a condition is met (indefinite).
- **Iterable**: Any Python object capable of returning its members one at a time (e.g., lists, strings, tuples, dictionaries, generators).
- **Sentinel Value**: A special value in a loop condition used to signal termination (e.g., encountering `None` or a `STOP` token).
- **Short-Circuit Evaluation**: The stopping of boolean expression evaluation as soon as the outcome is guaranteed (e.g., `False and expensive_function()` never executes the function).

## Intuition
Think of your code as a traveler standing before a junction in the woods:
- An **`if / elif / else`** statement is a road sign at a fork. Depending on the traveler's supplies (your variables), they take the left path, the middle trail, or the right detour. They only walk down **one** of those paths.
- A **`for` loop** is walking down an orchard with a basket, stopping at every apple tree in line to pick a fruit until no trees remain.
- A **`while` loop** is walking on a treadmill with your eyes on a timer; you keep jogging until the timer rings or someone pulls the emergency stop cord (`break`).
- A **`break`** is an emergency fire exit: you abandon whatever room you are in immediately.
- A **`continue`** is noticing a broken stair: you skip that one single step and immediately leap to the next stair.

## Concept
Python manages control flow through lexical indentation (four spaces per block level) and condition-driven branch statements.

### 1. The Rules of Truthiness
In Python, you don't need to write `if len(my_list) > 0:` or `if my_string != "":`. Every object inherently evaluates to either `True` or `False`:
- **Falsy**: `None`, `False`, numeric zeros (`0`, `0.0`), empty sequences/collections (`""`, `[]`, `()`, `{}`).
- **Truthy**: Non-zero numbers, non-empty strings, collections with at least one item, and user-defined objects by default.

### 2. Sequential Branching
When Python encounters an `if / elif / else` chain, it tests conditions from top to bottom. As soon as a condition yields `True`, that block executes, and all remaining branches are skipped entirely. If none match, the optional `else` block acts as the default fallback.

### 3. Loop Structures
- **`for item in iterable:`** Definite iteration. Python requests an iterator from the object and advances it until the iterator raises `StopIteration`.
- **`while condition:`** Indefinite iteration. Python re-evaluates the boolean condition before every single cycle. If the condition never becomes falsy and no `break` is executed, the program enters an infinite loop.

### 4. The Loop `else` Clause
Unlike languages like C, Java, or JavaScript, Python allows an `else` block directly on `for` and `while` loops. The loop `else` runs **only if the loop finished naturally without hitting a `break`**. If the loop terminates via `break`, the `else` block is bypassed.

## Syntax

```python
# 1. Conditionals
if condition_a:
    # Executes if condition_a is truthy
    do_something()
elif condition_b:
    # Executes if condition_a was falsy and condition_b is truthy
    do_other_thing()
else:
    # Executes if all preceding conditions were falsy
    fallback()

# 2. Ternary Operator (Conditional Expression)
result = "success" if code == 200 else "error"

# 3. For Loop with range and enumerate
for idx, item in enumerate(my_list, start=1):
    print(f"Item {idx}: {item}")

# 4. While Loop with break and continue
while is_running:
    if should_skip:
        continue
    if should_stop:
        break

# 5. Loop else Clause
for item in search_space:
    if item == target:
        print("Found target!")
        break
else:
    print("Target was not found in the entire collection.")
```

## Example

```python
# Real-world agent tool dispatch simulation
def run_agent_turn(tools: list[str], requests: list[dict]) -> None:
    print(f"Available tools: {tools}")
    
    for req in requests:
        action = req.get("action")
        priority = req.get("priority", "normal")
        
        # 1. Guard check with continue
        if priority == "low":
            print(f"Skipping low-priority action: '{action}'")
            continue
            
        # 2. Search tool using for...else
        for tool in tools:
            if tool == action:
                print(f"Dispatched tool '{action}' successfully.")
                break
        else:
            print(f"Warning: Tool '{action}' not recognized in tool list!")
            
        # 3. Emergency termination check
        if req.get("critical_failure"):
            print("Critical failure detected! Aborting execution loop.")
            break

# Run demonstration
sample_tools = ["search", "calculator", "terminal"]
agent_requests = [
    {"action": "search", "priority": "high"},
    {"action": "ping", "priority": "low"},
    {"action": "database_write", "priority": "high"},
    {"action": "calculator", "priority": "high", "critical_failure": True},
    {"action": "terminal", "priority": "normal"}
]

run_agent_turn(sample_tools, agent_requests)
```

## Line-by-Line Explanation
1. `def run_agent_turn(tools: list[str], requests: list[dict]) -> None:`: Declares a function accepting a list of available tool names and a list of request dictionaries.
2. `for req in requests:`: Initiates a definite loop over each request item in the sequence.
3. `action = req.get("action")`: Safely retrieves the action name from the dictionary.
4. `if priority == "low":`: Evaluates whether the priority equals the string `"low"`.
5. `continue`: If True, immediately skips lines 6-18 and jumps to the next iteration of the `for req in requests` loop.
6. `for tool in tools:`: An inner loop iterating over every available tool string in the `tools` list.
7. `if tool == action:`: Checks if the requested action matches the current available tool.
8. `break`: Halts the *inner* loop immediately once the tool match is confirmed.
9. `else:`: Belonging to `for tool in tools:`, this executes only if the inner loop checked all tools without hitting `break`.
10. `if req.get("critical_failure"):`: Checks whether the current request contains a truthy `critical_failure` flag.
11. `break`: Halts the *outer* loop immediately, preventing any remaining requests from processing.

## What Python Is Doing
Under the hood, Python compiles source code into bytecode instructions that manipulate an evaluation stack:
1. **Conditional Jumps**: An `if` statement evaluates the test expression and pushes the result onto the stack. Python executes `POP_JUMP_IF_FALSE <target_offset>`. If the value popped is falsy, the instruction pointer jumps past the block to the offset of the `elif` or `else`.
2. **Loop Iteration**: A `for` loop calls `iter(requests)` to create an iterator object. At the top of each loop, the bytecode instruction `FOR_ITER <end_offset>` calls the iterator's `__next__()` method. If elements remain, the next element is pushed onto the stack. If the iterator is exhausted (`StopIteration`), the instruction automatically jumps to the cleanup code (or the loop's `else` block).
3. **Break & Continue**: `break` translates to `JUMP_ABSOLUTE` directed to the instruction immediately following the loop (bypassing the `else` block). `continue` translates to `JUMP_ABSOLUTE` directed back to `FOR_ITER` at the top of the loop.

## Common Mistakes

### 1. Comparing Explicitly Against `True` or `False`
- **Bad**: `if is_valid == True:` or `if len(items) != 0:`
- **Good**: `if is_valid:` or `if items:`
- **Why**: Comparing with `== True` fails for truthy non-boolean values (e.g., `"hello" == True` is `False`, even though `"hello"` is truthy!).

### 2. Modifying a List While Iterating Over It
- **Bad**:
  ```python
  numbers = [1, 2, 3, 4, 5]
  for n in numbers:
      if n % 2 == 0:
          numbers.remove(n)
  ```
- **Why**: Removing elements shifts internal indices while Python's iterator counter advances, causing Python to skip elements silently.
- **Fix**: Iterate over a copy (`for n in numbers[:]:`) or use a list comprehension (`numbers = [n for n in numbers if n % 2 != 0]`).

### 3. Missing Loop Variable Updates in `while` Loops
- **Bad**:
  ```python
  attempts = 0
  while attempts < 3:
      call_api()
      # Forgot attempts += 1!
  ```
- **Why**: The loop condition never transitions to False, consuming 100% CPU in an infinite lock.

### 4. Misunderstanding the Loop `else`
- Many beginners assume `else` on a `for` loop executes if the loop never ran. In reality, it executes if the loop *completed without breaking*. If the iterable is empty, `else` **does** run!

## Real-World Uses
- **API Rate Limiter**: A `while` loop that sleeps and retries network requests with exponential backoff (`delay *= 2`) when HTTP 429 status codes occur.
- **Data Validation & Sanitization**: Filtering streams of web user input using `for` loops with `continue` guards to drop invalid records before database insertion.
- **Workflow State Machines**: Multi-branch `if/elif/else` pipelines that transition order statuses from `PENDING` -> `PAYMENT_CONFIRMED` -> `SHIPPED` -> `DELIVERED`.

## Connection to AI Agents
Autonomous AI agents are fundamentally control loops:
1. **The ReAct Agent Loop**: An agent runs a `while steps < max_step_budget:` loop. In each iteration, it:
   - Evaluates LLM output (`if action == "call_tool": ... elif action == "final_answer": break`).
   - Uses `for...else` to search the agent's registered tool schemas.
   - Evaluates token budgets with ternary conditionals: `mode = "compact" if token_count > 6000 else "verbose"`.
2. **Context Pruning**: When feeding conversation history into an LLM context window, agents iterate backwards through messages with `for msg in reversed(history):`, accumulating tokens and breaking before hitting the model's hard window limit.

## Practice
1. Write a function `is_valid_username(name: str) -> bool` that returns `True` if `name` is truthy, has between 3 and 16 characters, and contains no whitespace.
2. Use `zip()` to combine a list of agent names `["Planner", "Executor", "Auditor"]` and status codes `[200, 500, 200]`, printing only agents with status 200.
3. Write a `for...else` loop that scans a list of LLM tool response dictionaries for an error payload `{"error": True}` and prints a warning if no errors were found.

## Challenge
Implement a resilient autonomous agent step executor `execute_agent_plan(plan: list[dict], max_failures: int) -> dict`:
- Each item in `plan` has `{"step_id": int, "tool": str, "can_fail": bool}`.
- If a step fails and `can_fail` is `False`, increment a failure counter.
- If the failure counter reaches `max_failures`, break early and return a failure summary.
- If all steps execute successfully or within failure tolerances, let the loop `else` construct return a completion certificate.

## Summary
- Control flow directs programmatic execution dynamically based on runtime conditions.
- Truthiness governs how non-boolean objects resolve in conditional expressions (`0`, `""`, `[]`, `None` are falsy).
- `if/elif/else` provides mutually exclusive branch selection.
- `for` loops iterate over iterables; `enumerate()` adds 0-indexed positions; `zip()` groups multiple sequences.
- `while` loops repeat until their condition turns falsy; require careful termination guarantees.
- `break` exits a loop; `continue` skips the remaining body of the current iteration.
- `for...else` and `while...else` execute only if the loop terminates without encountering a `break`.

## What You Should Know Before Moving On
Before proceeding to Module 08 (Functions), ensure you can:
- Predict without running code whether any arbitrary Python value is truthy or falsy.
- Write nested and chained `if / elif / else` structures with correct indentation.
- Iterate over lists, dictionaries (keys, values, and items), and ranges using `for`.
- Explain exactly when a loop `else` block runs and why hitting `break` skips it.
- Implement loops with safe termination conditions, `continue` guards, and `break` triggers.
