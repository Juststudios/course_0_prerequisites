# Module 21: Testing

## Key Terminology
| Term | Definition |
|------|-----------|
| **Assertion** | `assert condition` — raises `AssertionError` if False |
| **Unit test** | Tests a single isolated piece of code |
| **Regression** | A bug that reappears; tests prevent this |
| **pytest** | Python's most popular test runner |
| **`pytest.raises`** | Context manager that asserts an exception was raised |

## Running Tests
```bash
pytest test_example.py -v   # verbose output
pytest .                    # discover all test_*.py files recursively
```

## Connection to AI Agents
Agent runtimes have test suites that verify tool registration, async execution, SQLite operations, and JSON parsing. You've already seen 243 tests run on the Course 0 material!
