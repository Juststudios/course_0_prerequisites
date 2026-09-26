"""
Module 05: Strings and Text Processing in Python
================================================
This lesson explores strings as immutable sequences of Unicode characters:
literals, indexing, slicing, immutability, modern f-string formatting,
vital string manipulation methods, and parsing structured text for AI agents.

Run this script directly:
    python3 strings.py
"""

import sys

print("=" * 75)
print("MODULE 05: STRINGS & TEXT PROCESSING — IMMUTABILITY, SLICING & FORMATTING")
print("=" * 75)


# -----------------------------------------------------------------------------
# Section 1: String Literals, Escaping, and Raw Strings
# -----------------------------------------------------------------------------
# Strings can be enclosed in single, double, or triple quotes.
# Escape characters (\n, \t, \", \') allow embedding special formatting.
# Raw strings (r"...") ignore escape interpretation (vital for regex & paths).

print("\n--- [Section 1: String Literals & Escaping] ---")

single_quoted = 'Hello from Python'
double_quoted = "AI Agent Pipeline"
multiline_text = """System Instruction:
You are an autonomous coding assistant.
Follow instructions strictly."""

print(f"Single quoted: {single_quoted}")
print(f"Double quoted: {double_quoted}")
print(f"Multiline string (length {len(multiline_text)} chars):\n{multiline_text}")

# Escape sequences vs. Raw Strings:
escaped_path = "C:\\Users\\admin\\new_folder\\test.txt"
raw_path = r"C:\Users\admin\new_folder\test.txt"
print(f"\nEscaped backslashes: {escaped_path}")
print(f"Raw string literal:  {raw_path}")
print(f"Are escaped and raw strings identical in value? {escaped_path == raw_path}")


# -----------------------------------------------------------------------------
# Section 2: 0-Based and Negative Indexing
# -----------------------------------------------------------------------------
# Strings are ordered sequences of characters.
# Forward indexes: 0, 1, 2, ... len - 1
# Backward indexes: -1 (last), -2 (second to last), ... -len

print("\n--- [Section 2: Indexing Mechanics] ---")

course_name = "AgenticAI"
print(f"Target string: '{course_name}' (length: {len(course_name)})")

print(f"  First character [0]:         '{course_name[0]}'")
print(f"  Fourth character [3]:        '{course_name[3]}'")
print(f"  Last character [-1]:         '{course_name[-1]}'")
print(f"  Second to last [-2]:         '{course_name[-2]}'")

# Out-of-bounds index raises IndexError:
try:
    missing = course_name[50]
except IndexError as err:
    print(f"  Caught expected IndexError: {err}")


# -----------------------------------------------------------------------------
# Section 3: Slicing Mastery ([start:stop:step])
# -----------------------------------------------------------------------------
# Slicing extracts sub-sequences:
#   start: index to start at (inclusive, default: 0)
#   stop:  index to stop at (EXCLUSIVE, default: end of string)
#   step:  stride/direction (default: 1)
# Note: Slicing never raises IndexError on out-of-range bounds!

print("\n--- [Section 3: Slicing Mastery] ---")

phrase = "PythonEngineering"
print(f"Target phrase: '{phrase}'")

# Substring extraction:
print(f"  First 6 chars [0:6]:         '{phrase[0:6]}'")
print(f"  Omit start [:6]:             '{phrase[:6]}'")
print(f"  From index 6 to end [6:]:    '{phrase[6:]}'")
print(f"  Middle slice [6:13]:         '{phrase[6:13]}'")
print(f"  Negative slice [-11:]:       '{phrase[-11:]}'")

# Step strides and string reversal:
print(f"  Every second character [::2]: '{phrase[::2]}'")
print(f"  Reversed string [::-1]:       '{phrase[::-1]}'")

# Boundary safety of slicing:
print(f"  Slice past end [0:999]:      '{phrase[0:999]}' (Does NOT crash!)")


# -----------------------------------------------------------------------------
# Section 4: Immutability & Safe Construction
# -----------------------------------------------------------------------------
# Strings CANNOT be modified in-place. Attempting to assign to an index crashes.
# To alter a string, you must construct and return a new string.

print("\n--- [Section 4: Immutability & Safe Construction] ---")

original = "Python"
print(f"Original string: '{original}' (id: {id(original)})")

try:
    # This is forbidden in Python!
    original[0] = "J"
except TypeError as err:
    print(f"  Caught expected TypeError: {err}")

# Safe replacement by slicing and concatenation:
modified = "J" + original[1:]
print(f"Created new string via slicing: '{modified}' (id: {id(modified)})")


# -----------------------------------------------------------------------------
# Section 5: Modern f-string Formatting & Specifiers
# -----------------------------------------------------------------------------
# Formatted string literals (f-strings) evaluate Python expressions at runtime
# and support rich format specification syntax:
#   {val:.2f}  -> 2 decimal float
#   {val:.1%}  -> Percentage
#   {val:05d}  -> Zero-padded integer
#   {val:>15}  -> Right-aligned in 15 spaces
#   {val=}     -> Self-documenting debug print

print("\n--- [Section 5: Modern f-string Formatting] ---")

agent_id = 7
agent_name = "ClassifierBot"
accuracy = 0.96548
execution_time = 0.0452
memory_mb = 128

print(f"Basic interpolation: Agent #{agent_id} ({agent_name})")
print(f"Float precision (2 decimals): {accuracy:.2f}")
print(f"Percentage formatting:        {accuracy:.2%}")
print(f"Scientific notation:          {execution_time:.2e} seconds")
print(f"Zero-padded integer:          ID-{agent_id:04d}")

# Alignment and column width:
print("\nAligned tabular output:")
print(f"| {'Metric':<15} | {'Value':>10} |")
print(f"| {'-'*15} | {'-'*10} |")
print(f"| {'Accuracy':<15} | {accuracy:>10.2%} |")
print(f"| {'Memory (MB)':<15} | {memory_mb:>10d} |")

# Python 3.8+ debug specifier:
print(f"\nDebugging output with '=' specifier:")
print(f"  {agent_name=}, {accuracy=:.3f}")


# -----------------------------------------------------------------------------
# Section 6: High-Frequency String Methods
# -----------------------------------------------------------------------------
# Python's built-in str class has dozens of powerful methods.
# Remember: string methods ALWAYS return a new string; they never mutate.

print("\n--- [Section 6: High-Frequency String Methods] ---")

messy_input = "   \t--Agent State Payload-- \n  "
print(f"Messy input: {repr(messy_input)}")

# 1. Stripping whitespace or characters:
stripped = messy_input.strip()
print(f"  .strip() whitespace:      {repr(stripped)}")
clean_chars = stripped.strip("-")
print(f"  .strip('-'):              {repr(clean_chars)}")

# 2. Case transformations:
sample_text = "agent-alpha: reasoning engine"
print(f"\nCase conversions for '{sample_text}':")
print(f"  .upper():      {sample_text.upper()}")
print(f"  .lower():      {sample_text.lower()}")
print(f"  .title():      {sample_text.title()}")
print(f"  .capitalize(): {sample_text.capitalize()}")

# 3. Search and validation:
url = "https://api.openai.com/v1/chat/completions"
print(f"\nURL Inspection for '{url}':")
print(f"  .startswith('https://'): {url.startswith('https://')}")
print(f"  .endswith('.com'):       {url.endswith('.com')}")
print(f"  .find('chat'):           {url.find('chat')} (index)")
print(f"  .find('missing'):        {url.find('missing')} (-1 if absent)")
print(f"  'api' in url:            {'api' in url}")

# 4. Replacement:
updated_url = url.replace("chat/completions", "embeddings")
print(f"  .replace():              {updated_url}")


# -----------------------------------------------------------------------------
# Section 7: Splitting and Joining Text Streams
# -----------------------------------------------------------------------------
# .split(delimiter) splits a string into a list of strings.
# 'delimiter'.join(iterable) combines an iterable of strings into one string.

print("\n--- [Section 7: Splitting & Joining] ---")

csv_data = "Ada,Lovelace,1815,Mathematician,London"
tokens = csv_data.split(",")
print(f"CSV line split on comma: {tokens}")

# Recombining with a custom separator:
reconstructed = " | ".join(tokens)
print(f"Rejoined with pipes:     {reconstructed}")

# Splitting on arbitrary whitespace (default .split()):
free_text = "The   quick   brown    fox\n\tjumps"
words = free_text.split()  # No arguments collapses consecutive whitespace!
print(f"Split on whitespace:     {words}")

# Safe joining vs. repeated += concatenation:
# In loops with many strings, "".join(list) is O(N), whereas s += chunk is O(N^2).
parts = [f"item_{i}" for i in range(5)]
joined_result = ", ".join(parts)
print(f"Joined items:            {joined_result}")


# -----------------------------------------------------------------------------
# Section 8: Real-World Scenario — AI Agent Prompting & Markdown Extraction
# -----------------------------------------------------------------------------
# Autonomous Agent Text Processing: building prompts and parsing markdown code.

print("\n--- [Section 8: AI Agent Prompt & Code Extraction] ---")

def build_agent_prompt(role: str, user_query: str, tools: list) -> str:
    """Constructs a structured system prompt with dynamic tool documentation."""
    tool_list_str = "\n".join([f"  - {t}" for t in tools])
    prompt = f"""You are an autonomous agent specialized as: {role}
Available Tools:
{tool_list_str}

User Query:
{user_query.strip()}

Instructions:
Respond with your thought process and an executable Python code block.
"""
    return prompt

def extract_python_code(llm_completion: str) -> str:
    """Extracts clean python code from markdown backticks."""
    start_tag = "```python"
    end_tag = "```"

    start_pos = llm_completion.find(start_tag)
    if start_pos == -1:
        # Fallback to generic ```
        start_tag = "```"
        start_pos = llm_completion.find(start_tag)
        if start_pos == -1:
            return llm_completion.strip()

    code_start = start_pos + len(start_tag)
    end_pos = llm_completion.find(end_tag, code_start)
    if end_pos == -1:
        # Unclosed code fence, return everything after start
        return llm_completion[code_start:].strip()

    return llm_completion[code_start:end_pos].strip()

# Test the prompt builder:
system_prompt = build_agent_prompt(
    role="Data Science Specialist",
    user_query="Compute the mean and variance of daily server latency.",
    tools=["database_query", "python_repl", "report_generator"]
)
print("Constructed Agent System Prompt:")
print(system_prompt)

# Test the markdown extractor:
simulated_llm_response = """
Certainly! Here is the calculation script:
```python
data = [12.4, 15.8, 11.2, 14.1]
mean_val = sum(data) / len(data)
variance = sum((x - mean_val) ** 2 for x in data) / len(data)
print(f"Mean: {mean_val:.2f}, Variance: {variance:.4f}")
```
You can execute this directly in your environment.
"""

clean_code = extract_python_code(simulated_llm_response)
print("Extracted Python Code Body:")
print(clean_code)

print("\n" + "=" * 75)
print("LESSON COMPLETE: Python Strings & Text Processing demonstrated.")
print("=" * 75)
