# Module 18: Generators

## Key Terminology
| Term | Definition |
|------|-----------|
| **`yield`** | Pause the function and produce a value; resume when next() is called |
| **Generator** | A function containing `yield`; returns a generator object |
| **Lazy evaluation** | Produce values on demand rather than all at once |
| **Generator expression** | `(expr for x in iterable)` — compact generator syntax |

## Connection to AI Agents
LLMs stream responses token-by-token. The agent runtime reads these as a generator (or async generator in Course 0). Understanding `yield` now makes async streaming in Course 0 much easier.
