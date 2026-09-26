# Topic: Iterables, Iterators, and the Iterator Protocol

## What You Will Learn
In this module, you will uncover the foundational mechanics that power Python's looping constructs: the Iterator Protocol. You will learn:
- The critical conceptual distinction between an **iterable** (a container or source that can produce an iterator) and an **iterator** (a stateful stream engine that produces items one at a time).
- How Python's `for` loop really works under the hood using `iter()` and `next()`.
- The two magic dunder methods that form the Iterator Protocol: `__iter__()` and `__next__()`.
- How to build custom stateful iterator classes from scratch with boundary management and exception signaling.
- How the two-argument form of `iter(callable, sentinel)` enables clean reading of streams, sockets, and chunks.
- How to leverage Python's powerful built-in `itertools` library (`islice`, `chain`, `cycle`, `count`, `takewhile`) to compose memory-efficient data pipelines.
- How autonomous AI agents use iterators to step through token sequences, iterate over tool schemas, paginate through vector database query results, and replay episode trajectories.

## Prerequisites
Before diving into iterators, you should be familiar with:
- Variables, data types, and collections such as lists, tuples, and dictionaries (Modules 03–06).
- Control flow constructs, particularly `for` loops, `while` loops, and break/continue statements (Module 07).
- Functions, arguments, and return values (Module 08).
- Basic object-oriented programming concepts such as classes, `self`, and dunder methods like `__init__` (Module 13).
- Generators and the concept of lazy evaluation (Module 17).

## The Problem
Every Python developer uses `for item in items:` on their very first day. But how does Python actually traverse an object?
Consider building an AI agent that retrieves millions of document chunks or embedded vectors from a remote index. If the retrieval client returns a list:
```python
# Problematic eager approach:
chunks = vector_db.get_all_embeddings()  # Allocates 10 GB in memory
for chunk in chunks:
    process(chunk)
```
If the dataset is large, loading the entire collection into memory upfront risks an out-of-memory crash. Furthermore, what if the stream of incoming events is infinite, such as real-time user inputs from a web interface, telemetry signals from a robot, or live WebSocket messages from a financial exchange? You cannot put an infinite sequence into a list.

Even more fundamentally, what happens if you want a custom data structure (such as a Tree, a Graph of agent execution steps, a Circular Buffer of conversation context, or an encrypted stream) to participate naturally in Python's native `for` loops, `sum()`, `min()`, `max()`, and list comprehensions?

Without understanding the Iterator Protocol, you are trapped writing awkward manual index bookkeeping (`while i < len(...)`) that is prone to off-by-one errors and breaks encapsulation. The Iterator Protocol provides a universal, elegant contract that decouples data traversal from data storage.

## Key Terminology
- **Iterable**: Any Python object capable of returning an iterator. An iterable implements `__iter__()` returning an iterator, or implements `__getitem__()` with consecutive integer indices starting from 0. Examples: `list`, `str`, `dict`, `set`, `tuple`, open files, and generator objects.
- **Iterator**: A stateful object representing a stream of data that produces successive values via the `__next__()` method. It must also implement `__iter__()` returning `self`.
- **Iterator Protocol**: The formal Python convention requiring an iterator to provide two methods: `__iter__()` (which returns the iterator itself) and `__next__()` (which returns the next item or raises `StopIteration`).
- **`StopIteration`**: The standard exception raised by `__next__()` when no further items are available in the stream, signaling clean completion to iteration constructs.
- **`iter(obj)`**: Built-in function that calls `obj.__iter__()`, or converts a sequence supporting `__getitem__` into an iterator.
- **`next(iterator[, default])`**: Built-in function that calls `iterator.__next__()`. If a default argument is provided, returns the default instead of raising `StopIteration` when exhausted.
- **Sentinel Iterator**: An iterator created with `iter(callable, sentinel)` that repeatedly invokes `callable()` until it returns the `sentinel` value.
- **`itertools`**: A standard library module offering fast, memory-efficient building blocks for creating combinatoric and streaming iterators.

## Intuition
Imagine a printed novel.
- The **novel** itself is an **iterable**. It contains the entire text, sitting statically on the shelf. You can open it as many times as you like.
- A **bookmark** with a magnifying glass is an **iterator**. It remembers exactly what line you are currently reading. When you say "read next sentence", it moves forward one line and reads it aloud.
- If two people are reading the same novel, each person has their own bookmark (separate iterators) pointing to different pages in the same book (the iterable).
- When the bookmark hits the back cover of the book, it raises its hand and says: "Finished!" (raising `StopIteration`). If you ask it again, it still says finished.
- To read the novel again from the beginning, you don't rewind the old bookmark; you put a brand new bookmark at page 1 (calling `iter(book)` to create a new iterator).

## Concept
Python achieves total polymorphism in looping through duck typing. A `for` loop does not care whether an object is a list, a string, a database cursor, an open network socket, or a custom class. The `for` loop executes a strict sequence of actions:
1. It calls `iter(container)` on the target object.
2. The object returns an iterator implementing `__next__()`.
3. The loop repeatedly calls `next(iterator)`.
4. The value returned by `next()` is bound to the loop variable and the loop body executes.
5. When `next()` raises `StopIteration`, the loop catches the exception and exits cleanly without displaying any traceback.

Here is the fundamental rule of the Iterator Protocol:
- **Every iterator is an iterable** (because calling `iter(it)` returns `it` itself).
- **Not every iterable is an iterator** (e.g., a `list` has `__iter__()` but does not have `__next__()`).

Because an iterator tracks its own traversal state, an iterator is generally single-pass and mutable: advancing it consumes the stream.

## Syntax
### 1. Manual Traversal with `iter()` and `next()`
```python
numbers = [10, 20, 30]
it = iter(numbers)        # Obtains list_iterator

val1 = next(it)          # 10
val2 = next(it)          # 20
val3 = next(it)          # 30
# next(it)               # Raises StopIteration

# Using safe default fallback:
val4 = next(it, "DONE")  # Returns "DONE" without raising StopIteration
```

### 2. Building a Custom Iterator Class
To create an iterator class, implement `__iter__` and `__next__`:
```python
class Countdown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        # An iterator's __iter__ must return self
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val
```

### 3. Creating Separate Iterable and Iterator
For reusable collections that can be looped over multiple times:
```python
class StepRange:
    def __init__(self, start: int, stop: int, step: int = 1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return StepRangeIterator(self.start, self.stop, self.step)

class StepRangeIterator:
    def __init__(self, current: int, stop: int, step: int):
        self.current = current
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += self.step
        return val
```

### 4. Sentinel-based `iter(callable, sentinel)`
```python
# Reads 64-byte chunks from a binary stream until b"" (empty bytes) is returned
chunks = iter(lambda: stream.read(64), b"")
for chunk in chunks:
    process_chunk(chunk)
```

## Example
The following runnable script demonstrates custom iterators, the exact deconstruction of a `for` loop, and stream processing with `itertools`:

```python
import itertools

# 1. Custom Agent Replay Buffer Iterator
class EpisodeReplay:
    """An iterable container holding agent state-action steps."""
    def __init__(self, steps):
        self.steps = list(steps)

    def __iter__(self):
        return EpisodeReplayIterator(self.steps)

class EpisodeReplayIterator:
    """An iterator maintaining a cursor over the episode steps."""
    def __init__(self, steps):
        self._steps = steps
        self._cursor = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cursor >= len(self._steps):
            raise StopIteration
        item = self._steps[self._cursor]
        self._cursor += 1
        return item

# 2. Iterating with for loop
episode = EpisodeReplay(["obs_0", "act_take_key", "obs_1", "act_unlock_door", "reward_10"])
for step in episode:
    print(f"Step: {step}")

# 3. Demonstrating that multiple iterators can independently traverse the same iterable
it1 = iter(episode)
it2 = iter(episode)
print("it1 step 1:", next(it1))  # obs_0
print("it1 step 2:", next(it1))  # act_take_key
print("it2 step 1:", next(it2))  # obs_0 (independent cursor!)

# 4. Composing with itertools
chained = list(itertools.chain(["intro"], iter(episode), ["summary"]))
print("Chained sequence:", chained)
```

## Line-by-Line Explanation
Let's analyze the `EpisodeReplay` and `EpisodeReplayIterator` implementation:
1. `class EpisodeReplay:` defines the high-level data collection (the iterable). It stores the steps in an internal list `self.steps`.
2. `def __iter__(self): return EpisodeReplayIterator(self.steps)`: Every time Python asks for an iterator via `iter(episode)`, this method executes and constructs a *fresh* `EpisodeReplayIterator` instance. This allows the collection to be iterated multiple times, or by multiple loops concurrently, without cursor collision.
3. `class EpisodeReplayIterator:` defines the iterator engine.
4. `self._cursor = 0`: Initializes the internal state tracking which element is next.
5. `def __iter__(self): return self`: Mandatory by the iterator protocol. Allows an iterator itself to be passed anywhere an iterable is expected (e.g. into `zip()`, `enumerate()`, or nested loops).
6. `def __next__(self):`: Evaluated on each iteration step.
7. `if self._cursor >= len(self._steps): raise StopIteration`: Checks the termination boundary. Raising `StopIteration` notifies Python that the stream has terminated.
8. `item = self._steps[self._cursor]; self._cursor += 1; return item`: Retrieves the current item, advances the cursor state forward, and yields the item to the caller.

## What Python Is Doing
When you write:
```python
for item in container:
    do_something(item)
```
CPython compiles this code into specific bytecode instructions:
```text
GET_ITER
FOR_ITER     target_label
STORE_FAST   item
... body ...
JUMP_BACKWARD
target_label:
```
Here is the step-by-step CPython virtual machine execution:
1. `GET_ITER`: CPython inspects the object at the top of the evaluation stack. It looks for `type(container)->tp_iter`. If present, it calls the C function corresponding to `__iter__()`. If not present, but `type(container)->tp_as_sequence` has `sq_item` (the `__getitem__` method), CPython creates a built-in `sequence_iterator` starting at index 0.
2. `FOR_ITER`: Calls `type(iterator)->tp_iternext` (corresponding to `__next__()`). If `tp_iternext` returns a non-NULL `PyObject*`, that object is pushed onto the stack and bound to `item`.
3. If `tp_iternext` returns NULL, CPython checks if `PyErr_Occurred()` is `PyExc_StopIteration`. If so, CPython clears the exception silently and jumps past the loop block to `target_label`. If a different exception occurred, execution halts and the exception propagates upward.
4. If an iterator does not define `__iter__` returning itself, calling `iter(it)` would fail, breaking composability with built-in functions like `zip`, `map`, and `filter`.

## Common Mistakes
### 1. Forgetting to Return `self` from `__iter__` in an Iterator
```python
class BadIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    # BUG: Missing __iter__(self): return self
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        res = self.data[self.index]
        self.index += 1
        return res

b = BadIterator([1, 2, 3])
# iter(b) -> TypeError: 'BadIterator' object is not iterable
```
**Fix**: Always implement `def __iter__(self): return self` on iterator classes.

### 2. Making the Container Its Own Iterator When It Should Be Reusable
If a class modifies its own internal cursor in `__next__` and returns `self` from `__iter__`, looping over it a second time does nothing:
```python
class SingleUseList:
    def __init__(self, items):
        self.items = items
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.i >= len(self.items):
            raise StopIteration
        val = self.items[self.i]
        self.i += 1
        return val

box = SingleUseList([1, 2, 3])
for x in box: pass
for x in box: print(x) # PRINTS NOTHING! Cursor was never reset!
```
**Fix**: Separate the collection class (iterable) from the cursor class (iterator), or reset the index in `__iter__` if the container owns the data.

### 3. Forgetting to Advance State in `__next__`
If you forget to increment the index or advance state before returning from `__next__`, the iterator creates an infinite loop yielding the same value over and over.

### 4. Expecting `len()` on Arbitrary Iterators
Iterators do not know their total length in advance without consuming elements. Calling `len(it)` raises `TypeError: object of type '...' has no len()`.

## Real-World Uses
- **Database Cursors (`psycopg2`, `sqlite3`, SQLAlchemy)**: Streaming large query results row by row from the network buffer rather than caching millions of rows in memory.
- **File and Socket Stream Readers**: Iterating line by line over multi-gigabyte log files using `for line in open(filepath):`.
- **Data Loaders in Machine Learning (PyTorch `DataLoader`, TensorFlow `Dataset`)**: Batching, shuffling, and serving tensors to GPU memory asynchronously during training epochs.
- **Stream Tokenizers & Lexers**: Compilers, parsers, and regex engines iterate over character streams one token at a time without loading entire syntax trees upfront.

## Connection to AI Agents
In AI agent systems, iterators are foundational:
- **Conversation History Sliding Windows**: Agent memory buffers use iterators to step backward through conversation turns, accumulating token counts until the context limit of the LLM is reached.
- **Streaming Tool Call Execution**: When an LLM generates structured tool invocations, an iterator streams and yields verified tool call arguments as they are validated by JSON schema parsers.
- **Vector Database Paginators**: When an agent searches for knowledge relevant to a user query, vector databases return paginated iterators that stream top-k nearest neighbors on demand.
- **Environment Step Trajectories**: Reinforcement learning and autonomous agent runtimes model agent interactions as state-action-observation iterators, enabling step-by-step simulation and replay during debugging.

## Practice
Test your understanding by trying these hands-on steps in Python:
1. Create a list `items = ["alpha", "beta", "gamma"]`. Create an iterator using `it = iter(items)`. Call `next(it)` until `StopIteration` is raised.
2. Call `next(it, "DEFAULT")` on the exhausted iterator and observe how the fallback value works.
3. Write a small iterator class `FibonacciIterator(n)` that generates the first `n` Fibonacci numbers.
4. Use `itertools.islice` on an infinite counter `itertools.count(start=10, step=2)` to take the first 5 numbers.
5. Use `iter(input_func, sentinel)` to build a simulated loop that stops when a specific termination code is encountered.

## Challenge
Build an `AgentMemoryRingBuffer` class: a fixed-capacity circular memory buffer that stores the most recent `N` agent observations. Implement the Iterator Protocol so that when someone iterates over the ring buffer with `for item in buffer:`, it yields elements strictly in chronological order (oldest to newest), correctly handling wraparound when more than `N` items have been inserted. Make sure the buffer can be iterated multiple times without destroying its stored history.

## Summary
- An **iterable** is an object with an `__iter__()` method that returns an iterator.
- An **iterator** is a stateful object with a `__next__()` method that produces items and raises `StopIteration` when finished.
- Every iterator must implement `__iter__()` returning `self`.
- Python's `for` loop is syntactic sugar for obtaining an iterator via `iter()` and calling `next()` until `StopIteration` is caught.
- Reusable collections should return a new iterator instance from `__iter__()` to avoid cursor exhaustion.
- The `itertools` module provides efficient, composable primitives for building complex streaming iterators.

## What You Should Know Before Moving On
Before advancing to Module 19 (Decorators), verify that you can:
- Clearly explain why a list is an iterable but not an iterator.
- Re-implement a standard `for` loop manually using a `while True:` loop, `iter()`, `next()`, and a `try/except StopIteration` block.
- Build a custom class from scratch implementing both `__iter__` and `__next__`.
- Describe why an iterator must return `self` from its `__iter__` method.
- Explain how AI agents use streaming iterators to process long context histories and tool execution steps with minimal memory consumption.
