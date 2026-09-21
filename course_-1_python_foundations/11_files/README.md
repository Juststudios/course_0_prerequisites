# Module 11: Files

## What You Will Learn
How to read, write, and manage files using Python's built-in `open()`.

## Key Terminology
| Term | Definition |
|------|------------|
| **File handle** | The object returned by `open()` that lets you read/write |
| **Mode** | `"r"` read, `"w"` write (overwrites), `"a"` append |
| **Encoding** | How characters are stored as bytes (`utf-8` is standard) |
| **Context manager** | The `with` block that guarantees cleanup |

## Common Mistakes
- Forgetting `encoding="utf-8"` → crashes on non-ASCII characters
- Using `"w"` when you meant `"a"` → data loss!
- Not using `with` → file stays open if an exception occurs

## Connection to AI Agents
Agents save conversation history to files, read config files on startup, and write logs for debugging.

## Practice
1. Write a program that saves your name and age to `profile.txt`.
2. Read `profile.txt` and print each line with its line number.
3. Append today's date to `profile.txt`.
