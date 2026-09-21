"""Module 31: Python Project Structure"""
print("""
Typical serious Python project layout:

my_agent/
├── README.md               ← project description
├── pyproject.toml          ← build/dependency metadata (modern)
├── requirements.txt        ← pinned dependencies
├── src/
│   └── my_agent/
│       ├── __init__.py     ← marks directory as a Python package
│       ├── agent.py        ← orchestration logic
│       ├── tools.py        ← tool functions
│       ├── memory.py       ← SQLite persistence
│       └── config.py       ← configuration loading
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   └── conftest.py         ← pytest fixtures
└── examples/
    └── basic_usage.py

Key points:
  - src/ layout prevents accidental imports from root
  - tests/ is separate from src/
  - __init__.py makes directories importable as packages
  - pyproject.toml replaces setup.py in modern Python
""")
