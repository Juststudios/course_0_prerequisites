"""
Module 02: First Python Programs
=================================
A comprehensive exploration of running Python code, standard output, the mechanics
of the built-in print() function, argument separators, line terminators, escape
sequences, and simulating real-time streaming agent outputs.

Run this script directly:
    python3 hello.py
"""

import sys
import time

print("=" * 70)
print("MODULE 02: FIRST PYTHON PROGRAMS — STDOUT, PRINT & FORMATTING")
print("=" * 70)

# -----------------------------------------------------------------------------
# Section 1: The Canonical "Hello, World!"
# -----------------------------------------------------------------------------
# In 1978, Brian Kernighan and Dennis Ritchie introduced the "Hello, World!" program
# in 'The C Programming Language'. It serves a critical engineering purpose:
# It verifies that your editor, file system, interpreter, and output streams
# are correctly configured and communicating.

print("\n--- [Section 1: The Canonical Hello World] ---")
print("Hello, World!")
print("Welcome to Course -1: Python Foundations for AI Engineers!")


# -----------------------------------------------------------------------------
# Section 2: Multiple Arguments and Automatic String Conversion
# -----------------------------------------------------------------------------
# The print() function accepts any number of positional arguments (*objects).
# Python automatically converts each object into a string using its __str__() method.
# By default, Python separates multiple arguments with a single space character (" ").

print("\n--- [Section 2: Multiple Arguments] ---")
agent_name = "Perseus"
model_parameter_count_billions = 70
context_window_k = 128
is_active = True

# Notice that we mix strings, integers, and booleans without manual type casting!
print("Agent:", agent_name, "| Parameters:", model_parameter_count_billions, "B | Context:", context_window_k, "k | Active:", is_active)


# -----------------------------------------------------------------------------
# Section 3: The 'sep' (Separator) Keyword Argument
# -----------------------------------------------------------------------------
# The 'sep' parameter determines what string is placed between each argument.
# Default: sep=" "
# Custom separators allow you to format paths, dates, arrows, or CSV rows cleanly.

print("\n--- [Section 3: Custom Separators with 'sep'] ---")

# Example A: Formatting a simulated path
print("home", "user", "workspace", "agent_project", sep="/")

# Example B: Formatting dates
year = 2026
month = 9
day = 21
print(year, f"{month:02d}", f"{day:02d}", sep="-")

# Example C: Visual state transition pipeline
print("Received Query", "Parsed Intent", "Invoked Tool", "Synthesized Answer", sep=" ===> ")

# Example D: Empty separator (sep="") for glued concatenation
print("Agent", "007", "Status", "READY", sep="")


# -----------------------------------------------------------------------------
# Section 4: The 'end' Keyword Argument
# -----------------------------------------------------------------------------
# The 'end' parameter specifies what character(s) are printed AFTER all arguments.
# Default: end="\n" (newline)
# By overriding 'end', you can keep subsequent print() calls on the same line.

print("\n--- [Section 4: Custom Line Terminators with 'end'] ---")

# Example A: Standard print vs custom end
print("Loading core models...", end=" ")
print("Initialized!")  # Appears on the same line!

# Example B: Printing items in a loop horizontally
print("Processing task batch: [", end="")
for step in range(1, 6):
    end_char = ", " if step < 5 else "]\n"
    print(f"Task-{step}", end=end_char)

# Example C: Custom punctuation terminators
print("Operation successful", end=" *** ALL SYSTEMS GO ***\n")


# -----------------------------------------------------------------------------
# Section 5: Escape Sequences and Special Characters
# -----------------------------------------------------------------------------
# When you need to include characters that have special syntactic meanings
# (like quotes, newlines, or tabs) inside a string literal, use a backslash (\).
# Key escape sequences:
#   \n : Line feed (newline)
#   \t : Horizontal tab (indentation)
#   \\ : Literal backslash
#   \' : Single quote inside single-quoted string
#   \" : Double quote inside double-quoted string

print("\n--- [Section 5: Escape Sequences] ---")

# Newline and tab combinations
print("AGENT DIAGNOSTIC REPORT:\n\tStatus:\tHEALTHY\n\tUptime:\t99.98%\n\tLatency:\t14ms")

# Escaping quotation marks
print("The lead researcher stated: \"Autonomous systems require deterministic toolchains.\"")

# Escaping backslashes (e.g. Windows paths or regex patterns)
print("File system reference: C:\\Users\\Administrator\\AppData\\Local\\Temp")

# Raw strings (prefixed with r) ignore escape sequences entirely:
raw_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
print("Compiled Regex Raw Pattern:", raw_pattern)


# -----------------------------------------------------------------------------
# Section 6: Comparing print() to Low-Level sys.stdout.write()
# -----------------------------------------------------------------------------
# Under the hood, print() is a high-level wrapper around sys.stdout.write().
# sys.stdout.write() does NOT add a trailing newline automatically.
# sys.stdout.write() requires pure string arguments (no auto-conversion).

print("\n--- [Section 6: Low-Level sys.stdout.write] ---")
sys.stdout.write("Direct write to stdout 1... ")
sys.stdout.write("Direct write to stdout 2... ")
sys.stdout.write("Finished with manual newline.\n")


# -----------------------------------------------------------------------------
# Section 7: Simulating Real-Time LLM Token Streaming
# -----------------------------------------------------------------------------
# Modern AI chatbots don't wait for an entire paragraph to finish generating.
# They emit tokens one-by-one. In Python, terminal buffers often hold output
# until a newline is sent. Passing flush=True forces the operating system
# to display every single token immediately.

print("\n--- [Section 7: Token Streaming Simulation with flush=True] ---")
simulated_llm_response = [
    "I", " have", " analyzed", " your", " codebase", " and", " verified",
    " that", " all", " 33", " modules", " are", " progressing", " smoothly."
]

print("Simulating streaming response from Agent: ", end="", flush=True)
for token in simulated_llm_response:
    print(token, end="", flush=True)
    # Tiny sleep to emulate inference generation latency
    time.sleep(0.02)
print("\n[Stream Complete]")


# -----------------------------------------------------------------------------
# Section 8: Building a Clean Terminal Dashboard
# -----------------------------------------------------------------------------
# Combining everything we learned to render a formatted CLI report.

print("\n--- [Section 8: Professional Terminal Status Dashboard] ---")

def render_dashboard(agent_id, task_count, error_rate, mode):
    border = "+" + "-" * 48 + "+"
    print(border)
    print(f"| AGENT TELEMETRY MONITOR: {agent_id:<21} |")
    print("+" + "=" * 48 + "+")
    print(f"| Mode        : {mode:<32} |")
    print(f"| Tasks Run   : {task_count:<32} |")
    print(f"| Error Rate  : {f'{error_rate:.2%}' :<32} |")
    print(f"| Heartbeat   : {'ACTIVE (OK)':<32} |")
    print(border)

render_dashboard("Orchestrator-01", 1420, 0.0014, "PRODUCTION")


# -----------------------------------------------------------------------------
# Section 9: Script Exit and Clean Return Codes
# -----------------------------------------------------------------------------
# When a Python script terminates normally, it exits with return code 0.
# A return code of 0 indicates success to the operating system and calling processes.
# sys.exit(0) can be used to explicitly exit at any point.

print("\n--- [Section 9: Clean Process Termination] ---")
print("Process execution completed successfully. Returning exit code 0 to OS.")

print("\n" + "=" * 70)
print("MODULE 02 COMPLETE: HELLO WORLD & OUTPUT MASTERED")
print("=" * 70)
