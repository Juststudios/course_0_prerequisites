## 2026-09-20T12:34:43Z
You are explorer_survey_c0.
Your working directory is: /home/settings/Documents/pearl/.agents/explorer_survey_c0/
Project workspace root: /home/settings/Documents/pearl

MANDATORY FIRST STEP: Read /home/settings/Documents/pearl/ORIGINAL_REQUEST.md, specifically the latest user request under "## Follow-up — 2026-09-20T12:32:36Z" regarding R1. Build Course 0 (AI Agent Prerequisites).

Your mission is to conduct an in-depth survey of requirements and the existing repository state for Course 0:
1. Examine what currently exists in /home/settings/Documents/pearl/ (check for any existing course_0_prerequisites, existing curricula styles, python versions, installed packages).
2. Detail the exact 15 modules needed to bridge basic Python to AI-agent engineering:
   - Callables & Functional Python
   - Classes, Dunder Methods & OOP Patterns
   - Type Hints, Generics & Pydantic / Runtime Validation
   - Async/Await, Asyncio Event Loops & Tasks
   - ContextVars & Request/Task-Scoped State
   - HTTP Requests, Sessions & REST APIs
   - JSON Parsing, Schema Validation & Serialization
   - Config Management (Env vars, .env, Settings classes)
   - Subprocesses, CLI execution & Tool Sandboxing
   - SQLite, Transactions, In-Memory DBs & Agent Memory
   - Architecture Patterns (Pipelines, State Machines, Dependency Injection)
   - Prompt Templating & Structured Output Protocols
   - Logging, Observability & Tracing in Agents
   - Streaming, Generators & Server-Sent Events
   - Math Bridges for AI Agents (Linear Algebra/Vector embeddings, Calculus/Loss gradients, Probability/Confidence scores for agents)
3. Detail the runnable Python files needed across the modules (including contextvars_demo.py, async_basics.py, sqlite_basics.py, etc.).
4. Detail the mini_agent runnable skeleton project requirements (combining async, sqlite memory, tool registry, error handling, runnable end-to-end without external API keys needed e.g. mock/local model or deterministic reasoning engine).
5. Detail pedagogical documentation requirements: Every lesson must strictly follow the format:
   TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE.

Deliverables:
- Keep your progress.md updated with timestamps.
- Write your comprehensive survey report to /home/settings/Documents/pearl/.agents/explorer_survey_c0/handoff.md.
- Send a message to the parent orchestrator with the handoff path once complete.
