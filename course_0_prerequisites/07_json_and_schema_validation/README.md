# Module 07: JSON Parsing, Schema Validation, and Heuristic Repair

## 1. Learning Objectives
By the end of this module, you will be able to:
- Perform robust JSON serialization and deserialization using Python's standard `json` library and custom encoders.
- Reliably strip surrounding markdown formatting (such as ```` ```json ... ``` ````) emitted by LLMs.
- Implement heuristic repair algorithms to heal common LLM syntax errors: unescaped quotes, trailing commas, single quotes instead of double quotes, and missing closing brackets/braces due to token truncation.
- Validate parsed JSON objects against structural schemas before invoking downstream tools.
- Design an automated JSON sanitization pipeline for autonomous agent runtimes.

---

## 2. Why AI Agent Engineers Need This
JSON is the lingua franca of agent tool calling and structured output protocols. Every major model provider outputs tool arguments and decision payloads formatted as JSON.

However, LLMs do not write to a socket byte-by-byte with syntax verification; they sample token-by-token probabilistically. Consequently, LLM-generated JSON frequently breaks:
1. **Markdown Wrapping**: Models wrap JSON inside ```` ```json\n{...}\n``` ```` blocks with conversational preamble ("Here is the requested tool call: ...").
2. **Trailing Commas**: Models often append a comma after the final key-value pair (`{"a": 1,}`).
3. **Token Truncation**: A response hitting max-token limits cuts off mid-string (`{"items": ["apple", "ban`), leaving unclosed brackets.
4. **Python Dict Confusion**: Models output single-quoted strings or Python literals (`{'valid': True, 'null_val': None}`).

An agent runtime that simply calls `json.loads(response)` will crash constantly. A production agent requires a robust JSON extraction and heuristic repair pipeline.

---

## 3. Structured Concept Breakdown

### Concept 1: JSON Serialization & Custom Encoders
- **TERM**: JSON Serialization & Custom Encoders
- **DEFINITION**: Converting in-memory Python data structures into standard JSON text formatted strings, utilizing `json.JSONEncoder` or a `default` handler for non-primitive types (dates, UUIDs, dataclasses).
- **INTUITION**: Packing household items into standardized moving boxes. Standard items (books, clothes) fit easily; non-standard items (a bicycle) need a specialized disassembly routine before fitting into a standard box.
- **WHY IT EXISTS**: Agents pass rich objects (e.g. `datetime`, `UUID`, Pydantic models, numpy arrays) between components. `json.dumps()` raises `TypeError: Object of type X is not JSON serializable` unless an encoder tells it how to convert them into strings or numbers.
- **HOW IT WORKS**: `json.dumps(obj, default=serializer_func)` calls `serializer_func(item)` whenever it encounters an object type not natively recognized (i.e. not `dict`, `list`, `str`, `int`, `float`, `bool`, `None`).
- **CODE**:
```python
import json
from datetime import datetime
import uuid

def custom_json_serializer(obj):
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

payload = {"id": uuid.uuid4(), "created_at": datetime.now(), "tokens": 42}
serialized = json.dumps(payload, default=custom_json_serializer)
```

---

### Concept 2: Code Fence Stripping
- **TERM**: Markdown Code Fence Stripping
- **DEFINITION**: Extracting raw JSON text from an LLM completion that includes markdown backtick delimiters and conversational chatter.
- **INTUITION**: Unboxing a package. You tear off the external cardboard shipping box and bubble wrap before using the electronic device inside.
- **WHY IT EXISTS**: Prompting an LLM to "respond ONLY in JSON" often fails—models still output conversational niceties ("Sure! Here is the JSON:") followed by ```` ```json ... ``` ````. Stripping fences extracts the inner payload safely.
- **HOW IT WORKS**: Regular expressions or string partition logic locate the first occurrence of ```` ```json ```` or ```` ``` ```` and extract everything up to the matching closing ```` ``` ````. If no fences exist, regex locates the outermost matching `{ ... }` or `[ ... ]`.
- **CODE**:
```python
import re

def strip_markdown_fences(text: str) -> str:
    text = text.strip()
    # Match ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # If no fences, find the first '{' and last '}'
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        return text[first_brace:last_brace + 1].strip()
    return text
```

---

### Concept 3: Heuristic Repair of Malformed JSON
- **TERM**: Heuristic JSON Repair
- **DEFINITION**: Algorithmic rules applied to malformed JSON text to rectify common LLM syntax deviations prior to deserialization.
- **INTUITION**: Autocorrect on a smartphone. When a user types a minor typo, the system seamlessly corrects it without stopping the conversation.
- **WHY IT EXISTS**: A trailing comma or single quote shouldn't require a 3-second round trip LLM re-generation. Fixing it in Python takes under 0.5 milliseconds.
- **HOW IT WORKS**:
  1. Replace single quotes `'` with double quotes `"` (taking care of apostrophes).
  2. Strip trailing commas before closing braces/brackets (`,\s*}` $\rightarrow$ `}`).
  3. Replace Python constants (`True`, `False`, `None`) with JSON equivalents (`true`, `false`, `null`).
  4. Balance unclosed brackets/braces by counting open vs closed symbols.
- **CODE**:
```python
import re

def repair_json_syntax(text: str) -> str:
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([\]}])", r"\1", text)
    # Fix Python boolean/None literals if present
    text = re.sub(r"\bTrue\b", "true", text)
    text = re.sub(r"\bFalse\b", "false", text)
    text = re.sub(r"\bNone\b", "null", text)
    return text
```

---

### Concept 4: Bracket Balancing for Truncated JSON
- **TERM**: Bracket Balancing
- **DEFINITION**: Appending missing closing braces (`}`) and brackets (`]`) to repair truncated JSON streams caused by max token cutoffs.
- **INTUITION**: Completing an interrupted sentence with a closing period so the statement parses as valid grammar.
- **WHY IT EXISTS**: If an LLM reaches its `max_tokens` limit, the tail of the JSON structure is omitted. Without bracket balancing, the entire completion is unparseable and lost.
- **HOW IT WORKS**: A stack-based scanner tracks open `{` and `[` characters outside of string quotes. When reaching the end of the text, it appends the matching closing characters in reverse stack order.
- **CODE**:
```python
def balance_brackets(text: str) -> str:
    stack = []
    in_string = False
    escape = False

    for char in text:
        if char == '"' and not escape:
            in_string = not in_string
        elif not in_string:
            if char in "{[":
                stack.append("}" if char == "{" else "]")
            elif char in "}]":
                if stack and stack[-1] == char:
                    stack.pop()
        escape = (char == "\\" and not escape)

    # Close any open strings first
    if in_string:
        text += '"'
    # Append missing closing brackets in reverse order
    while stack:
        text += stack.pop()
    return text
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Blind `eval()` on Single-Quoted JSON
- **The Bug**: Using `eval(llm_output)` or `ast.literal_eval(llm_output)` to parse single-quoted JSON.
- **The Consequence**: `eval()` introduces critical security holes (arbitrary remote code execution). `ast.literal_eval()` fails on valid JSON literals like `true` or `null`.
- **The Fix**: Sanitize strings into valid JSON format and parse with `json.loads()`.

### Anti-Pattern 2: Discarding the Entire Completion on JSON Error
- **The Bug**: Raising an unhandled `JSONDecodeError` and terminating the agent run when a minor trailing comma exists.
- **The Consequence**: High agent task failure rates and wasted inference tokens/costs.
- **The Fix**: Run the output through a heuristic repair pipeline before failing; if repair fails, request LLM self-correction.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What exception is raised by Python's `json.loads()` when given invalid JSON syntax?
2. What are the JSON equivalents of Python's `True`, `False`, and `None`?
3. Why does standard `json.loads('{"key": "value",}')` fail?

### Tier 2 (Debugging)
Find the flaw in this naive fence stripper:
```python
def extract_json(response):
    return response.split("```")[1]
```
*Hint*: What happens if the response does not contain any code fences? What if there are multiple code blocks?

### Tier 3 (Application)
Write a function `safe_json_parse(raw_text: str) -> dict` that:
1. Strips markdown fences.
2. Removes trailing commas.
3. Parses with `json.loads()`.
4. If still invalid, returns `None` without raising an exception.

### Tier 4 (Challenge)
Build a `RobustJSONExtractor` class that handles:
- Conversational preamble and postscript.
- Single-quoted keys/values.
- Unclosed strings and truncated object hierarchies.
- Write test assertions covering 6 distinct broken LLM output examples.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/07_json_and_schema_validation/json_validation.py
python3 course_0_prerequisites/07_json_and_schema_validation/repair_malformed_json.py
```
