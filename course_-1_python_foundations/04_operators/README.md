# Topic: Python Operators

## What You Will Learn
- Complete mastery of Python's arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`), including true division vs. floor division.
- Comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) and Python's distinctive chained comparison syntax.
- Logical operators (`and`, `or`, `not`) and the exact mechanics of short-circuit evaluation.
- Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`) for permission masks and low-level binary state flags.
- Membership (`in`, `not in`) and identity (`is`, `is not`) operators.
- Augmented assignment operators (`+=`, `-=`, etc.) and operational side-effects.
- Operator precedence rules and how to write clean, unambiguous expressions with parentheses.
- How AI agents use operators for confidence gating, token budget rationing, short-circuit guardrails, and role-based access control.

## Prerequisites
- Completion of Module 03 ("Variables and Data Types").
- Understanding of primitive types (`int`, `float`, `bool`, `str`, `NoneType`).
- Basic arithmetic knowledge (addition, multiplication, powers, remainders).

## The Problem
Storing data in variables is useless if a program cannot compute, compare, or decide. A navigation app must calculate the remaining distance between coordinates. A security system must verify if a user's age is greater than 18 *and* their account is active. A game loop must decrement health points when damage occurs.

Without operators, programs would be static catalogs of unchanging values. Furthermore, subtle differences in how operators behave can introduce catastrophic bugs:
- Does `7 / 2` give `3.5` or `3`?
- What does `-7 // 2` evaluate to?
- Why does `False or "fallback"` return the string `"fallback"` instead of a boolean?
- When does Python stop evaluating a compound boolean condition?

Mastering operators allows you to transform raw state into meaningful computational decisions with mathematical certainty.

## Key Terminology
- **Operator**: A dedicated syntactic symbol or keyword that directs the interpreter to perform a specific mathematical, logical, or relational manipulation on data.
- **Operand**: The data value or expression on which an operator acts (e.g., in `a + b`, `+` is the operator; `a` and `b` are operands).
- **True Division (`/`)**: Division that always produces a floating-point result, even if the operands divide evenly (e.g., `4 / 2` yields `2.0`).
- **Floor Division (`//`)**: Division that rounds the quotient downwards towards negative infinity, returning the largest integer less than or equal to the mathematical result.
- **Modulo (`%`)**: The remainder operator yielding the arithmetic remainder after floor division ($a \% b = a - (a // b) \times b$).
- **Short-Circuit Evaluation**: The property of logical operators (`and`, `or`) where the second operand is never evaluated if the first operand is sufficient to determine the overall outcome.
- **Chained Comparison**: A syntactic elegance of Python allowing expressions like `0 <= x <= 100`, evaluated as `(0 <= x) and (x <= 100)` without evaluating `x` twice.
- **Bitwise Mask**: An integer whose individual bits represent boolean flags or permissions, manipulated with binary logic (`&`, `|`, `^`, `~`).
- **Precedence**: The rules determining the order in which different operators are evaluated in a complex compound expression (like PEMDAS in algebra).

## Intuition
Think of operators as specialized tools in an automated factory assembly line:
1. **Arithmetic Operators** are the heavy machinery: cutting material in half (`/`), stamping repeated parts (`*`), or counting leftover scrap (`%`).
2. **Comparison Operators** are quality-control sensors: measuring whether a part's weight matches specifications (`==`), is too light (`<`), or exceeds tolerances (`>`). They emit a green light (`True`) or red light (`False`).
3. **Logical Operators** are safety circuits: an emergency shutoff triggers if the sensor detects an obstruction *OR* the emergency button is pressed. The safety circuit is efficient: if the first condition is already triggered, it doesn't bother waiting to read the secondary sensor (short-circuiting).
4. **Bitwise Operators** are a row of toggle switches on the control panel: flipping specific bits on or off to enable power, cooling, or alarms using compact binary codes.

## Concept

### 1. Arithmetic Operators
- Addition: `a + b`
- Subtraction: `a - b`
- Multiplication: `a * b`
- True Division: `a / b` (always produces `float`)
- Floor Division: `a // b` (rounds toward $-\infty$)
  - `7 // 2` is `3`
  - `-7 // 2` is `-4` (rounds down, away from zero!)
- Modulo (Remainder): `a % b`
  - Useful for cycle wraps, clocks, and checking even/odd (`x % 2 == 0`)
- Exponentiation: `a ** b` ($a^b$)

### 2. Comparison Operators
Always evaluate to a boolean (`True` or `False`):
- Equal to: `a == b` (checks value equality)
- Not equal to: `a != b`
- Greater than: `a > b`
- Less than: `a < b`
- Greater than or equal: `a >= b`
- Less than or equal: `a <= b`
- Chained comparisons: `10 < score <= 100`

### 3. Logical (Boolean) Operators & Short-Circuiting
Python's logical operators do not merely return `True` or `False`; **they return the operand that determined the result**:
- `x and y`: If `x` is falsy, returns `x` immediately without evaluating `y`. Otherwise, returns `y`.
- `x or y`: If `x` is truthy, returns `x` immediately without evaluating `y`. Otherwise, returns `y`.
- `not x`: Returns `True` if `x` is falsy, `False` if `x` is truthy.

```python
# Default value fallback idiom using short-circuit 'or':
username = input_name or "Guest"
```

### 4. Bitwise Operators
Operate directly on the two's complement binary representation of integers:
- AND (`&`): Bit is 1 if both bits are 1.
- OR (`|`): Bit is 1 if either bit is 1.
- XOR (`^`): Bit is 1 if exactly one bit is 1.
- NOT (`~`): Inverts all bits ($\sim x = -x - 1$).
- Left Shift (`<<`): Shifts bits left by $n$ positions ($x \times 2^n$).
- Right Shift (`>>`): Shifts bits right by $n$ positions ($x // 2^n$).

### 5. Membership and Identity Operators
- Membership: `x in sequence`, `x not in sequence`
- Identity: `x is y`, `x is not y`

## Syntax
```python
# Arithmetic
total = (base_cost * quantity) + shipping_fee
average = total / count
remaining = total % batch_size
squared = radius ** 2

# Comparison & Chaining
is_valid_range = 0.0 <= confidence <= 1.0
has_changed = old_state != new_state

# Logical & Short-Circuiting
can_proceed = is_logged_in and (has_permission or is_admin)
default_agent = preferred_model or "claude-3-haiku"

# Augmented Assignment
token_count += 150   # Equivalent to token_count = token_count + 150
score -= 10
budget *= 0.95

# Bitwise Permissions (Flags)
READ = 1 << 0   # 1  (0b001)
WRITE = 1 << 1  # 2  (0b010)
EXEC = 1 << 2   # 4  (0b100)

user_perms = READ | WRITE       # 3 (0b011)
can_write = bool(user_perms & WRITE)  # True
```

## Example
Here is a comprehensive script demonstrating operator categories, short-circuit execution, and an AI agent token-budgeting and permission validator:

```python
# Agent Resource & Guardrail Evaluator

# 1. Arithmetic & Token Budgeting
max_context_tokens = 8192
prompt_tokens = 1450
completion_reserve = 2000

used_tokens = prompt_tokens + completion_reserve
remaining_tokens = max_context_tokens - used_tokens
pct_used = (used_tokens / max_context_tokens) * 100

print(f"Used Tokens: {used_tokens}/{max_context_tokens} ({pct_used:.2f}%)")
print(f"Remaining Tokens: {remaining_tokens}")

# 2. Comparison & Chaining
is_within_budget = 0 <= used_tokens <= max_context_tokens
print(f"Budget Check: {is_within_budget}")

# 3. Short-Circuit Safety Guard
# We only inspect detailed results if the query executed without errors:
agent_success = True
agent_results = {"output": "42"}

# If agent_success is False, agent_results["output"] is never accessed!
result_preview = agent_success and agent_results["output"]
print(f"Result Preview: {result_preview}")

# 4. Bitwise Access Control (RBAC)
PERM_READ = 1 << 0    # 1
PERM_WRITE = 1 << 1   # 2
PERM_EXEC = 1 << 2    # 4

agent_role_perms = PERM_READ | PERM_EXEC  # 5 (Read + Execute)
requested_action = PERM_WRITE

has_access = bool(agent_role_perms & requested_action)
print(f"Can agent execute WRITE? {has_access}")
```

## Line-by-Line Explanation
- `used_tokens = prompt_tokens + completion_reserve`: Uses the `+` arithmetic operator to sum two integers (`1450 + 2000 = 3450`).
- `remaining_tokens = max_context_tokens - used_tokens`: Uses `-` to compute available margin (`8192 - 3450 = 4742`).
- `pct_used = (used_tokens / max_context_tokens) * 100`: Uses true division `/` to yield a float ratio (`0.4211...`), multiplied by `100` via `*`. Parentheses ensure division happens before multiplication.
- `0 <= used_tokens <= max_context_tokens`: Evaluates a chained comparison equivalent to `(0 <= used_tokens) and (used_tokens <= max_context_tokens)`.
- `result_preview = agent_success and agent_results["output"]`: Demonstrates short-circuit evaluation. Because `agent_success` is `True`, `and` evaluates and returns the second operand (`"42"`).
- `PERM_READ = 1 << 0`: Uses the bitwise left-shift operator `<<` to compute $1 \times 2^0 = 1$.
- `agent_role_perms = PERM_READ | PERM_EXEC`: Uses bitwise OR `|` to combine flags `1 | 4 = 5` (`0b101`).
- `bool(agent_role_perms & requested_action)`: Uses bitwise AND `&` to mask permissions (`5 & 2 = 0`), which casts to `False`.

## What Python Is Doing
1. **Dunder Method Dispatch**: Python operators are syntactic sugar for special "dunder" (double underscore) methods on objects:
   - `a + b` invokes `a.__add__(b)` (or `b.__radd__(a)` if `a` does not support it).
   - `a == b` invokes `a.__eq__(b)`.
   - `a // b` invokes `a.__floordiv__(b)`.
   - `a & b` invokes `a.__and__(b)`.
2. **Short-Circuit Bytecode Optimization**:
   When Python compiles an `and` or `or` expression to bytecode, it emits conditional jump instructions (`JUMP_IF_FALSE_OR_POP` or `JUMP_IF_TRUE_OR_POP`). If the left operand satisfies the condition, the jump skips the right operand's bytecode instructions entirely.
3. **Chained Comparison Expansion**:
   In `a < b < c`, Python compiles code that evaluates `a`, evaluates `b`, tests `a < b`; if false, jumps out immediately; if true, compares `b` to `c` without evaluating `b` a second time.

## Common Mistakes
1. **Confusing True Division (`/`) with Floor Division (`//`)**:
   ```python
   x = 10 / 2   # Returns 5.0 (a float!), not integer 5
   y = 10 // 2  # Returns 5 (an integer)
   ```
2. **Floor Division with Negative Numbers**:
   ```python
   print(7 // 2)   # 3
   print(-7 // 2)  # -4 (not -3! Floor division rounds towards negative infinity)
   ```
3. **Order of Precedence in Boolean Expressions**:
   In Python, `not` has highest precedence, followed by `and`, followed by `or`.
   ```python
   # False and False or True evaluates as ((False and False) or True) -> True!
   # Always use parentheses to make intent explicit:
   is_valid = (condition_a and condition_b) or condition_c
   ```
4. **Expecting `and` / `or` to Always Return `bool`**:
   ```python
   val = [] or "default"  # Returns "default", NOT True!
   val2 = 0 and "something"  # Returns 0, NOT False!
   ```

## Real-World Uses
- **Financial Calculations**: Computing compound interest ($P(1 + r/n)^{nt}$) with `**` and division.
- **Pagination**: Calculating total pages from item counts using ceiling math via floor division: `total_pages = (items + page_size - 1) // page_size`.
- **Game Physics**: Checking collision boundaries with chained comparisons: `x_min <= player_x <= x_max`.
- **System Administration**: Managing Unix file permissions (`chmod 755`) using octal bitwise masks (`rwxr-xr-x`).

## Connection to AI Agents
Operators are essential for controlling agent behavior and resource management:
- **Decision Guardrails**: Agents use compound comparisons (`min_confidence <= model_score and latency_ms < 500`) to decide whether to trust an LLM response or invoke a fallback tool.
- **Short-Circuit Fallbacks**: Using `model_response or retrieve_cached_answer()` prevents slow, expensive API calls when cached responses exist.
- **Token Budget Rationing**: Floor division (`budget // max_agent_turns`) allocates exact token quotas per step.
- **Tool Access Control**: Bitwise flags encode agent capabilities (e.g. `CAN_SHELL | CAN_SQL | CAN_FILE`). A security layer inspects `agent_caps & TOOL_PERM` before executing dangerous tools.

## Practice
1. Evaluate `15 % 4`, `15 // 4`, and `15 / 4` in Python. Note their exact return types.
2. Experiment with chained comparisons: test whether `10 <= 25 < 50` is `True`.
3. Test short-circuit behavior: create a variable `x = None` and evaluate `x is not None and len(x) > 0`. Notice that it does not crash because `len(x)` is never reached!
4. Calculate powers: compute $2^{16}$ using `**`.
5. Combine bitwise flags: create `FLAG_A = 1`, `FLAG_B = 2`, `FLAG_C = 4`. Combine all three into `flags = FLAG_A | FLAG_B | FLAG_C` and verify that `flags & FLAG_B` is non-zero.

## Challenge
Write a small pure-Python expression or function that:
1. Computes the ceiling division of two positive integers $a$ and $b$ (i.e. $\lceil a / b \rceil$) using ONLY the basic arithmetic operators `+`, `//`, or `%` (without importing `math.ceil`).
2. Implement a safe dict lookup `data and data.get("user") and data["user"].get("role")` relying strictly on short-circuit evaluation to prevent `AttributeError` or `TypeError`.
3. Use bitwise operations to toggle a specific permission bit on and off without modifying any other bits in the mask.

## Summary
- Arithmetic operators include true division `/` (float) and floor division `//` (integer rounded to $-\infty$).
- Modulo `%` calculates remainder; `**` computes exponentiation.
- Comparisons return booleans and support Python's elegant chaining syntax (`0 <= x <= 100`).
- Logical operators `and` and `or` short-circuit and return the decisive operand rather than converting to a boolean.
- Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`) manipulate binary representations of integers.
- Parentheses eliminate ambiguity in complex expressions and should always be preferred over relying on implicit precedence.

## What You Should Know Before Moving On
Before advancing to Module 05 ("Strings"), verify that you can:
- Explain why `7 // 2` is `3` while `-7 // 2` is `-4`.
- Explain how short-circuit evaluation prevents runtime errors like `data is not None and data["key"] == 5`.
- Construct and inspect permission masks using bitwise `|` and `&`.
- Use augmented assignment operators (`+=`, `*=`) correctly.
- Explain how an AI agent uses operators to budget tokens and gate tool execution.
