# Module 17: Iteration

## Key Terminology
| Term | Definition |
|------|-----------|
| **Iterable** | Object with `__iter__` — can be looped over |
| **Iterator** | Object with `__next__` — remembers position |
| **`iter(x)`** | Gets the iterator from an iterable |
| **`next(it)`** | Returns next value; raises `StopIteration` at end |
| **`enumerate`** | Produces `(index, value)` pairs |
| **`zip`** | Combines multiple iterables element-by-element |

## Connection to AI Agents
Agent runtimes iterate over tool results, message histories, and streaming responses. Understanding iterators helps you work with generators and async streams in Course 0.
