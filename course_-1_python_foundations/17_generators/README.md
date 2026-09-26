# Topic: Generators and Lazy Evaluation

## What You Will Learn
In this module, you will master Python generators—one of the most elegant and memory-efficient features in the language. You will learn:
- The fundamental difference between eager evaluation (calculating everything upfront) and lazy evaluation (producing values on demand).
- How the `yield` keyword transforms a standard function into a stateful generator factory.
- The mechanics of generator execution, pause, and resumption across successive `next()` invocations.
- How to construct lightweight generator expressions to save memory without boilerplate code.
- How to chain multiple generators together into streaming pipelines for high-throughput, low-memory data processing.
- How autonomous AI agents use generators to stream LLM token responses in real-time and process massive log files or vector embeddings without exhausting system memory.

## Prerequisites
Before diving into generators, you should be comfortable with:
- Standard Python functions, parameter passing, and the `return` statement (Module 08).
- Basic loops (`for` and `while`) and loop iteration (Module 07).
- Collection types like lists, tuples, and dictionaries (Module 06).
- List comprehensions (Module 14).

## The Problem
Imagine you are building an AI agent that needs to analyze a 10-gigabyte telemetry file containing 50 million lines of conversation logs, or stream real-time tokens from a large language model API.

If you write a function using standard lists and `return`:
```python
def load_all_logs(filepath):
    logs = []
    with open(filepath) as f:
        for line in f:
            logs.append(line.strip())
    return logs
```
Your program attempts to allocate memory for all 50 million strings at once. On a machine with 8 GB or 16 GB of RAM, your operating system will run out of memory, crash the Python interpreter with a `MemoryError`, or grind the machine to a halt through aggressive disk swapping.

Furthermore, you cannot process the first log entry until the last log entry has been read from disk. You cannot stream the first token to a user until the AI model finishes generating the entire 4,000-word essay. Eager evaluation forces you to choose between memory exhaustion and high latency.

Generators solve both problems completely. Instead of computing all results in advance and holding them in memory, a generator computes the next item only when you ask for it.

## Key Terminology
- **Lazy Evaluation**: A programming strategy where evaluation of an expression is deferred until its value is explicitly needed by the consumer.
- **Eager Evaluation**: Computing and storing the entire result set immediately before continuing execution.
- **Generator Function**: A function that contains one or more `yield` statements. Calling it returns a generator object without executing the function body immediately.
- **Generator Object**: An iterator produced by a generator function that yields a sequence of values on demand via the iterator protocol (`__iter__()` and `__next__()`).
- **`yield` Keyword**: A Python keyword that pauses the generator function, preserves its entire local execution frame (variables, instruction pointer), and sends a value back to the caller.
- **Generator Expression**: A concise syntactic construct enclosed in parentheses `(x for x in iterable)` that produces a generator object without writing a full `def` block.
- **`StopIteration`**: The built-in exception raised by a generator or iterator when there are no further values to yield.
- **Data Pipeline**: A series of generator stages where each stage transforms or filters data yielded by the preceding stage, maintaining minimal memory overhead.

## Intuition
Think of an eager function as a baker who bakes 1,000 donuts, boxes all 1,000 donuts at once, and hands you a giant pallet of boxes. You need a massive warehouse (RAM) to store the pallet, and you have to wait an hour before you can take your very first bite.

Think of a generator as a magical conveyor belt with a button. You press the button once (`next()`). The baker immediately fries one fresh donut, places it in your hand, and pauses. The baker goes to sleep right there, holding the spatula in mid-air. Whenever you are ready for another donut, you press the button again. The baker wakes up, makes one more donut, hands it over, and pauses again.

You never need a warehouse. You only ever hold one donut at a time. If you only want three donuts, you stop pressing the button, and no ingredients or energy are wasted making the remaining 997 donuts.

## Concept
When a regular Python function executes, it receives input arguments, creates a local stack frame, runs top-to-bottom until it hits `return` (or reaches the end), destroys its stack frame, and returns a single value. Any local variables created during that call vanish forever.

A generator function works entirely differently:
1. **Compilation**: When Python compiles a function definition and detects the `yield` keyword, it marks the code object with a special flag (`CO_GENERATOR`).
2. **Invocation**: Calling the function does **not** run any code inside the body! Instead, Python immediately constructs and returns a generator object wrapping the code object and execution state.
3. **Pumping (`next()`)**: When the caller invokes `next(gen)` (or loops over it with `for item in gen:`), Python resumes execution of the generator from the exact line where it previously paused (or from the very beginning if called for the first time).
4. **Suspension (`yield`)**: When execution encounters a `yield <value>` expression, Python captures `<value>`, freezes the generator's local variables, instruction pointer, and exception handlers, and delivers `<value>` to the consumer.
5. **Termination**: When the generator function finishes executing or hits an explicit `return`, Python automatically raises `StopIteration`. A `for` loop catches this exception behind the scenes and cleanly terminates.

## Syntax
### Defining and Calling a Generator Function
```python
def count_up_to(max_val: int):
    current = 1
    while current <= max_val:
        yield current
        current += 1

# Calling does NOT run the code; it returns a generator object
counter = count_up_to(3)

# Retrieve values using next()
first = next(counter)   # 1
second = next(counter)  # 2
third = next(counter)   # 3
# next(counter)         # Raises StopIteration!
```

### Generator Expressions
Generator expressions use the same syntax as list comprehensions, but with parentheses `(...)` instead of square brackets `[...]`:
```python
# List comprehension (eager: allocates memory for 1,000,000 integers)
squares_list = [x * x for x in range(1_000_000)]

# Generator expression (lazy: allocates memory for just one generator object)
squares_gen = (x * x for x in range(1_000_000))
```

### Yield From Syntax
To delegate yielding to a sub-generator or iterable, use `yield from`:
```python
def flatten_nested(lists):
    for sublist in lists:
        yield from sublist
```

## Example
Here is a complete, runnable example contrasting an eager data loader with a lazy generator pipeline for parsing simulated server telemetry logs:

```python
import sys

def eager_log_reader(num_entries: int):
    results = []
    for i in range(num_entries):
        results.append(f"LOG_ENTRY_{i:06d}: status=200 latency={i % 50}ms")
    return results

def lazy_log_reader(num_entries: int):
    for i in range(num_entries):
        yield f"LOG_ENTRY_{i:06d}: status=200 latency={i % 50}ms"

# Eager memory footprint:
eager_data = eager_log_reader(100_000)
print(f"Eager list memory size: {sys.getsizeof(eager_data)} bytes")

# Lazy memory footprint:
lazy_data = lazy_log_reader(100_000)
print(f"Lazy generator memory size: {sys.getsizeof(lazy_data)} bytes")

# Consuming items on-demand:
for index, entry in enumerate(lazy_data):
    if index >= 3:
        break
    print(f"Streamed: {entry}")
```

## Line-by-Line Explanation
Let's dissect the lazy generator function line-by-line:
1. `def lazy_log_reader(num_entries: int):`: Defines a function taking an integer parameter. Because the body contains `yield`, Python compiles this as a generator factory.
2. `for i in range(num_entries):`: Starts a standard loop. Notice that `range()` itself is also a lazy sequence in Python 3!
3. `yield f"LOG_ENTRY_{i:06d}: status=200 latency={i % 50}ms"`: This is the core magic:
   - Evaluates the formatted string.
   - Pauses the function frame immediately.
   - Transmits the string to whatever called `next()`.
   - Freezes `i`, `num_entries`, and the current loop counter inside the generator object's frame.
4. `lazy_data = lazy_log_reader(100_000)`: Creates the generator object. Zero log strings have been created yet! `sys.getsizeof(lazy_data)` reports under 200 bytes, regardless of whether `num_entries` is 10 or 100,000,000.
5. `for index, entry in enumerate(lazy_data):`: The `for` loop calls `iter(lazy_data)` and repeatedly invokes `next(lazy_data)`. Each iteration wakes up the generator, retrieves one string, and immediately prints it.
6. `if index >= 3: break`: When we break after 3 items, the remaining 99,997 log strings are never generated, saving CPU cycles and RAM.

## What Python Is Doing
Under the hood in CPython, every generator object contains:
- `gi_frame`: A pointer to the execution frame (`PyFrameObject`). Unlike regular functions where frames are created on the C call stack and popped upon return, generator frames are allocated on the heap! This allows them to outlive individual function invocations.
- `f_lasti`: The "last instruction" byte offset. When suspended at a `yield`, CPython records the exact bytecode instruction. When `next()` is called, CPython uses `JUMP_ABSOLUTE` or re-enters the evaluation loop (`_PyEval_EvalFrameDefault`) right after `f_lasti`.
- `f_locals`: A dictionary-like array containing all local variable bindings (`i`, `num_entries`). These remain intact in memory while suspended.
- `gi_running`: A boolean flag preventing re-entrant calls into the same generator while it is actively executing.

When the function finishes, CPython sets the frame's instruction pointer to the end, clears the local references, and raises `StopIteration`.

## Common Mistakes
### 1. Expecting a Value from Calling the Function
```python
def make_numbers():
    yield 1
    yield 2

res = make_numbers()
print(res)  # <generator object make_numbers at 0x7f...> (NOT 1 or [1, 2]!)
```
**Fix**: Consume it using `list(res)`, a `for` loop, or `next(res)`.

### 2. Exhausting a Generator and Reusing It
A generator is a single-use stream. Once it reaches the end, it is exhausted:
```python
gen = (x * 2 for x in [1, 2, 3])
print(list(gen))  # [2, 4, 6]
print(list(gen))  # [] — It's completely empty now!
```
**Fix**: If you need multiple passes, re-create the generator by calling the generator function again, or convert it to a `list` if the data fits in memory.

### 3. Confusing `return` with `yield`
Inside a generator, `return value` does **not** yield `value` to a standard `for` loop. Instead, in Python 3.3+, `return value` sets the value attribute of the raised `StopIteration(value)` exception, which is used in coroutines, but ignored by `for` loops!

### 4. Indexing a Generator
Generators do not support indexing (`gen[0]`) or `len(gen)`. Because items are generated dynamically on demand, Python does not know how many items exist or where item `k` is without advancing the stream.

## Real-World Uses
- **Processing Large CSV and JSON Files**: Reading gigabyte-scale datasets line by line without blowing up server memory.
- **Database Query Cursors**: Fetching query results in chunks or single records using server-side cursors (`fetchmany` or streaming ORM queries).
- **Infinite Sequences**: Generating mathematical series (Fibonacci numbers, prime number sieves, UUID sequences) that cannot fit into finite memory.
- **Audio and Video Streaming**: Reading raw multimedia frames in chunks of 4 KB or 64 KB and piping them directly to network sockets or transcoding engines.

## Connection to AI Agents
In AI agent architectures, generators are indispensable:
- **Streaming LLM Tokens**: Modern LLM APIs (OpenAI, Anthropic, Ollama, vLLM) send server-sent events (SSE) token by token. Agent runtimes wrap these HTTP streams in Python generators, yielding each token to the user UI the millisecond it arrives instead of waiting 15 seconds for the full response.
- **Agent Action Observation Pipelines**: Agents consume long environment event streams (e.g. file watchers, Discord/Slack webhooks, git commit feeds). Generators filter and preprocess raw events into clean agent observations on the fly.
- **Context Window Sliding**: When an agent summarizes massive interaction histories, generators yield chunked sliding windows of text for embedding computation without buffering the entire document corpus into memory.

## Practice
Open a Python interactive shell and try the following exercises:
1. Write a generator function `even_numbers(limit)` that yields all even numbers from `0` up to `limit`.
2. Step through it manually using `next()` and observe the `StopIteration` error when you pass `limit`.
3. Create a generator expression that reads strings from a list and yields them in uppercase.
4. Chain two generators: one that yields integers `1` to `10`, and a second generator that takes the first and yields only the values greater than `5`.

## Challenge
Write a streaming pipeline that monitors a simulated access log. Stage 1 generates infinite raw log lines formatted as `TIMESTAMP IP STATUS PATH`. Stage 2 parses the lines into dictionaries. Stage 3 filters out all statuses except `500` (server errors). Stage 4 consumes the stream and alerts when more than 3 errors occur within 10 requests. Verify that your pipeline processes millions of simulated lines while keeping resident memory under 50 MB.

## Summary
- Generators enable **lazy evaluation**: computing values only when requested.
- Functions containing `yield` become generator factories that return stateful generator objects.
- Generator objects freeze their local frame when yielding and resume seamlessly when `next()` is called.
- Generator expressions `(x for x in data)` provide concise, memory-friendly one-liners.
- Generators are single-use streams: once exhausted, they cannot be rewound.
- In AI engineering, generators provide the backbone for streaming token output, sliding-window chunking, and memory-safe data processing.

## What You Should Know Before Moving On
Before advancing to Module 18 (Iterators), ensure you can:
- Explain the difference in execution flow between `return` and `yield`.
- Predict how local variables behave across multiple calls to `next()`.
- Identify when to use a generator expression versus a list comprehension.
- Handle or understand the role of `StopIteration` in terminating iteration loops.
- Explain why streaming tokens via generators creates a responsive user experience in AI chat applications.
