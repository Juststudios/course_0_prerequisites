# Topic: Python Strings and Text Processing

## What You Will Learn
- The core nature of Python strings as immutable sequences of Unicode characters.
- String literals, escape sequences (`\n`, `\t`, `\\`), raw strings (`r"..."`), and multiline strings (`"""..."""`).
- 0-based and negative indexing, along with powerful slicing syntax (`[start:stop:step]`).
- Why strings are strictly immutable and how memory allocation differs between string concatenation and `''.join()`.
- Modern text formatting: f-strings (`f"{val:.2f}"`), format specifiers, and the Python 3.8+ debugging syntax (`f"{var=}"`).
- Crucial string manipulation methods: `.strip()`, `.split()`, `.join()`, `.replace()`, `.find()`, `.startswith()`, and `.endswith()`.
- Unicode encoding/decoding (`utf-8`) and byte transitions.
- How AI agents rely on strings for prompt templating, markdown code block extraction, and structured output parsing.

## Prerequisites
- Completion of Module 03 ("Variables and Data Types") and Module 04 ("Operators").
- Understanding of variables, data types, and basic sequence concepts.
- Familiarity with command-line script execution.

## The Problem
Human communication happens primarily through natural language: words, sentences, transcripts, and documents. Similarly, modern Large Language Models (LLMs) and web APIs communicate almost entirely through textual streams (JSON, markdown, HTTP headers, code blocks).

However, text is messy. User input contains stray leading and trailing whitespace. URLs contain encoded characters. File paths on Windows use backslashes while Linux uses forward slashes. LLMs wrap code in markdown delimiters like ```` ```python ... ``` ```` that crash Python interpreters if executed verbatim. 

To build robust software, data processing pipelines, and AI agents, you must be able to inspect, clean, slice, format, and reassemble text predictably and efficiently.

## Key Terminology
- **String (`str`)**: An immutable ordered sequence of Unicode code points representing textual characters.
- **Immutability**: A property of an object meaning its internal contents cannot be altered after creation. Any modification produces a brand new string in memory.
- **Index**: The numeric position of a character within a string. Python uses 0-based indexing for forward traversal and negative indexing for backward traversal.
- **Slice**: An expression (`string[start:stop:step]`) that extracts a contiguous sub-sequence from a sequence without modifying the original.
- **Escape Sequence**: A character combination beginning with a backslash (`\`) used to encode characters that cannot easily be typed directly, such as newlines (`\n`) or quotes (`\"`).
- **Raw String (`r"..."`)**: A string literal where backslashes are treated as literal characters rather than escape character prefixes, essential for regex patterns and file paths.
- **f-string (Formatted String Literal)**: A string prefixed with `f` or `F` that allows Python expressions to be evaluated inside curly braces `{}` at runtime.
- **Unicode**: The universal character encoding standard that assigns a unique numeric identifier (code point) to every character, symbol, and emoji across all written languages.

## Intuition
Imagine a string as a printed strip of photographic film negatives:
1. **Frames and Indexes**: Each frame on the film holds one character. Frame 0 is the very first character; Frame 1 is the second. If you count backwards from the end, Frame -1 is the last frame, and Frame -2 is the second to last.
2. **Immutability**: Once the film is developed in the darkroom, you cannot erase or paint over a single frame. If you want to change "cat" to "bat", you cannot physically alter the "c". Instead, you cut out the "at" frames, manufacture a new "b" frame, and splice them together onto a brand-new strip of film.
3. **Slicing**: Slicing is like taking a pair of scissors and cutting out frames from start to stop. The original film strip remains untouched in the archive.
4. **f-strings**: An f-string is like a dynamic template transparency where designated cutouts `{}` are filled with live camera footage right before projection.

## Concept

### 1. String Creation & Escape Sequences
Python supports single, double, and triple quotes:
```python
single = 'Hello'
double = "World"
multiline = """Line 1
Line 2"""
escaped = "First line\nSecond line\tIndented"
raw_path = r"C:\Users\agent\new_data"  # Backslashes are not treated as escapes!
```

### 2. Indexing and Slicing
- Forward indexing begins at `0` and goes to `len(s) - 1`.
- Negative indexing begins at `-1` (last character) and goes to `-len(s)`.
- Slicing syntax: `sequence[start:stop:step]`
  - `start` is inclusive (default: 0).
  - `stop` is exclusive (default: end of string).
  - `step` determines stride and direction (default: 1).
  - `s[::-1]` reverses the string!

```python
msg = "PythonAgent"
print(msg[0])     # 'P'
print(msg[-1])    # 't'
print(msg[0:6])   # 'Python' (characters 0 to 5)
print(msg[6:])    # 'Agent' (character 6 through end)
print(msg[::-1])  # 'tnegAnolhtyP'
```

### 3. Immutability & Safe Construction
Strings cannot be modified in-place:
```python
s = "hello"
# s[0] = "H"  # CRASH: TypeError: 'str' object does not support item assignment!
s = "H" + s[1:]  # Correct: Creates a new string "Hello"
```

### 4. Modern String Formatting (f-strings)
Introduced in Python 3.6, f-strings are fast, readable, and expressive:
```python
name = "Agent-X"
accuracy = 0.98234
latency = 45

# Embedded expressions and format specifiers
print(f"Agent: {name.upper()}")
print(f"Accuracy: {accuracy:.1%}")       # Formats as 98.2%
print(f"Latency: {latency:04d}ms")       # Zero-padded to 4 digits: 0045ms
print(f"{name=}")                        # Debugging output: name='Agent-X'
```

### 5. High-Frequency String Methods
- **Cleaning**: `s.strip()` (removes leading/trailing whitespace), `s.lstrip()`, `s.rstrip()`.
- **Search & Validate**: `s.startswith("prefix")`, `s.endswith(".json")`, `s.find("query")`, `"needle" in haystack`.
- **Splitting & Joining**:
  ```python
  csv_row = "item1,item2,item3"
  items = csv_row.split(",")           # ['item1', 'item2', 'item3']
  rejoined = " | ".join(items)         # "item1 | item2 | item3"
  ```
- **Replacement**: `s.replace(old, new, count)`.

## Syntax
```python
# Slicing
sub = text[start:stop]
stride = text[::2]
reversed_str = text[::-1]

# Formatting
formatted = f"Agent {id_num}: score = {score:.2f}, status = {status.lower()}"

# Method Chaining
cleaned = raw_text.strip().lower().replace(" ", "_")

# Splitting and Joining
parts = log_line.split(" - ")
reconstructed = ", ".join(parts)
```

## Example
Here is a comprehensive text-processing engine demonstrating slicing, cleaning, f-strings, and extracting structured code blocks from an LLM response:

```python
# LLM Response Parser & Cleaner

raw_llm_response = """
Here is the Python script you requested:
```python
def calculate_trajectory(v, angle):
    import math
    return v * math.cos(math.radians(angle))
```
Hope that helps!
"""

print("--- Step 1: Searching for Code Block ---")
fence_start = "```python"
fence_end = "```"

start_idx = raw_llm_response.find(fence_start)
if start_idx != -1:
    content_start = start_idx + len(fence_start)
    end_idx = raw_llm_response.find(fence_end, content_start)
    if end_idx != -1:
        extracted_code = raw_llm_response[content_start:end_idx].strip()
        print("Successfully extracted code block:")
        print(extracted_code)
    else:
        print("Closing fence not found.")
else:
    print("Opening fence not found.")

print("\n--- Step 2: Line-by-Line Normalization ---")
raw_tags = "  ai , agent,   python ,  automation , machine_learning  "
clean_tags = [tag.strip().lower() for tag in raw_tags.split(",")]
print("Clean tags list:", clean_tags)

tag_string = " #".join([""] + clean_tags).strip()
print(f"Generated hashtag string: {tag_string}")
```

## Line-by-Line Explanation
- `raw_llm_response = """..."""`: Defines a multiline string literal containing newlines, markdown fences, and explanatory conversational filler text.
- `start_idx = raw_llm_response.find(fence_start)`: Uses `.find()` to locate the 0-based character index where `"```python"` begins. Returns `-1` if not found.
- `content_start = start_idx + len(fence_start)`: Computes the exact index immediately following the fence delimiter.
- `end_idx = raw_llm_response.find(fence_end, content_start)`: Searches for the closing fence `"```"` starting *after* the opening fence.
- `extracted_code = raw_llm_response[content_start:end_idx].strip()`: Slices the substring between the fences and calls `.strip()` to discard leading/trailing newlines.
- `raw_tags.split(",")`: Splits the string on comma delimiters into a list of strings with uncleaned whitespace.
- `tag.strip().lower()`: Strips whitespace from each individual element and converts characters to lowercase.
- `" #".join(...)`: Concatenates the cleaned tokens into a single formatted hashtag string.

## What Python Is Doing
1. **Unicode Representation (PEP 393 - Flexible String Representation)**:
   CPython optimizes string memory based on the highest code point in the string:
   - Latin-1 (ASCII / Western): 1 byte per character (`PyASCIIObject`).
   - UCS-2 (BMP, Asian scripts): 2 bytes per character.
   - UCS-4 (Emojis, rare scripts): 4 bytes per character.
   This ensures indexing `s[i]` is always an $O(1)$ constant-time pointer calculation, regardless of the alphabet!
2. **String Interning**: CPython automatically interns short strings, variable identifiers, and dictionary keys. If two strings are interned, `s1 is s2` evaluates to `True` because they share the identical memory address.
3. **The Danger of `+=` in Loops**: Because strings are immutable, writing `s += char` inside a loop of $N$ iterations can trigger $O(N^2)$ memory copying if CPython's in-place reallocation optimization cannot be applied. Using `''.join(list_of_strings)` is strictly $O(N)$ and should always be preferred.

## Common Mistakes
1. **Attempting In-Place Character Mutation**:
   ```python
   s = "python"
   s[0] = "P"  # CRASH: TypeError! Strings are immutable.
   ```
2. **Off-by-One Slicing Errors**:
   Remember that the `stop` index in `s[start:stop]` is exclusive.
   `"python"[0:2]` returns `"py"` (indexes 0 and 1, NOT 2).
3. **Using `.find()` vs `.index()`**:
   - `s.find("missing")` returns `-1`.
   - `s.index("missing")` raises `ValueError`.
   Using `.find()` without checking for `-1` causes bugs because `-1` is a valid slice/index in Python!
4. **Forgetting that String Methods Return New Strings**:
   ```python
   text = "  hello  "
   text.strip()  # Does NOT modify text!
   print(text)   # Still "  hello  "
   text = text.strip()  # Correct: Rebind the variable to the returned new string
   ```

## Real-World Uses
- **HTTP URL & Query Parameter Construction**: Slicing paths, parsing tokens, and formatting API URLs.
- **Log Parsing & Auditing**: Slicing timestamps, log levels, and stack traces from server logs using `.split()` and regex.
- **Data Normalization in ETL Pipelines**: Stripping punctuation, standardizing phone numbers, and converting dirty spreadsheet inputs to clean uniform text.
- **Template Engines**: Dynamically generating HTML, emails, and markdown reports from backend data models.

## Connection to AI Agents
Modern AI systems live and breathe text:
- **Prompt Engineering & Dynamic Injection**: Agents assemble complex system prompts by embedding conversation history, user personas, and real-time tool documentation into template strings using f-strings.
- **Tool Call Extraction**: When an LLM generates a tool invocation, the agent framework must parse function names and arguments out of raw response strings (stripping markdown backticks and whitespace).
- **Context Window Management**: Agents slice long text documents into smaller chunks using character or subword slices to fit inside model token limits.
- **ReAct Parsing**: Parsing `Thought: ... Action: ... Observation: ...` agent loops requires robust string splitting and line-by-line inspection.

## Practice
1. Take the string `"Autonomous Agent Architecture"`:
   - Print its length using `len()`.
   - Slice the first word (`"Autonomous"`).
   - Slice the last word (`"Architecture"`).
   - Reverse the entire string using `[::-1]`.
2. Format a floating-point score: given `score = 0.95729`, format it as a percentage with 2 decimal places (`95.73%`) using an f-string.
3. Clean user input: given `raw = "  \n  Agent_007 \t "`, remove all surrounding whitespace and convert to lowercase.
4. Experiment with `.split()`: split `"apple,banana,cherry,dates"` by comma and rejoin with `" -> "`.

## Challenge
Implement a robust markdown sanitizer function:
1. Accept an arbitrary LLM response containing conversational text and code blocks.
2. Extract all code blocks enclosed in triple backticks ```` ```[language] ... ``` ````.
3. For each block, return a tuple `(language, code_body)` where leading and trailing whitespace are stripped.
4. If no language was specified (e.g. ```` ``` ... ``` ````), default the language identifier to `"text"`.

## Summary
- Strings are immutable sequences of Unicode characters; every modification creates a new object.
- Indexing is 0-based forward and negative backward; slicing is `[start:stop:step]` with an exclusive stop.
- f-strings (`f"{expr}"`) provide readable, performant formatting with rich format specifiers (`.2f`, `04d`, `>10`).
- Use `.strip()`, `.split()`, `.join()`, and `.replace()` for fast, clean text manipulation.
- In-place string accumulation in loops should be replaced with `"".join(chunks)` for linear performance.
- AI agents rely on strings to build prompts, sanitize model completions, and parse tool arguments.

## What You Should Know Before Moving On
Before advancing to Module 06 ("Collections"), verify that you can:
- Predict the exact character slice produced by `s[start:stop:step]` with positive and negative indexes.
- Explain why strings are immutable and what error occurs if you try to mutate a character.
- Format numbers, percentages, and expressions cleanly using f-strings.
- Clean dirty text using `.strip()`, `.lower()`, and `.replace()`.
- Explain how an AI agent extracts executable code from markdown-formatted LLM responses.
