# Project: Course -1 Python Foundations (Complete Rewrite)

## Architecture & Pedagogical Philosophy
Course -1 (`course_-1_python_foundations/`) is the foundational prerequisite curriculum designed to take a complete beginner to an AI-agent-ready Python engineer. 
Instead of dry syntax cheat sheets, each module delivers deep conceptual intuition, mechanics ("What Python Is Doing"), common traps, real-world utility, and direct links to how AI agents utilize each concept.

### Mandatory Standards (Requirements R1 - R4)
- **R1. 18-Section Pedagogical README.md**:
  Every module MUST have a `README.md` with these exact 18 headers:
  1. `# Topic`
  2. `## What You Will Learn`
  3. `## Prerequisites`
  4. `## The Problem`
  5. `## Key Terminology`
  6. `## Intuition`
  7. `## Concept`
  8. `## Syntax`
  9. `## Example`
  10. `## Line-by-Line Explanation`
  11. `## What Python Is Doing`
  12. `## Common Mistakes`
  13. `## Real-World Uses`
  14. `## Connection to AI Agents`
  15. `## Practice`
  16. `## Challenge`
  17. `## Summary`
  18. `## What You Should Know Before Moving On`
- **R2. Detailed Python Lessons**:
  Main lesson `.py` file MUST be at least 150-200 lines long, heavily commented with narrative explanations, progressive examples (simple to complex), and clear `print()` outputs demonstrating execution.
- **R3. Authentic Exercises & Decoupled Solutions**:
  - `exercises.py`: 4 distinct levels (`Level 1: Recall`, `Level 2: Modify`, `Level 3: Build`, `Level 4: Debug`), with authentic `# TODO` comments and `raise NotImplementedError` scaffolding.
  - `solutions.py`: Completely decoupled, clean solutions implementing all exercises without TODOs or errors, executing cleanly with exit code 0.
- **R4. All 33 Modules Complete**:
  Full 100% curriculum coverage across all 33 modules.

---

## Feature Inventory
| # | Feature / Module | Topic Description | Milestone | Source |
|---|---|---|---|---|
| 01 | `01_what_programming_is` | Programming mental models, instructions, state | M1 | Survey 1 |
| 02 | `02_first_python_programs` | First scripts, Python interpreter, hello world | M1 | Survey 1 |
| 03 | `03_variables_and_data_types` | Variables, primitive types, type conversion | M1 | Survey 1 |
| 04 | `04_operators` | Arithmetic, comparison, logical, bitwise ops | M1 | Survey 1 |
| 05 | `05_strings` | Strings, formatting, slicing, string methods | M1 | Survey 1 |
| 06 | `06_collections` | Lists, tuples, sets, dicts, indexing, mutability | M1 | Survey 1 |
| 07 | `07_control_flow` | If/elif/else, for loops, while loops, breaks | M2 | Survey 1 |
| 08 | `08_functions` | Functions, args, kwargs, return, docstrings | M2 | Survey 1 |
| 09 | `09_scope` | Scope, LEGB rule, global/nonlocal, lifetimes | M2 | Survey 1 |
| 10 | `10_errors_and_exceptions` | Try/except/finally, custom exceptions, traces | M2 | Survey 1 |
| 11 | `11_files` | File I/O, context managers, paths, text/binary | M2 | Survey 1 |
| 12 | `12_modules` | Modules, packages, imports, sys.path, __all__ | M3 | Survey 2 |
| 13 | `13_classes_and_oop` | Classes, self, inheritance, polymorphism, dunder | M3 | Survey 2 |
| 14 | `14_functional_programming` | Lambdas, map, filter, comprehensions, pure funcs | M3 | Survey 2 |
| 15 | `15_type_hints` | Typing module, Union, Optional, Callable, generics | M3 | Survey 2 |
| 16 | `16_dataclasses` | Dataclasses, fields, immutability, post-init | M3 | Survey 2 |
| 17 | `17_generators` | Yield, generator expressions, pipeline processing | M4 | Survey 2 |
| 18 | `18_iterators` | Iterables, iter(), next(), itertools, protocols | M4 | Survey 2 |
| 19 | `19_decorators` | Decorators, closures, functools.wraps, params | M4 | Survey 2 |
| 20 | `20_context_managers` | Context manager protocol, contextlib.contextmanager | M4 | Survey 2 |
| 21 | `21_testing` | Unit testing, unittest, pytest assertions, fixtures | M4 | Survey 2 |
| 22 | `22_logging` | Logging levels, handlers, formatters, agent logs | M4 | Survey 2 |
| 23 | `23_virtual_environments` | venv, pip, site-packages, dependencies, isolation | M5 | Survey 3 |
| 24 | `24_async_python_intro` | Coroutines, async/await, event loop fundamentals | M5 | Survey 3 |
| 25 | `25_async_concurrency` | asyncio.gather, TaskGroup, queues, timeouts | M5 | Survey 3 |
| 26 | `26_http_and_json_intro` | HTTP methods, urllib/requests, json dumps/loads | M5 | Survey 3 |
| 27 | `27_environment_variables` | os.environ, dotenv, secure secrets for agents | M5 | Survey 3 |
| 28 | `28_subprocesses_intro` | subprocess.run, Popen, pipes, CLI tool calling | M5 | Survey 3 |
| 29 | `29_sqlite_intro` | sqlite3, schemas, queries, transactions, agent DB | M5 | Survey 3 |
| 30 | `30_basic_software_architecture` | Modularity, separation of concerns, interfaces | M6 | Survey 3 |
| 31 | `31_python_project_structure` | pyproject.toml, src layout, packaging, CLI entry | M6 | Survey 3 |
| 32 | `32_python_debugging` | pdb, tracebacks, logging vs print, breakpoint() | M6 | Survey 3 |
| 33 | `33_integrated_projects` | Capstone: Tool-using Mini ReAct Agent pipeline | M6 | Survey 3 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| **E2E** | Test Track | Automated verification harness checking R1, R2, R3, R4 | none | PLANNED |
| **M1** | Core Fundamentals | Modules 01–06 (`01_what_programming_is` to `06_collections`) | none | PLANNED |
| **M2** | Control, Functions & I/O | Modules 07–11 (`07_control_flow` to `11_files`) | M1 contracts | PLANNED |
| **M3** | OOP, Types & Modern Data | Modules 12–16 (`12_modules` to `16_dataclasses`) | M1, M2 | PLANNED |
| **M4** | Advanced Mechanics & Tooling | Modules 17–22 (`17_generators` to `22_logging`) | M3 | PLANNED |
| **M5** | Systems, Concurrency & DB | Modules 23–29 (`23_virtual_environments` to `29_sqlite_intro`) | M2, M4 | PLANNED |
| **M6** | Architecture, Packaging & Capstone | Modules 30–33 (`30_basic_software_architecture` to `33_integrated_projects`) | M1-M5 | PLANNED |
| **FINAL** | Gate & Acceptance Pass | 100% acceptance test passage & forensic audit clearance | M1-M6, E2E | PLANNED |

---

## Code Layout & Exclusive Write Ownership
All course files reside under `/home/settings/Documents/pearl/course_-1_python_foundations/`.
To prevent file collision during parallel worker execution, write ownership is strictly partitioned:
- Worker M1: Exclusive owner of `course_-1_python_foundations/0[1-6]_*`
- Worker M2: Exclusive owner of `course_-1_python_foundations/0[7-9]_*` and `1[0-1]_*`
- Worker M3: Exclusive owner of `course_-1_python_foundations/1[2-6]_*`
- Worker M4: Exclusive owner of `course_-1_python_foundations/1[7-9]_*` and `2[0-2]_*`
- Worker M5: Exclusive owner of `course_-1_python_foundations/2[3-9]_*`
- Worker M6: Exclusive owner of `course_-1_python_foundations/3[0-3]_*`
- Test Writer: Exclusive owner of `/home/settings/Documents/pearl/tests/e2e/test_course_minus_1_acceptance.py` and `scripts/verify_course_minus_1.py`
