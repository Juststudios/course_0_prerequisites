# Course 0: Comprehensive 4-Tier Solutions and Walkthroughs

---

## Module 01: Callables and Functional Python

### Tier 1 (Recall)
1. `callable(obj)` returns `True` if `obj` can be called.
2. The `__call__` magic method allows a class instance to be invoked like a function (`instance()`).
3. `@functools.wraps(func)` preserves `__name__`, `__doc__`, `__annotations__`, `__module__`, and `__qualname__`.

### Tier 2 (Debugging)
**Corrected Implementation**:
```python
import functools

def tool(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling tool {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### Tier 3 (Application)
```python
import functools
import time

def timed_tool(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        wrapper.last_latency_ms = (time.perf_counter() - t0) * 1000.0
        return res
    wrapper.last_latency_ms = 0.0
    return wrapper
```

### Tier 4 (Challenge)
Refer to `01_callables_and_functional_python/tool_decorator.py` for the complete `ToolRegistry` implementation with schema extraction.

---

## Module 02: Classes, Dunder Methods, and OOP Patterns

### Tier 1 (Recall)
1. `__repr__` is intended for developers (unambiguous, code-like representation); `__str__` is intended for end-users (human-readable text).
2. `def __enter__(self) -> Any:` and `def __exit__(self, exc_type, exc_val, exc_tb) -> bool:`.
3. No. Python raises `TypeError: Can't instantiate abstract class ... with abstract methods ...`.

### Tier 2 (Debugging)
**Fix**: Remove `return True` from `__exit__`. Returning `None` or `False` allows exceptions to bubble up appropriately rather than being silently ignored.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `02_classes_dunder_and_oop/dunder_patterns.py` and `abstract_providers.py`.

---

## Module 03: Type Hints and Pydantic Runtime Validation

### Tier 1 (Recall)
1. `MyModel.model_json_schema()`
2. `Field(ge=1, le=10)`
3. `pydantic.ValidationError`

### Tier 2 (Debugging)
```python
from pydantic import BaseModel, Field

class SearchArgs(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    limit: int = Field(default=5, ge=1, le=50, description="Max results")
```

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `03_type_hints_and_pydantic/runtime_validation.py` for the self-correcting loop and error prompt formatter.

---

## Module 04: Async/Await and Event Loops

### Tier 1 (Recall)
1. Cooperative multitasking switches tasks only at explicit suspension points (`await`); preemptive multithreading allows the OS kernel to interrupt execution at any arbitrary CPU instruction.
2. `asyncio.gather(*coros)`
3. `await asyncio.to_thread(blocking_func, *args, **kwargs)`

### Tier 2 (Debugging)
```python
import asyncio

async def run_batch(tools):
    return await asyncio.gather(*(t.run() for t in tools))
```

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `04_async_and_event_loops/concurrent_tools.py` for the `ThrottledToolExecutor` with `asyncio.Semaphore` and `asyncio.wait_for`.

---

## Module 05: ContextVars and Scoped State

### Tier 1 (Recall)
1. `threading.local` is bound to OS threads. Because multiple coroutines share the same thread during async event loop interleaving, they overwrite each other's thread-local values.
2. `ContextVar.set()` returns a `Token` representing the previous value. Calling `var.reset(token)` restores that value.
3. Yes, `asyncio.create_task()` copies the current context snapshot to the child task.

### Tier 2 (Debugging)
```python
tenant_ctx = ContextVar("tenant", default="anon")

async def handle_request(tenant_id, task):
    tok = tenant_ctx.set(tenant_id)
    try:
        return await task()
    finally:
        tenant_ctx.reset(tok)
```

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `05_contextvars_and_state/tenant_isolation.py`.

---

## Module 06: HTTP and REST APIs

### Tier 1 (Recall)
1. HTTP 429 Too Many Requests.
2. `Authorization: Bearer <TOKEN>`
3. Connection pooling reuses established TCP/TLS handshakes, avoiding 100-300ms overhead on every subsequent request.

### Tier 2 (Debugging)
Only retry transient codes (429, 500, 502, 503, 504); immediately raise exceptions on 400 Bad Request, 401 Unauthorized, or 403 Forbidden. Add randomized exponential backoff.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `06_http_and_rest_apis/resilient_session.py`.

---

## Module 07: JSON Parsing, Schema Validation, and Heuristic Repair

### Tier 1 (Recall)
1. `json.JSONDecodeError`
2. `true`, `false`, and `null`
3. LLMs are trained on markdown code blocks and treat backticks as standard formatting delimiters.

### Tier 2 (Debugging)
Use regular expressions or boundary searches rather than hardcoded string splits.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `07_json_and_schema_validation/repair_malformed_json.py` for full fence extraction, quote replacement, literal substitution, and stack bracket balancing.

---

## Module 08: Configuration Management and Secret Masking

### Tier 1 (Recall)
1. CLI Arguments > OS Environment Variables > `.env` file > Default Values.
2. `secret.get_secret_value()`
3. `.env` files contain sensitive API credentials that will be harvested by bots if committed to public repositories.

### Tier 2 (Debugging)
Cast through `float()` first or use `pydantic-settings` to handle type conversion declaratively.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `08_config_management/config_manager.py` and `env_settings.py`.

---

## Module 09: Subprocesses and Sandboxing

### Tier 1 (Recall)
1. `shell=True` invokes `/bin/sh` to interpret command strings, allowing metacharacters like `;`, `&&`, and `|` to execute injected commands.
2. `timeout` parameter in `subprocess.run(..., timeout=N)`.
3. `os.path.realpath(path)` resolves all symlinks and `..` segments to evaluate canonical absolute paths.

### Tier 2 (Debugging)
```python
subprocess.run(["python3", "runner.py", "--user", username], shell=False)
```

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `09_subprocesses_and_sandboxing/sandboxed_runner.py`.

---

## Module 10: SQLite and Agent Memory

### Tier 1 (Recall)
1. `sqlite3.connect(":memory:")`
2. `PRAGMA journal_mode = WAL;`
3. Parameterized queries compile the SQL query plan before binding parameter values, preventing values from being interpreted as SQL syntax.

### Tier 2 (Debugging)
Wrap operations in `with conn:` or explicitly call `conn.commit()`.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `10_sqlite_and_memory/message_store.py`.

---

## Module 11: Architecture Patterns

### Tier 1 (Recall)
1. `IDLE`, `PLANNING`, `EXECUTING`, `EVALUATING`, `FINISHED`, `ERROR`.
2. A boolean check evaluated before allowing a transition (e.g. `current_steps < max_steps`).
3. DI allows dependencies (database, model provider, tool dispatcher) to be swapped with mocks during unit tests.

### Tier 2 (Debugging)
Always enforce a maximum step limit ($N \le \text{max\_steps}$) to prevent runaway execution loops.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `11_architecture_patterns/state_machine.py` and `dependency_injection.py`.

---

## Module 12: Prompt Templating

### Tier 1 (Recall)
1. LLMs are trained to respect XML delimiter boundaries, helping them distinguish untrusted context from system instructions.
2. Few-shot examples provide concrete input/output demonstrations that constrain syntax formatting.
3. Escape angle brackets (`<` $\rightarrow$ `&lt;`, `>` $\rightarrow$ `&gt;`).

### Tier 2 (Debugging)
Add `re.DOTALL` to regex searches matching across multiple lines.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `12_prompt_templating/structured_protocol.py`.

---

## Module 13: Logging and Observability

### Tier 1 (Recall)
1. `timestamp`, `level`, `logger`, `message`, `trace_id`, `duration_ms`.
2. A `trace_id` tracks an entire end-to-end request; a `span_id` tracks a specific timed sub-operation within that trace.
3. Token usage translates directly to dollar costs and request latency; unmonitored agents can trigger massive cloud billing spikes.

### Tier 2 (Debugging)
Configure standard logging with a JSON formatter and contextual filters.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `13_logging_and_observability/trace_context.py`.

---

## Module 14: Streaming and SSE

### Tier 1 (Recall)
1. An async generator uses `yield` within an `async def` function, yielding values lazily over time and consumed via `async for`.
2. `event: <name>\ndata: <json>\n\n`
3. Tool arguments arrive fragmented across multiple streaming tokens; parsing incomplete chunks raises `JSONDecodeError`.

### Tier 2 (Debugging)
Use `async for token in stream:` instead of standard `for`.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `14_streaming_and_sse/sse_streamer.py`.

---

## Module 15: Mathematics Bridges

### Tier 1 (Recall)
1. Range $[-1.0, 1.0]$.
2. The probability distribution converges to an argmax one-hot vector (1.0 for the highest logit, 0.0 for all others).
3. The formula is $E[U] = \sum P(\text{outcome}) \cdot \text{Utility}(\text{outcome})$.

### Tier 2 (Debugging)
Denominator must be $\sqrt{\sum u_i^2} \sqrt{\sum v_i^2}$.

### Tier 3 & Tier 4 (Application & Challenge)
Refer to `15_math_bridges/vector_search.py` and `math_bridges.py`.
