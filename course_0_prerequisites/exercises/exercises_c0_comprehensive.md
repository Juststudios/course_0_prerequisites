# Course 0: Comprehensive 4-Tier Exercise Curriculum

---

## Module 01: Callables and Functional Python

### Tier 1 (Recall)
1. Which built-in function checks whether an object can be called with parentheses `()`?
2. What magic method must a class implement to allow its instances to be invoked like functions?
3. What information is preserved by decorating a wrapper with `@functools.wraps(func)`?

### Tier 2 (Debugging)
Identify and correct the bug in this tool decorator:
```python
def tool(func):
    def wrapper(*args, **kwargs):
        print(f"Calling tool {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```
*Issue*: Omitting `@functools.wraps` destroys `wrapper.__name__`, `wrapper.__doc__`, and `wrapper.__annotations__`, breaking LLM schema introspection.

### Tier 3 (Application)
Implement a `@timed_tool` decorator that records the execution duration in milliseconds as an attribute on the callable (`func.last_latency_ms`).

### Tier 4 (Challenge)
Construct an extensible `DynamicToolRegistry` class that inspects parameter type annotations, defaults, and docstrings using the `inspect` module to dynamically build an OpenAI-compliant JSON schema dictionary.

---

## Module 02: Classes, Dunder Methods, and OOP Patterns

### Tier 1 (Recall)
1. What is the difference between `__repr__` and `__str__`?
2. What are the method signatures of `__enter__` and `__exit__` in context managers?
3. Can an Abstract Base Class (`abc.ABC`) with un-implemented `@abstractmethod`s be instantiated?

### Tier 2 (Debugging)
Diagnose why this database context manager swallows all errors:
```python
class AgentDBSession:
    def __enter__(self):
        self.conn = connect()
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True
```
*Issue*: Returning `True` in `__exit__` suppresses all exceptions, masking catastrophic bugs. It should return `False` or omit return.

### Tier 3 (Application)
Create an `AgentMessage` class implementing `__str__` for clean prompt display, `__repr__` for debug logs, and `__getitem__` on a `ConversationHistory` class.

### Tier 4 (Challenge)
Define an abstract `BaseLLMProvider` interface and implement two polymorphic classes (`MockProvider` and `RuleProvider`). Inject both into an `Agent` class via composition.

---

## Module 03: Type Hints and Pydantic Runtime Validation

### Tier 1 (Recall)
1. Which Pydantic method generates a standard JSON Schema dictionary?
2. How do you declare an integer field that must be between 1 and 10 in Pydantic?
3. What exception is raised when invalid types are supplied to a Pydantic model?

### Tier 2 (Debugging)
Fix the validation gap:
```python
class SearchArgs(BaseModel):
    query: str
    limit: int
```
*Issue*: `query` accepts empty strings `""` and `limit` accepts negative integers `-10`. Use `Field(..., min_length=1)` and `Field(default=5, ge=1, le=50)`.

### Tier 3 (Application)
Write a Pydantic model for `ToolCallEnvelope` containing a unique string `call_id`, a validated tool name, and a nested Pydantic argument model.

### Tier 4 (Challenge)
Build an automated `SelfCorrectingParser` that parses raw LLM JSON strings into a Pydantic model. If a `ValidationError` occurs, generate a formatted correction prompt enumerating each invalid field path and error message.

---

## Module 04: Async/Await and Event Loops

### Tier 1 (Recall)
1. How does cooperative multitasking in an asyncio event loop differ from preemptive multithreading?
2. What function gathers multiple awaitable coroutines and runs them concurrently?
3. How do you run a blocking synchronous function without freezing the event loop?

### Tier 2 (Debugging)
Why does this tool runner fail to achieve concurrent speedup?
```python
async def run_batch(tools):
    results = []
    for t in tools:
        res = await t.run()
        results.append(res)
    return results
```
*Issue*: Sequentially awaiting each tool inside a `for` loop executes them one by one. Use `await asyncio.gather(*(t.run() for t in tools))`.

### Tier 3 (Application)
Write an async function `execute_with_timeout(coro, timeout_seconds: float)` that cancels the coroutine and returns an error payload if it takes longer than `timeout_seconds`.

### Tier 4 (Challenge)
Implement a `ThrottledBatchExecutor` that uses `asyncio.Semaphore` to bound concurrency to at most $N$ simultaneous tool executions, recording maximum observed concurrency.

---

## Module 05: ContextVars and Scoped State

### Tier 1 (Recall)
1. Why does `threading.local` fail to isolate state between coroutines in Python?
2. What does `ContextVar.set()` return, and how is it used?
3. Are context variables inherited by child tasks spawned via `asyncio.create_task()`?

### Tier 2 (Debugging)
Find the memory leak / context bleed in this middleware:
```python
tenant_ctx = ContextVar("tenant", default="anon")
async def handle_request(tenant_id, task):
    tenant_ctx.set(tenant_id)
    return await task()
```
*Issue*: The token returned by `set()` is never reset in a `finally` block, causing context to leak into subsequent requests.

### Tier 3 (Application)
Implement a context manager `ScopedContext(var: ContextVar[T], value: T)` that guarantees token resetting upon exit.

### Tier 4 (Challenge)
Run 10 concurrent async tasks representing 10 distinct tenants. Have each task make 3 nested function calls that read `tenant_id` from a `ContextVar` without passing it as an argument, asserting zero cross-talk across tasks.

---

## Module 06: HTTP and REST APIs

### Tier 1 (Recall)
1. What HTTP status code denotes "Too Many Requests"?
2. What header is standard for Bearer token API authentication?
3. What is the benefit of HTTP connection pooling across multiple agent API requests?

### Tier 2 (Debugging)
Why is this retry loop dangerous?
```python
for attempt in range(5):
    res = requests.post(url, json=data)
    if res.status_code == 200:
        break
    time.sleep(1)
```
*Issue*: It retries non-retryable 4xx client errors (like 401 Unauthorized or 400 Bad Request) and uses fixed sleep without exponential backoff or jitter.

### Tier 3 (Application)
Write an async HTTP client function that sends a POST request with an `Authorization: Bearer` header, custom `User-Agent`, and explicit timeout settings.

### Tier 4 (Challenge)
Build a resilient HTTP gateway that catches simulated 429 and 503 status codes, retrying with exponential backoff and randomized jitter ($t = \text{random.uniform}(0, \text{base} \cdot 2^{\text{attempt}})$), failing fast on 401.

---

## Module 07: JSON Parsing, Schema Validation, and Heuristic Repair

### Tier 1 (Recall)
1. What exception does `json.loads` raise on invalid syntax?
2. What are the JSON equivalents of Python's `True`, `False`, and `None`?
3. Why do LLMs frequently output markdown code fences around JSON?

### Tier 2 (Debugging)
Why does `json.loads(response.split("```json")[1].split("```")[0])` fail?
*Issue*: It crashes with an `IndexError` if the LLM output does not contain ```` ```json ````.

### Tier 3 (Application)
Write a function `strip_markdown_fences(text: str) -> str` that extracts raw JSON from markdown blocks, falling back to finding the outermost `{` and `}` braces.

### Tier 4 (Challenge)
Build a `RobustJSONRepair` pipeline that:
- Strips fences and conversational preamble.
- Removes trailing commas before closing braces/brackets.
- Replaces Python literals (`True`, `False`, `None`) with JSON equivalents.
- Appends missing closing brackets/braces using stack-based balancing for truncated responses.

---

## Module 08: Configuration Management and Secret Masking

### Tier 1 (Recall)
1. What order of precedence should configuration resolution follow?
2. What method on a Pydantic `SecretStr` retrieves the underlying raw secret?
3. Why should `.env` files never be committed to version control?

### Tier 2 (Debugging)
Identify the flaw:
```python
class Settings:
    TIMEOUT = int(os.environ.get("TIMEOUT", "10.5"))
```
*Issue*: Calling `int("10.5")` raises a `ValueError`! Cast via `float()` first or handle types properly.

### Tier 3 (Application)
Write a pure-Python parser that reads a multi-line `.env` string, strips quotes, and ignores comments and empty lines.

### Tier 4 (Challenge)
Build a `ProductionSettings` class using `pydantic-settings` that reads environment variables with prefix `AGENT_`, loads `api_key` as a `SecretStr`, and validates that database paths end in `.db`.

---

## Module 09: Subprocesses and Sandboxing

### Tier 1 (Recall)
1. Why does `shell=True` expose systems to command injection?
2. What parameter enforces an execution time limit in `subprocess.run()`?
3. What method canonicalizes file paths to detect directory traversal (`../`)?

### Tier 2 (Debugging)
Fix the injection vulnerability:
```python
subprocess.run(f"python3 runner.py --user {username}", shell=True)
```
*Issue*: Command injection if `username` contains `; rm -rf /`. Pass an argument array with `shell=False`.

### Tier 3 (Application)
Write a function `safe_exec(cmd_list, timeout=3.0)` that captures stdout, stderr, and return codes, handling `TimeoutExpired` cleanly.

### Tier 4 (Challenge)
Build a `SandboxedRunner` that restricts file operations and command execution to an ephemeral directory, rejecting any path escaping the root with `PermissionError`.

---

## Module 10: SQLite and Agent Memory

### Tier 1 (Recall)
1. How do you open an in-memory SQLite database?
2. Which PRAGMA command enables WAL mode in SQLite?
3. How do parameterized queries (`?`) prevent SQL injection?

### Tier 2 (Debugging)
Why does this function fail to persist records on disk?
```python
def save(conn, msg):
    conn.execute("INSERT INTO log VALUES (?)", (msg,))
```
*Issue*: Missing `conn.commit()` or wrapping in `with conn:`.

### Tier 3 (Application)
Create an `AgentMemory` class with tables for `messages` and `tool_audit`, supporting transactional inserts.

### Tier 4 (Challenge)
Implement sliding-window history retrieval that queries the database for the most recent $N$ messages and returns them in chronological order.

---

## Module 11: Architecture Patterns

### Tier 1 (Recall)
1. What are the core states in a ReAct agent state machine?
2. What is a "state transition guard"?
3. How does Dependency Injection improve agent testability?

### Tier 2 (Debugging)
Why does an agent using `while True:` without a step counter present a production hazard?
*Issue*: Infinite reasoning loops occur when tools repeatedly return errors or the LLM hallucinates, exhausting budgets.

### Tier 3 (Application)
Implement a simple 3-state Finite State Machine (`IDLE` $\rightarrow$ `RUNNING` $\rightarrow$ `COMPLETED`) that raises `ValueError` on illegal transitions.

### Tier 4 (Challenge)
Construct an `AgentFSM` enforcing step guards ($N \le \text{max\_steps}$), recording transition timestamps, and transitioning to an `ERROR` state on runaway loops.

---

## Module 12: Prompt Templating

### Tier 1 (Recall)
1. Why is XML tag delimitation recommended for LLM prompts?
2. How does few-shot prompting improve tool output compliance?
3. How do you escape user input to prevent prompt injection?

### Tier 2 (Debugging)
Fix the regex:
```python
re.search(r"<action>(.*)</action>", text).group(1)
```
*Issue*: Fails on multi-line actions because `.` does not match newlines without `re.DOTALL`.

### Tier 3 (Application)
Write a `SafeTemplate` class that validates that all placeholders in a template string are provided before rendering.

### Tier 4 (Challenge)
Build a `StructuredReActProtocol` that compiles system prompts with tool manifests, few-shot examples, and parses `<thought>`, `<action>`, and `<final_answer>` tags.

---

## Module 13: Logging and Observability

### Tier 1 (Recall)
1. What are the key fields in a structured JSON log entry?
2. What is the difference between a `trace_id` and a `span_id`?
3. Why is token usage accounting necessary in multi-step agents?

### Tier 2 (Debugging)
Why should you not use `print()` for production agent observability?
*Issue*: Output lacks severity levels, timestamps, structured fields, and interleaves arbitrarily across concurrent async tasks.

### Tier 3 (Application)
Create a custom `logging.Formatter` that outputs single-line JSON strings with timestamps, levels, and messages.

### Tier 4 (Challenge)
Build an `AgentTraceRecorder` that manages parent-child spans using context managers, records latency, and calculates cumulative token costs.

---

## Module 14: Streaming and SSE

### Tier 1 (Recall)
1. How does an async generator differ from a regular generator?
2. What is the required format of an SSE event chunk?
3. Why can you not parse individual streaming argument chunks as complete JSON?

### Tier 2 (Debugging)
Fix this syntax error:
```python
async def read(stream):
    for token in stream:
        print(token)
```
*Issue*: Must use `async for token in stream:`.

### Tier 3 (Application)
Write an async generator that yields words with artificial delay to simulate token streaming.

### Tier 4 (Challenge)
Build an `SSEDeltaAccumulator` that parses incoming SSE frames and reassembles fragmented tool argument chunks into a valid JSON object upon stream completion.

---

## Module 15: Mathematics Bridges

### Tier 1 (Recall)
1. What is the mathematical definition and range of cosine similarity?
2. Why is `temperature=0.0` critical for deterministic tool calling?
3. What is the formula for expected utility in decision-making?

### Tier 2 (Debugging)
Find the mathematical error:
```python
def cosine_sim(u, v):
    return sum(a*b for a,b in zip(u,v)) / (sum(u) * sum(v))
```
*Issue*: Denominator must be the product of the Euclidean $L_2$ norms ($\sqrt{\sum u_i^2}$), not the sum of elements.

### Tier 3 (Application)
Write a function `softmax_with_temperature(logits: list[float], temperature: float) -> list[float]` with numerical stability subtraction.

### Tier 4 (Challenge)
Build an `InMemoryVectorStore` that unit-normalizes document embeddings, computes cosine similarity, and performs Top-K nearest neighbor retrieval for RAG.
