# Module 05: ContextVars and Scoped State Management in AI Agents

## 1. Learning Objectives
By the end of this module, you will be able to:
- Contrast thread-local storage (`threading.local`) with task-local storage (`contextvars.ContextVar`) in concurrent asynchronous runtimes.
- Propagate contextual metadata (such as `trace_id`, `user_id`, `session_id`, and `budget_limit`) deeply into nested agent function calls without polluting parameter signatures.
- Manage the exact lifecycle of context tokens using `var.set()` and `var.reset(token)` to eliminate context bleeding.
- Ensure strict tenant isolation when dozens of agent tasks execute concurrently within the same Python process.
- Inspect and copy execution contexts using `contextvars.copy_context()` for background worker tasks.

---

## 2. Why AI Agent Engineers Need This
In modern agent services (e.g. multi-tenant web servers running LangGraph, FastAPI, or Swarm frameworks), many agent sessions run concurrently on a single event loop.

If you use global variables (`GLOBAL_USER_ID = "alice"`), concurrent task switching will immediately cause Alice's agent to read Bob's API key, or write audit logs under Charlie's billing account.
On the other hand, manually passing `trace_id`, `tenant_id`, `span_id`, and `auth_token` through 15 layers of helper functions (`agent -> engine -> tool_registry -> tool -> db_adapter`) creates unmaintainable signature pollution.

Python's `contextvars` module solves this by providing **asynchronous task-local storage**: variables that are globally accessible in syntax, but strictly isolated to the currently executing asynchronous task hierarchy.

---

## 3. Structured Concept Breakdown

### Concept 1: ContextVar
- **TERM**: ContextVar
- **DEFINITION**: A standard library class from `contextvars` that declares a variable whose value is local to the current asynchronous context and inherited by spawned child tasks.
- **INTUITION**: A traveler's personal passport. Wherever the traveler goes within the airport (across nested function calls), the passport belongs strictly to them. Other travelers in the same airport terminal carry their own distinct passports.
- **WHY IT EXISTS**: In async Python, multiple tasks interleave on the same thread. `threading.local` fails because all tasks on the thread see the same value. `ContextVar` isolates state per async task.
- **HOW IT WORKS**: When an async task is scheduled or resumes on the event loop, Python restores that task's active `Context` dictionary. Accessing `my_var.get()` looks up the value in that task-specific context.
- **CODE**:
```python
import contextvars

# Declare context variable with default
current_trace_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "current_trace_id", default="untraced"
)

# Set and retrieve
token = current_trace_id.set("trace_abc_123")
print(current_trace_id.get())  # 'trace_abc_123'
current_trace_id.reset(token)
print(current_trace_id.get())  # 'untraced'
```

---

### Concept 2: Task-Local Storage vs Thread-Local Storage
- **TERM**: Task-Local Storage
- **DEFINITION**: Storage mechanism where variable state is tied to the lifecycle of an `asyncio.Task` rather than an OS thread.
- **INTUITION**: In an office with shared desks (a thread), multiple workers (tasks) take turns sitting at a desk. Thread-local storage writes on the desk itself, so worker B sees worker A's notes. Task-local storage gives each worker their own personal notebook they bring to the desk.
- **WHY IT EXISTS**: In an async web service, request A and request B both execute on Thread 1. Thread-local variables will corrupt state between request A and request B. Task-local storage ensures request A and B have separate state.
- **HOW IT WORKS**: Each `asyncio.Task` maintains an internal reference to a `contextvars.Context` object. Context switches swap this pointer.
- **CODE**:
```python
import asyncio
import contextvars

tenant_var: contextvars.ContextVar[str] = contextvars.ContextVar("tenant_var", default="anon")

async def worker(tenant_name: str):
    tenant_var.set(tenant_name)
    await asyncio.sleep(0.01)  # Context switch occurs here!
    # Correct tenant is preserved across the context switch
    assert tenant_var.get() == tenant_name
```

---

### Concept 3: Context Inheritance Across Tasks
- **TERM**: Context Inheritance
- **DEFINITION**: The automatic copying of the current context snapshot when spawning a new child task via `asyncio.create_task()`.
- **INTUITION**: Genetic inheritance. A child receives a copy of their parent's genetic traits at birth, but subsequent mutations in the child do not alter the parent's genes.
- **WHY IT EXISTS**: When an agent spawns sub-tasks (e.g. 3 background tool searches), each child sub-task must inherit the parent's `trace_id` and `user_id` so that sub-task logs correlate with the parent request.
- **HOW IT WORKS**: `asyncio.create_task()` internally calls `contextvars.copy_context()` to initialize the child task's context with a snapshot of the parent's current values. Mutations made in the child task remain isolated to that child.
- **CODE**:
```python
async def parent_task():
    current_trace_id.set("trace_parent_999")
    # Child task automatically inherits "trace_parent_999"
    task = asyncio.create_task(child_task())
    await task

async def child_task():
    # Child sees parent's trace ID
    print(f"Child inherited: {current_trace_id.get()}")
```

---

### Concept 4: Token Lifecycle & Resetting
- **TERM**: ContextVar Token
- **DEFINITION**: An opaque object returned by `ContextVar.set()` that represents the prior state of the variable, used to restore the variable via `ContextVar.reset(token)`.
- **INTUITION**: A coat check claim ticket. When you check your coat (`set`), you get a ticket (`token`). When you return the ticket (`reset`), you get your original coat back.
- **WHY IT EXISTS**: In middleware or agent step loops, you may temporarily override state (e.g. setting a temporary sub-trace ID during a tool call). After the tool call completes, state must be cleanly restored without leaking into subsequent steps.
- **HOW IT WORKS**: `token = var.set(new_val)` captures the previous value. Calling `var.reset(token)` validates that the token belongs to this variable and resets the context entry.
- **CODE**:
```python
def run_with_temporary_tenant(tenant: str, func):
    token = tenant_var.set(tenant)
    try:
        return func()
    finally:
        tenant_var.reset(token)  # Guaranteed cleanup
```

---

### Concept 5: Preventing Context Leaks
- **TERM**: Context Leaking
- **DEFINITION**: A bug where state set during one agent request lingers in the execution context and is accidentally read by subsequent requests.
- **INTUITION**: Leaving someone else's sensitive documents on a shared conference table after a meeting ends.
- **WHY IT EXISTS**: Without strict token resetting or per-request task boundaries, worker coroutines reused across requests (e.g. connection pool callbacks) will retain stale state.
- **HOW IT WORKS**: Context leaks are prevented by always pairing `.set()` with `.reset(token)` in a `try...finally` block, or by running entry points inside isolated `asyncio.create_task()` or `copy_context().run()`.
- **CODE**:
```python
async def handle_agent_request(trace_id: str, request_coro):
    token = current_trace_id.set(trace_id)
    try:
        await request_coro
    finally:
        current_trace_id.reset(token)
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Mutable Objects Inside ContextVars
- **The Bug**: Storing a mutable list or dictionary inside a ContextVar: `active_tools: ContextVar[list] = ContextVar("tools", default=[])`.
- **The Consequence**: Because `copy_context()` performs a shallow copy, child tasks mutating the list via `active_tools.get().append("bad_tool")` mutate the parent's and siblings' lists, corrupting state globally!
- **The Fix**: Always store immutable objects (strings, ints, tuples, frozen dataclasses) in ContextVars.

### Anti-Pattern 2: Forgetting to Reset Tokens in Loops
- **The Bug**: Calling `var.set(sub_id)` inside a retry loop without resetting the token upon exceptions.
- **The Consequence**: Deep stack accumulation of unreset tokens and incorrect context state in exception handlers.
- **The Fix**: Always use `try...finally` blocks around `.set()` and `.reset()`.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What does `ContextVar.set()` return?
2. Does `threading.local` safely isolate state between two coroutines running concurrently on the same thread?
3. When `asyncio.create_task()` is called, what happens to the parent task's context?

### Tier 2 (Debugging)
Identify the flaw in this middleware:
```python
user_var = ContextVar("user", default=None)

async def process_user_action(user_id, action_coro):
    user_var.set(user_id)
    result = await action_coro()
    # What happens if action_coro() raises an exception?
    return result
```
*Hint*: If an exception occurs, the token is never reset! Wrap with `try...finally`.

### Tier 3 (Application)
Implement a context manager `ScopedContext(var: ContextVar[T], value: T)` that sets the context variable on `__enter__` and resets it via its token on `__exit__`.

### Tier 4 (Challenge)
Create a `MultiTenantAgentDispatcher` that spawns 10 concurrent agent tasks for 10 different tenants (`tenant_1` through `tenant_10`). Each task must make 3 simulated tool calls that verify deep in their call stacks that `tenant_var.get()` matches their assigned tenant without a single collision.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/05_contextvars_and_state/contextvars_demo.py
python3 course_0_prerequisites/05_contextvars_and_state/tenant_isolation.py
```
