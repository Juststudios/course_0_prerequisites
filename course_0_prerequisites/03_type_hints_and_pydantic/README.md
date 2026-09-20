# Module 03: Type Hints, Generics, and Pydantic Runtime Validation

## 1. Learning Objectives
By the end of this module, you will be able to:
- Apply Python's static typing system (`typing.Optional`, `Union`, `Annotated`, `Generic[T]`, `Literal`) to define unambiguous contracts for agent payloads.
- Define Pydantic v2 `BaseModel` classes equipped with field-level constraints, custom validators, and serialization configs.
- Automatically generate standard JSON Schemas via `model_json_schema()` to feed directly into LLM function-calling APIs (OpenAI, Anthropic, Gemini).
- Intercept and parse Pydantic `ValidationError` exceptions at runtime to construct automated self-correction feedback prompts for the LLM.
- Structure strongly typed agent message envelopes, tool calls, and execution responses.

---

## 2. Why AI Agent Engineers Need This
Large Language Models generate unstructured or semi-structured string outputs. However, backend tools, databases, and APIs require strictly typed, validated data (e.g. valid emails, integers within bounds, non-empty URLs).

Without runtime validation:
1. A tool expecting an integer received `"five"` or `None`, causing unhandled exceptions that crash the agent loop.
2. Silent type coercion leads to subtle bugs (e.g. `"10" + "20"` evaluating to `"1020"` instead of `30`).
3. Manually maintaining JSON schemas for OpenAI or Anthropic tool manifests results in schema drift where the model is told one thing, but the code expects another.

Pydantic bridges untrusted LLM strings and trusted Python code, providing automatic coercion, schema extraction, and human/LLM-readable validation errors.

---

## 3. Structured Concept Breakdown

### Concept 1: Type Hints & Generics
- **TERM**: Type Hints & Generics
- **DEFINITION**: Annotations attached to function parameters, return values, and class attributes that specify expected data types, optionally parameterized over generic type variables (`T`).
- **INTUITION**: Labeled shipping containers. Instead of an unlabelled box that might contain explosives, food, or electronics, each container has a stamped code indicating exactly what fits inside.
- **WHY IT EXISTS**: Python is dynamically typed. As agent codebases grow with complex state graphs, developers and IDEs lose track of what attributes exist on a message or tool output. Generics (e.g. `AgentResponse[T]`) allow reusable envelopes that preserve the specific type of the payload.
- **HOW IT WORKS**: Type hints are stored in the `__annotations__` dictionary of functions and classes. At runtime, standard Python ignores them; however, static checkers (mypy) and runtime libraries (Pydantic) inspect `__annotations__` to enforce contracts.
- **CODE**:
```python
from typing import TypeVar, Generic, Optional, List

T = TypeVar("T")

class ToolExecutionResult(Generic[T]):
    def __init__(self, tool_name: str, success: bool, data: Optional[T] = None, error: Optional[str] = None):
        self.tool_name = tool_name
        self.success = success
        self.data = data
        self.error = error

# Fully type-checked payload
result: ToolExecutionResult[List[str]] = ToolExecutionResult("search", True, data=["doc1.txt", "doc2.txt"])
```

---

### Concept 2: Pydantic BaseModel
- **TERM**: Pydantic BaseModel
- **DEFINITION**: The foundational class in Pydantic used to construct strongly typed data validation containers that parse, validate, and coerce raw inputs upon instantiation.
- **INTUITION**: A strict border customs checkpoint. Raw inputs (untrusted strings, dictionaries from an LLM) must pass through inspection. Valid items are stamped and converted to native Python types; invalid items are turned away with an itemized citation.
- **WHY IT EXISTS**: In agents, parsing JSON strings from an LLM into raw Python dictionaries (`data = json.loads(...)`) leaves you vulnerable to missing keys (`KeyError`) or wrong types (`TypeError`). `BaseModel` guarantees that if an instance exists, every field is guaranteed to be present and of the correct type.
- **HOW IT WORKS**: Pydantic compiles a fast Rust-based validation graph (`pydantic-core`) based on the class annotations. When `MyModel(**data)` is called, it recursively coerces values (e.g., converting `"42"` to `42` for an `int` field) and validates constraints.
- **CODE**:
```python
from pydantic import BaseModel, Field

class SearchArguments(BaseModel):
    query: str = Field(..., min_length=2, description="The search query terms.")
    limit: int = Field(default=5, ge=1, le=50, description="Max number of results.")
    include_metadata: bool = Field(default=True, description="Whether to include timestamps.")

# Passing dictionary from LLM
args = SearchArguments(**{"query": "neural networks", "limit": "10"})
assert args.limit == 10  # Automatically coerced from string "10" to int 10!
```

---

### Concept 3: Field Constraints & Metadata
- **TERM**: Field Constraints
- **DEFINITION**: Declarative rules declared via `Field()` specifying numerical limits (`ge`, `le`, `gt`, `lt`), string constraints (`min_length`, `max_length`, `pattern`), and descriptions.
- **INTUITION**: Speed limits and lane boundaries on a highway. They prevent drivers (LLMs) from drifting off the road into dangerous territories (e.g. requesting 10,000,000 search results or empty query strings).
- **WHY IT EXISTS**: LLMs frequently hallucinate boundary-violating parameters (e.g. `page: -1` or `temperature: 99.0`). Catching these declaratively at the schema boundary prevents crashes in downstream tools.
- **HOW IT WORKS**: During validation, Pydantic tests each field value against the declared validator rules before assigning it to the instance. Any violation raises a `ValidationError` containing the exact offending field path and error message.
- **CODE**:
```python
from pydantic import BaseModel, Field

class WeatherQuery(BaseModel):
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    days_forecast: int = Field(default=1, ge=1, le=7, description="Number of days to forecast (1 to 7)")
```

---

### Concept 4: JSON Schema Generation
- **TERM**: JSON Schema Generation
- **DEFINITION**: The automatic export of a Pydantic model's type structure, field descriptions, defaults, and constraints into a standardized JSON Schema dictionary via `model_json_schema()`.
- **INTUITION**: An auto-generated user manual. You write the machine's blueprint once (Python class), and the factory automatically prints a clear multilingual spec sheet (JSON Schema) for external operators.
- **WHY IT EXISTS**: Model providers require tool manifests formatted as JSON Schema Draft-07. Writing JSON Schemas by hand is tedious and guarantees syntax errors. Generating them from Pydantic keeps your Python code as the single source of truth.
- **HOW IT WORKS**: Pydantic inspects the model's fields, types, and `Field(description=...)` metadata, compiling a standard JSON Schema object with `"type": "object"`, `"properties": {...}`, and `"required": [...]`.
- **CODE**:
```python
schema = WeatherQuery.model_json_schema()
# Contains:
# {
#   "type": "object",
#   "title": "WeatherQuery",
#   "properties": {
#     "city": {"type": "string", "description": "City name", "minLength": 1, ...},
#     "days_forecast": {"type": "integer", "default": 1, "minimum": 1, "maximum": 7, ...}
#   },
#   "required": ["city"]
# }
```

---

### Concept 5: Runtime Validation & Error Recovery
- **TERM**: Runtime Validation & Self-Correction
- **DEFINITION**: Catching `pydantic.ValidationError` when parsing LLM outputs and formatting the structured error details into an informative feedback prompt sent back to the LLM for self-correction.
- **INTUITION**: A compiler error message. Instead of crashing the computer, the compiler tells the programmer: *"Line 4: Expected integer for 'limit', got string 'infinity'"*. The programmer reads the error and fixes the code.
- **WHY IT EXISTS**: Autonomous agents should not crash on a single bad tool call. Modern LLMs are adept at self-correction if given the exact validation error message.
- **HOW IT WORKS**: When `ValidationError` is caught, `err.errors()` returns a list of dictionaries with keys `loc` (field location), `msg` (failure reason), and `type` (error type). The agent formats these into a message: `"Tool argument validation failed: [error details]. Please correct the arguments and retry."`
- **CODE**:
```python
from pydantic import ValidationError

try:
    WeatherQuery(city="", days_forecast=20)
except ValidationError as e:
    feedback = []
    for err in e.errors():
        loc = " -> ".join(str(p) for p in err["loc"])
        feedback.append(f"- Field '{loc}': {err['msg']}")
    correction_prompt = "Validation error:\n" + "\n".join(feedback)
    print(correction_prompt)
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Silently Discarding Validation Errors
- **The Bug**: Wrapping tool parsing in `try: ... except Exception: return None`.
- **The Consequence**: The agent receives no feedback, enters an infinite loop repeating the same invalid tool call until the step limit or token budget is exhausted.
- **The Fix**: Catch `ValidationError` explicitly and return the detailed validation error string to the model as a `ToolResult` observation so it can self-correct.

### Anti-Pattern 2: Unconstrained String Fields
- **The Bug**: Defining tool parameters as bare `query: str` without `min_length=1` or descriptions.
- **The Consequence**: The LLM passes empty strings `""` or whitespace, causing internal database query errors or empty search responses that degrade agent decision quality.
- **The Fix**: Always use `Field(..., min_length=1, description="...")`.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What method on a Pydantic v2 `BaseModel` produces its JSON schema dictionary?
2. How do you specify that a field is required in Pydantic?
3. What exception does Pydantic raise when input data violates field constraints?

### Tier 2 (Debugging)
Find and correct the bug in this tool schema:
```python
from pydantic import BaseModel, Field

class RunSQLArgs(BaseModel):
    query: str
    timeout_seconds: int = Field(description="Query timeout", le=30)
```
*Hint*: Can `timeout_seconds` be `-5`? Add a lower bound constraint (`ge=1`).

### Tier 3 (Application)
Write a Pydantic model `AgentMessageEnvelope` that has:
- `role`: Literal string restricted to `"system"`, `"user"`, `"assistant"`, `"tool"`.
- `content`: Non-empty string.
- `metadata`: Optional dictionary with string keys and arbitrary values.
- `timestamp`: Float defaulting to the current Unix timestamp via `default_factory`.

### Tier 4 (Challenge)
Build a `SelfCorrectingToolParser` class that accepts a Pydantic model and a raw JSON string from an LLM. If parsing fails, it generates a formatted corrective prompt. Write a simulated loop showing an invalid input being corrected on turn 2.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/03_type_hints_and_pydantic/pydantic_schemas.py
python3 course_0_prerequisites/03_type_hints_and_pydantic/runtime_validation.py
```
