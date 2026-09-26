# Topic: Python Collections: Lists, Tuples, Sets, and Dictionaries

## What You Will Learn
- The core mechanics and trade-offs of Python's four primary built-in collection types: `list`, `tuple`, `set`, and `dict`.
- The critical distinction between mutability (lists, dicts, sets) and immutability (tuples).
- How hash tables power $O(1)$ average-time lookups in dictionaries and sets, and the concept of hashability.
- Safe dictionary access patterns (`.get()`, default fallbacks, `.setdefault()`, and dictionary views).
- Set theory operations (unions, intersections, differences) and their role in deduplication and graph filtering.
- Reference aliasing traps, shallow copying (`.copy()`), and deep copying (`copy.deepcopy()`).
- How AI agents use collections to organize conversation message histories, build tool registries, and track visited execution nodes.

## Prerequisites
- Completion of Module 03 ("Variables and Data Types"), Module 04 ("Operators"), and Module 05 ("Strings").
- Clear understanding of object references and memory identity (`id()` vs. value equality `==`).

## The Problem
Individual variables (`x = 10`, `user = "Ada"`) can only hold a single value at a time. Real-world applications, however, process groups of interrelated data: a batch of 10,000 sensor readings, an ongoing chat history of dozens of user and assistant messages, an inventory database indexed by SKU, or a set of unique IP addresses visiting a server.

Storing 100 items by creating 100 separate variables (`item1`, `item2`, ..., `item100`) is impossible to maintain, impossible to loop through dynamically, and impossible to scale. Furthermore, different problems demand different data structures:
- If you need an ordered sequence that changes frequently, you need a **List**.
- If you need fixed, immutable records that can safely serve as dictionary keys, you need a **Tuple**.
- If you need instant $O(1)$ membership checks and duplicate elimination, you need a **Set**.
- If you need structured key-value lookups (like JSON records or agent tool catalogs), you need a **Dictionary**.

Selecting the wrong collection type can destroy performance ($O(N)$ vs $O(1)$) or cause corrupt state mutations.

## Key Terminology
- **Collection (Container)**: A data structure that holds multiple items simultaneously.
- **List (`list`)**: An ordered, mutable sequence of arbitrary elements indexed by integers starting at 0.
- **Tuple (`tuple`)**: An ordered, immutable sequence of elements. Once created, its length and elements cannot be changed.
- **Set (`set`)**: An unordered collection of unique, hashable items supporting mathematical set operations (union, intersection, difference).
- **Dictionary (`dict`)**: An associative collection of key-value pairs where unique keys map to arbitrary values (preserves insertion order in Python 3.7+).
- **Mutability**: The ability of an object to change its internal state or contents in-place without creating a new object in memory.
- **Hashability**: The property that an object possesses a hash value that never changes during its lifetime (via `__hash__()`) and can be compared for equality (via `__eq__()`). Immutable types (`int`, `float`, `str`, `tuple`) are hashable; mutable containers (`list`, `dict`, `set`) are unhashable.
- **Aliasing**: When two or more variable names reference the exact same mutable container in memory, causing mutations through one name to affect the other.

## Intuition
Imagine organizing an AI research office:
1. **The Clipboard (List)**: A vertical notepad where you jot down research tasks in order. You can append new tasks to the bottom, cross tasks off, or reorder them. If you ask for "task #3", you count down from the top.
2. **The Stone Tablet (Tuple)**: A permanent stone inscription of GPS coordinates: `(37.7749, -122.4194)`. It cannot be erased, rewritten, or extended. Because it is unchangeable, anyone can safely cite it without fear of unexpected tampering.
3. **The Keycard Badge Reader (Set)**: A digital turnstile tracking authorized personnel IDs. It doesn't care what order people arrived in, only whether an ID is in the authorized group. If an ID is scanned twice, it doesn't create a duplicate person in the room. Checking if a badge is valid happens in the blink of an eye ($O(1)$).
4. **The Office Phone Directory (Dictionary)**: A rolodex where you look up a person's name (the unique **key**) to find their direct extension number and office location (the **value**). You don't have to scan through every name one by one; you flip directly to their entry.

## Concept

### 1. Lists (`list`)
- Syntax: `[elem1, elem2, ...]`
- Common methods: `.append(x)`, `.extend(iterable)`, `.insert(i, x)`, `.pop(i)`, `.remove(x)`, `.sort()`, `.reverse()`.
- Slicing works identically to strings (`lst[start:stop:step]`).

```python
tasks = ["analyze_data", "run_tests"]
tasks.append("deploy_agent")       # ['analyze_data', 'run_tests', 'deploy_agent']
first_task = tasks.pop(0)          # Removes and returns 'analyze_data'
```

### 2. Tuples (`tuple`)
- Syntax: `(elem1, elem2, ...)` (Single item requires comma: `(x,)`).
- Immutability guarantees safety for multi-threaded access and allows tuples to be dictionary keys or set elements.
- Unpacking: `x, y = (10, 20)`.

```python
agent_coordinate = (12.5, 45.0, 100.0)
lat, lon, alt = agent_coordinate   # Unpacking
# agent_coordinate[0] = 13.0       # CRASH: TypeError! Tuples are immutable.
```

### 3. Sets (`set`)
- Syntax: `{elem1, elem2}` or `set(iterable)` (Note: `{}` creates an empty dict; use `set()` for empty sets!).
- Automatic deduplication.
- Set operations:
  - Union (`|`): all elements in either set.
  - Intersection (`&`): elements present in both sets.
  - Difference (`-`): elements in first set but not second.
  - Symmetric Difference (`^`): elements in one set or the other, but not both.

```python
active_nodes = {"node_1", "node_2", "node_3"}
failed_nodes = {"node_2", "node_4"}

healthy_nodes = active_nodes - failed_nodes  # {'node_1', 'node_3'}
all_nodes = active_nodes | failed_nodes      # {'node_1', 'node_2', 'node_3', 'node_4'}
```

### 4. Dictionaries (`dict`)
- Syntax: `{"key": value, ...}`
- Keys must be immutable/hashable (`str`, `int`, `tuple`). Values can be anything.
- Access: `d[key]` (raises `KeyError` if missing); `d.get(key, default)` (returns default safely).
- Views: `d.keys()`, `d.values()`, `d.items()`.

```python
agent_registry = {
    "search": {"cost": 5, "enabled": True},
    "calculator": {"cost": 1, "enabled": True}
}
calc_info = agent_registry.get("calculator")
unknown_info = agent_registry.get("terminal", {"cost": 0, "enabled": False})
```

## Syntax
```python
# Lists
messages = ["System initialized"]
messages.append("User query received")

# Tuples
config_pair = ("temperature", 0.7)
key, val = config_pair

# Sets
visited_urls = set()
visited_urls.add("https://example.com")
has_visited = "https://example.com" in visited_urls  # O(1) time complexity!

# Dictionaries
state = {"turn": 1, "status": "RUNNING"}
state["turn"] += 1
state.update({"status": "SUCCESS", "result": 42})
```

## Example
Here is a comprehensive script demonstrating all four collections in an AI Agent Tool Registry and Message History system:

```python
# Autonomous Agent Memory & Tool Execution Engine

# 1. Tuples: Immutable Agent Identity & Coordinates
agent_meta = ("Agent-Omni", "v1.2", 2026)
name, version, year = agent_meta
print(f"Agent Initialized: {name} (Version: {version})")

# 2. Lists: Ordered Conversation History
# Messages are appended sequentially as conversation unfolds:
conversation_history = [
    {"role": "system", "content": "You are a research agent."},
    {"role": "user", "content": "Summarize recent findings in quantum computing."}
]
conversation_history.append({"role": "assistant", "content": "Querying arXiv database..."})
print(f"History contains {len(conversation_history)} messages.")

# 3. Sets: Visited URLs / Deduplication
# Fast O(1) membership check prevents scraping cycles:
discovered_urls = ["https://arxiv.org/abs/1", "https://arxiv.org/abs/2", "https://arxiv.org/abs/1"]
visited_urls = set()

for url in discovered_urls:
    if url not in visited_urls:
        print(f"Scraping new URL: {url}")
        visited_urls.add(url)
    else:
        print(f"Skipping duplicate URL: {url}")

print(f"Unique URLs visited: {visited_urls}")

# 4. Dictionary: Tool Registry
# Maps tool name to capability metadata and handler:
def mock_search(query): return f"Search results for: {query}"
def mock_calc(expr): return eval(expr)

tool_registry = {
    "web_search": {"handler": mock_search, "rate_limit": 10},
    "calculator": {"handler": mock_calc, "rate_limit": 50},
}

# Invoking a tool dynamically:
invoked_tool = "web_search"
if invoked_tool in tool_registry:
    tool_data = tool_registry[invoked_tool]
    handler = tool_data["handler"]
    result = handler("quantum supremacy benchmarks")
    print(f"Tool Execution Output: {result}")
```

## Line-by-Line Explanation
- `agent_meta = ("Agent-Omni", "v1.2", 2026)`: Creates an immutable tuple containing three disparate types (`str`, `str`, `int`).
- `name, version, year = agent_meta`: Unpacks the three tuple elements into separate local variables in a single statement.
- `conversation_history = [...]`: Creates a mutable list of message dictionaries.
- `conversation_history.append(...)`: Appends a new dictionary object to the end of the list in $O(1)$ amortized time.
- `discovered_urls = [...]`: Defines a list containing a duplicate URL.
- `visited_urls = set()`: Instantiates an empty set (NOT `{}` which creates an empty dictionary).
- `url not in visited_urls`: Performs a membership check using hash lookup in $O(1)$ average time.
- `visited_urls.add(url)`: Inserts the string into the set, ensuring no duplicates exist.
- `tool_registry = {...}`: Creates a dictionary mapping string keys to nested dictionary values containing function references.
- `tool_registry[invoked_tool]["handler"](...)`: Retrieves the handler callable from the registry dictionary and executes it.

## What Python Is Doing
1. **Dynamic Array Mechanics in `list`**:
   In CPython, a list is implemented as a variable-length array of `PyObject*` pointers. When a list outgrows its allocated buffer, CPython over-allocates extra capacity using an over-allocation formula ($\approx +12.5\%$). This makes `.append()` amortized $O(1)$, but inserting at index 0 requires shifting all pointers in memory ($O(N)$).
2. **Hash Tables in `dict` and `set`**:
   Dictionaries use a compact hash table (introduced in Python 3.6). A hash table consists of an index array and an entries array. Python computes `hash(key) % table_size` to find the bucket index. When a collision occurs, it uses open addressing with quadratic perturbation. This provides lightning-fast $O(1)$ lookup, insertion, and deletion.
3. **Reference Aliasing Trap**:
   ```python
   a = [1, 2, 3]
   b = a          # Both names point to the SAME list in memory!
   b.append(4)
   print(a)       # [1, 2, 3, 4] -> 'a' was modified!
   ```
   To make an independent copy, use `b = a.copy()` or `b = list(a)`. For nested objects, use `copy.deepcopy()`.

## Common Mistakes
1. **Using `{}` to Create an Empty Set**:
   ```python
   s = {}        # This creates a DICT, not a set!
   print(type(s)) # <class 'dict'>
   s = set()     # Correct way to instantiate an empty set
   ```
2. **Creating a Single-Element Tuple Without a Comma**:
   ```python
   t1 = ("hello")   # This is a string (parentheses are just grouping)!
   t2 = ("hello",)  # Correct: The comma defines the tuple
   ```
3. **Using a Mutable Object as a Dictionary Key**:
   ```python
   d = {}
   d[[1, 2]] = "data"  # CRASH: TypeError: unhashable type: 'list'
   # Use tuples for compound keys: d[(1, 2)] = "data"
   ```
4. **Modifying a Collection While Iterating Over It**:
   Deleting items from a list or dictionary while looping over it skips elements or causes a `RuntimeError: dictionary changed size during iteration`. Always iterate over a copy: `for k in list(d.keys()): ...`.

## Real-World Uses
- **JSON Serialization & Deserialization**: In modern web APIs, JSON objects map directly to Python dicts, and JSON arrays map directly to Python lists.
- **Deduplication in Search Engines & Crawlers**: Using sets to track seen web pages, documents, or processed IDs.
- **Relational Lookups & Caching**: Using dictionaries as in-memory caches (memoization) mapping argument tuples `(arg1, arg2)` to precomputed results.
- **Graph Traversal**: Tracking visited vertices with sets and queued paths with lists.

## Connection to AI Agents
Collections are the foundational anatomy of autonomous agents:
- **Conversation Context Window**: Agents track chat history as a list of message dicts (`[{"role": "user", ...}, {"role": "assistant", ...}]`). Managing context limits involves slicing the list (`messages[-10:]`).
- **Tool Registries**: Agents map available tool names to function pointers and schema definitions in a dictionary.
- **Agent Memory & Knowledge Graphs**: Graph-based agents store nodes and edges using dictionaries of adjacency sets.
- **Deduplication in Planning**: When an agent searches through possible action trees (e.g. Tree of Thoughts, MCTS), it records visited state hashes in a set to avoid infinite loops.

## Practice
1. Create a list of 5 agent tool names. Append a new tool, remove the second tool, and slice the middle 3 tools.
2. Create a tuple containing 3 values: your agent's name, role, and max tokens. Unpack them into 3 variables.
3. Take a list with duplicates `[1, 2, 2, 3, 4, 4, 5]` and convert it to a set to remove duplicates, then back to a list.
4. Create a dictionary storing an agent's configuration. Use `.get()` with a fallback value to look up a key that doesn't exist.
5. Create two sets: `backend_tools = {"db", "api", "auth"}` and `required_tools = {"db", "search"}`. Compute their intersection (`&`) and difference (`-`).

## Challenge
Design an in-memory `AgentTaskQueue`:
1. Maintain an internal list of tasks sorted by priority (higher priority integer runs first).
2. Maintain a set of `completed_task_ids` to ensure no task is executed twice.
3. Maintain a dictionary `task_registry` mapping `task_id` to its execution metadata.
4. Implement methods `enqueue(task_id, priority, data)`, `dequeue()`, and `mark_complete(task_id)`.

## Summary
- Lists are ordered, mutable sequences ideal for dynamic arrays and sequential histories.
- Tuples are ordered, immutable sequences ideal for fixed records, multi-variable unpacking, and dictionary keys.
- Sets are unordered collections of unique elements providing $O(1)$ membership checks and set algebra.
- Dictionaries are key-value mappings powered by hash tables for $O(1)$ lookups by key.
- Be careful with mutability: assignment creates aliases, not copies. Use `.copy()` or `copy.deepcopy()`.
- AI agents represent their message memory as lists, tool catalogs as dictionaries, and exploration histories as sets.

## What You Should Know Before Moving On
Before advancing to Module 07 ("Control Flow"), verify that you can:
- Choose the appropriate collection type (`list`, `tuple`, `set`, `dict`) based on ordering, mutability, and lookup requirements.
- Safely look up keys in dictionaries without crashing via `.get(key, default)`.
- Perform set operations (`|`, `&`, `-`) to filter and deduplicate data.
- Avoid the aliasing trap when copying mutable collections.
- Explain how an AI agent uses lists for message history and dictionaries for tool registries.
