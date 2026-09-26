"""
Module 18: Iterators and the Iterator Protocol
==============================================

This lesson explores the foundational mechanics of Python's iteration model.
We examine the contract between iterables and iterators, dissect how the `for`
loop executes at the runtime level, build custom stateful iterator classes,
demonstrate sentinel-based stream processing, and leverage `itertools` for
streaming pipelines in AI agent applications.

Sections:
  1. The Core Iterator Protocol: iter(), next(), and StopIteration
  2. Deconstructing the `for` Loop: Manual Emulation
  3. Iterable vs. Iterator: The Fundamental Architectural Distinction
  4. Building Custom Iterator Classes (Single-use vs Reusable)
  5. The Two-Argument iter(callable, sentinel) Pattern
  6. High-Performance Iteration with the `itertools` Standard Library
  7. AI Agent Case Study: Trajectory Replay Buffer and Token Windowing
"""

import itertools
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple


# =====================================================================
# 1. The Core Iterator Protocol: iter(), next(), and StopIteration
# =====================================================================
print("=" * 70)
print("1. THE CORE ITERATOR PROTOCOL: iter(), next(), and StopIteration")
print("=" * 70)

# An iterable is any object that can return an iterator via iter(obj).
fruits = ["apple", "banana", "cherry"]

# Calling iter() on an iterable returns an iterator object:
fruit_iterator = iter(fruits)
print(f"Original container (iterable): {fruits} (Type: {type(fruits).__name__})")
print(f"Obtained iterator object:      {fruit_iterator} (Type: {type(fruit_iterator).__name__})")

# We advance the iterator by invoking next():
first_fruit = next(fruit_iterator)
second_fruit = next(fruit_iterator)
third_fruit = next(fruit_iterator)
print(f"\nRetrieved sequentially:")
print(f"  Step 1: {first_fruit}")
print(f"  Step 2: {second_fruit}")
print(f"  Step 3: {third_fruit}")

# Once exhausted, further calls to next() raise StopIteration:
print("\nAttempting to call next() on an exhausted iterator:")
try:
    next(fruit_iterator)
except StopIteration:
    print("  -> Caught StopIteration! The iterator has reached the end of its stream.")

# Using next() with a default fallback to avoid raising an exception:
safe_fallback = next(fruit_iterator, "NO_MORE_ELEMENTS")
print(f"  -> Safe retrieval with default: '{safe_fallback}'")


# =====================================================================
# 2. Deconstructing the `for` Loop: Manual Emulation
# =====================================================================
print("\n" + "=" * 70)
print("2. DECONSTRUCTING THE `for` LOOP: MANUAL EMULATION")
print("=" * 70)

raw_data = [100, 200, 300]
print(f"Target list: {raw_data}")

print("\n--- Standard Python `for` Loop Output ---")
for num in raw_data:
    print(f"  Processing item: {num}")

print("\n--- Manual Emulation of the `for` Loop Runtime ---")
# Step A: Obtain the iterator
manual_it = iter(raw_data)

# Step B: Enter an infinite loop calling next() and catching StopIteration
while True:
    try:
        current_item = next(manual_it)
    except StopIteration:
        # Step C: The stream is exhausted, cleanly exit loop without traceback
        break
    else:
        # Step D: Execute loop body
        print(f"  [Manual Loop] Processing item: {current_item}")

print("  -> Manual loop finished cleanly, exactly matching Python's native behavior.")


# =====================================================================
# 3. Iterable vs. Iterator: The Fundamental Architectural Distinction
# =====================================================================
print("\n" + "=" * 70)
print("3. ITERABLE VS. ITERATOR: ARCHITECTURAL DISTINCTION")
print("=" * 70)

# Key Rule:
#   - An Iterable has __iter__(), but does NOT necessarily have __next__().
#   - An Iterator has BOTH __iter__() and __next__().
#   - An Iterator's __iter__() method MUST return self!

sample_list = [1, 2, 3]
sample_iter = iter(sample_list)

print(f"Does list have '__iter__'? {'__iter__' in dir(sample_list)}")
print(f"Does list have '__next__'? {'__next__' in dir(sample_list)}")

print(f"Does iterator have '__iter__'? {'__iter__' in dir(sample_iter)}")
print(f"Does iterator have '__next__'? {'__next__' in dir(sample_iter)}")

# Verify the iterator protocol contract: iter(iterator) is iterator
print(f"Is iter(sample_iter) identical to sample_iter? {iter(sample_iter) is sample_iter}")


# =====================================================================
# 4. Building Custom Iterator Classes (Single-Use vs Reusable)
# =====================================================================
print("\n" + "=" * 70)
print("4. BUILDING CUSTOM ITERATOR CLASSES")
print("=" * 70)

class CountdownIterator:
    """
    A stateful countdown iterator.
    Implements both __iter__ and __next__ directly.
    Notice: This is single-use. Once it reaches 0, it stays exhausted.
    """
    def __init__(self, start: int):
        self.count = start

    def __iter__(self) -> "CountdownIterator":
        return self

    def __next__(self) -> int:
        if self.count <= 0:
            raise StopIteration
        current = self.count
        self.count -= 1
        return current

print("Testing CountdownIterator(3):")
timer = CountdownIterator(3)
for tick in timer:
    print(f"  T-minus {tick}...")
print("  Liftoff!")

# Demonstrating Reusable Iterable Pattern:
# To make a collection reusable, separate the collection class (iterable)
# from the cursor class (iterator).

class AgentKnowledgeBase:
    """
    Reusable container representing facts stored in an AI agent's memory.
    """
    def __init__(self, facts: List[str]):
        self._facts = list(facts)

    def add_fact(self, fact: str) -> None:
        self._facts.append(fact)

    def __iter__(self) -> "KnowledgeBaseIterator":
        # Returns a brand-new iterator on each call to iter()
        return KnowledgeBaseIterator(self._facts)

class KnowledgeBaseIterator:
    """
    Stateful cursor that steps through a snapshot of facts.
    """
    def __init__(self, facts: List[str]):
        self._facts = facts
        self._index = 0

    def __iter__(self) -> "KnowledgeBaseIterator":
        return self

    def __next__(self) -> str:
        if self._index >= len(self._facts):
            raise StopIteration
        fact = self._facts[self._index]
        self._index += 1
        return fact

print("\nTesting Reusable AgentKnowledgeBase:")
kb = AgentKnowledgeBase(["Sky is blue", "Python is expressive", "Agents plan actions"])

print("  First iteration pass:")
for item in kb:
    print(f"    Pass 1: {item}")

print("  Second iteration pass (fresh cursor created):")
for item in kb:
    print(f"    Pass 2: {item}")


# =====================================================================
# 5. The Two-Argument iter(callable, sentinel) Pattern
# =====================================================================
print("\n" + "=" * 70)
print("5. THE TWO-ARGUMENT iter(callable, sentinel) PATTERN")
print("=" * 70)

# In networking, subprocess reading, and agent message queues, we often poll
# a function until it returns a specific sentinel value (e.g. None or b"").

class SimulatedSensorQueue:
    def __init__(self, readings: List[Optional[int]]):
        self._readings = list(readings)
        self._pos = 0

    def poll(self) -> Optional[int]:
        if self._pos < len(self._readings):
            val = self._readings[self._pos]
            self._pos += 1
            return val
        return None

sensor = SimulatedSensorQueue([21, 22, 23, 22, None, 25])

# iter(sensor.poll, None) repeatedly calls sensor.poll() until it returns None
sentinel_iterator = iter(sensor.poll, None)
print("Consuming sensor data with sentinel=None:")
for reading in sentinel_iterator:
    print(f"  Valid sensor reading: {reading}°C")
print("  Sentinel encountered: Stream ended gracefully.")


# =====================================================================
# 6. High-Performance Iteration with the `itertools` Standard Library
# =====================================================================
print("\n" + "=" * 70)
print("6. HIGH-PERFORMANCE ITERATION WITH `itertools`")
print("=" * 70)

# itertools.islice: Slice an iterator without loading the entire stream
counter = itertools.count(start=10, step=5)  # Infinite: 10, 15, 20, 25, ...
first_four = list(itertools.islice(counter, 4))
print(f"itertools.islice on infinite count(): {first_four}")

# itertools.chain: Concatenate multiple iterables into a single seamless stream
batch_a = ["agent_setup", "init_model"]
batch_b = ["load_weights", "start_inference"]
merged = list(itertools.chain(batch_a, batch_b))
print(f"itertools.chain merged stream: {merged}")

# itertools.takewhile: Consume while condition holds
scores = [98, 95, 91, 84, 72, 60]
high_scores = list(itertools.takewhile(lambda s: s >= 90, scores))
print(f"itertools.takewhile (score >= 90): {high_scores}")


# =====================================================================
# 7. AI Agent Case Study: Trajectory Replay Buffer and Token Windowing
# =====================================================================
print("\n" + "=" * 70)
print("7. AI AGENT CASE STUDY: TRAJECTORY REPLAY BUFFER & TOKEN WINDOWING")
print("=" * 70)

class TrajectoryReplayBuffer:
    """
    Fixed-capacity circular replay buffer for RL agents.
    Provides chronological iteration regardless of current ring head.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer: List[Optional[Dict[str, Any]]] = [None] * capacity
        self.head = 0
        self.size = 0

    def append(self, step_data: Dict[str, Any]) -> None:
        self.buffer[self.head] = step_data
        self.head = (self.head + 1) % self.capacity
        if self.size < self.capacity:
            self.size += 1

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        # Calculate starting index of oldest record
        start = (self.head - self.size) % self.capacity
        for offset in range(self.size):
            idx = (start + offset) % self.capacity
            record = self.buffer[idx]
            if record is not None:
                yield record

replay = TrajectoryReplayBuffer(capacity=3)
replay.append({"step": 1, "action": "scan_directory", "reward": 0.1})
replay.append({"step": 2, "action": "read_manifest", "reward": 0.5})
replay.append({"step": 3, "action": "find_target_file", "reward": 1.0})
# This 4th write will overwrite step 1 in the circular buffer:
replay.append({"step": 4, "action": "execute_patch", "reward": 2.0})

print("Chronological traversal of circular agent buffer (capacity 3):")
for step_record in replay:
    print(f"  Step {step_record['step']}: {step_record['action']} (Reward: {step_record['reward']})")

print("\n" + "=" * 70)
print("Module 18 lesson completed successfully!")
print("=" * 70)
