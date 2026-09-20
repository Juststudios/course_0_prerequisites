# Course 0: Prerequisites for AI Agent Engineering

Welcome to **Course 0: AI Agent Prerequisites**.

Modern AI agent frameworks (such as AutoGen, LangGraph, CrewAI, Semantic Kernel, and autonomous coding agents) are often introduced with high-level abstractions that hide the underlying mechanics. When agents fail—running into infinite loops, leaking context across tenants, failing to parse malformed JSON, timing out on subprocess execution, or hitting database lock contention—developers without deep systems fluency struggle to debug them.

This course bridges classical Python software engineering and modern AI agent architecture. It takes you from fundamental Python callables to a fully functional, autonomous, persistent **MiniAgent** with zero external API dependencies.

---

## Pedagogical Structure

Every module in this course rigorously follows our standardized instructional framework:

$$\text{TERM} \longrightarrow \text{DEFINITION} \longrightarrow \text{INTUITION} \longrightarrow \text{WHY IT EXISTS} \longrightarrow \text{HOW IT WORKS} \longrightarrow \text{CODE}$$

In addition, each module includes:
1. **Learning Objectives**: Clear capabilities you will acquire.
2. **Why AI Agent Engineers Need This**: Concrete production relevance.
3. **Real-World Failure Modes & Anti-Patterns**: Pitfalls that cause production outages in agent swarms.
4. **Progressive 4-Tier Exercises**:
   - **Tier 1 (Recall)**: Conceptual and mechanical verification.
   - **Tier 2 (Debugging)**: Diagnosing and correcting broken agent implementations.
   - **Tier 3 (Application)**: Building practical agent utilities from scratch.
   - **Tier 4 (Challenge)**: Architectural integration problems.
5. **Runnable Python Scripts**: Standalone demonstration scripts with automated self-tests in `if __name__ == "__main__":`.

---

## Curriculum Roadmap (15 Modules)

| # | Module | Core Concepts | Standalone Scripts |
|---|--------|---------------|-------------------|
| **01** | [Callables & Functional Python](01_callables_and_functional_python/) | First-class functions, `__call__`, closures, decorators, signature introspection, tool registration | `callables_demo.py`, `tool_decorator.py` |
| **02** | [Classes, Dunder & OOP](02_classes_dunder_and_oop/) | `__repr__`, context managers (`__enter__`/`__exit__`), ABCs, polymorphic LLM providers | `dunder_patterns.py`, `abstract_providers.py` |
| **03** | [Type Hints & Pydantic](03_type_hints_and_pydantic/) | Generics, Pydantic v2 `BaseModel`, `Field` constraints, JSON schema extraction, error correction | `pydantic_schemas.py`, `runtime_validation.py` |
| **04** | [Async & Event Loops](04_async_and_event_loops/) | Coroutines, `asyncio.gather`, `asyncio.Semaphore`, timeouts, thread offloading | `async_basics.py`, `concurrent_tools.py` |
| **05** | [ContextVars & State](05_contextvars_and_state/) | `ContextVar`, task-local storage, token lifecycle, tenant and trace isolation | `contextvars_demo.py`, `tenant_isolation.py` |
| **06** | [HTTP & REST APIs](06_http_and_rest_apis/) | Async HTTP client, headers, connection pooling, status codes, exponential backoff with jitter | `rest_client.py`, `resilient_session.py` |
| **07** | [JSON & Schema Validation](07_json_and_schema_validation/) | `json.loads`/`dumps`, markdown fence stripping, bracket balancing, heuristic LLM JSON repair | `json_validation.py`, `repair_malformed_json.py` |
| **08** | [Config Management](08_config_management/) | Environment variables, `.env` parsing, precedence hierarchies, `pydantic-settings`, `SecretStr` | `config_manager.py`, `env_settings.py` |
| **09** | [Subprocesses & Sandboxing](09_subprocesses_and_sandboxing/) | Safe process execution, injection defense (`shell=False`), timeouts, path sandboxing | `subprocesses_demo.py`, `sandboxed_runner.py` |
| **10** | [SQLite & Agent Memory](10_sqlite_and_memory/) | Connection lifecycle, WAL mode, ACID transactions, relational message stores, `:memory:` | `sqlite_basics.py`, `message_store.py` |
| **11** | [Architecture Patterns](11_architecture_patterns/) | Pipeline pattern, Finite State Machines (FSM), state guards, Dependency Injection | `state_machine.py`, `dependency_injection.py` |
| **12** | [Prompt Templating](12_prompt_templating/) | Template engines, variable validation, XML delimiter boundaries, few-shot prompt construction | `prompt_templates.py`, `structured_protocol.py` |
| **13** | [Logging & Observability](13_logging_and_observability/) | Structured JSON logs, trace/span ID hierarchy, token usage accounting, audit trails | `agent_logger.py`, `trace_context.py` |
| **14** | [Streaming & SSE](14_streaming_and_sse/) | Async generators (`yield`), Server-Sent Events (SSE), token streaming, tool call delta assembly | `async_token_stream.py`, `sse_streamer.py` |
| **15** | [Math Bridges for Agents](15_math_bridges/) | Vector embeddings, cosine similarity, top-k RAG, loss gradients, softmax with temperature | `vector_search.py`, `math_bridges.py` |

---

## Capstone Project: `mini_agent`

Located in [`mini_agent/`](mini_agent/), this modular project synthesizes all 15 modules into an autonomous agent runtime:
- **`config.py`**: Validated settings via Pydantic.
- **`models.py`**: Strongly-typed message, tool call, and step schemas.
- **`memory.py`**: Persistent SQLite memory with WAL mode, session tracking, and audit trails.
- **`tools.py`**: Extensible tool registry with `@tool` schema extraction and safe AST calculator.
- **`engine.py`**: Deterministic ReAct reasoning loop (Thought $\rightarrow$ Action $\rightarrow$ Observation $\rightarrow$ Answer).
- **`agent.py`**: Async coordinator with `ContextVar` trace ID propagation and retry loops.
- **`main.py`**: Multi-task interactive CLI demonstration.
- **`tests/test_mini_agent.py`**: Comprehensive test suite verifying all system components.

---

## How to Run & Verify

### Running Any Demonstration Script
All scripts are standalone and self-testing:
```bash
python3 course_0_prerequisites/01_callables_and_functional_python/callables_demo.py
python3 course_0_prerequisites/05_contextvars_and_state/tenant_isolation.py
python3 course_0_prerequisites/15_math_bridges/vector_search.py
```

### Running the Capstone Project
```bash
python3 -m course_0_prerequisites.mini_agent.main
```

### Running the Capstone Pytest Suite
```bash
pytest course_0_prerequisites/mini_agent/tests/ -v
```
