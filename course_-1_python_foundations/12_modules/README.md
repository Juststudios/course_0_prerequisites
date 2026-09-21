# Module 12: Modules and Imports

## Key Terminology
| Term | Definition |
|------|------------|
| **Module** | A `.py` file you can import |
| **Package** | A directory with `__init__.py` making it importable |
| **`import`** | Load a module into the current namespace |
| **`from X import Y`** | Import only `Y` from module `X` |
| **`__name__`** | `"__main__"` when run directly, else the module name |

## The `__name__ == "__main__"` Guard
```python
if __name__ == "__main__":
    main()   # Only runs when you execute this file directly
```
Without this guard, code runs when the file is merely imported — causing unintended side effects.

## Connection to AI Agents
Agent runtimes split their code into modules: `tools.py`, `memory.py`, `config.py`, `agent.py`. You'll see this exact structure in Course 0.
