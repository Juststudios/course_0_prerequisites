"""pydantic_schemas.py - Demonstrates Pydantic v2 schemas and JSON schema extraction for AI tools.

Key concepts demonstrated:
1. Pydantic BaseModel with strict typing and Field constraints.
2. Generating JSON Schema Draft-07 for LLM tool manifests.
3. Nested Pydantic models for complex tool payloads.
4. Safe serialization and deserialization.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl
import json


class FilterCriteria(BaseModel):
    """Sub-model for structured search filters."""
    category: Literal["documentation", "code", "issue_tracker"] = Field(
        default="documentation",
        description="Target repository category."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Filter tags that must all match."
    )


class SearchToolInput(BaseModel):
    """Schema for an agent search tool."""
    query: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="The semantic search query string."
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=25,
        description="Maximum number of documents to retrieve."
    )
    filter: Optional[FilterCriteria] = Field(
        default=None,
        description="Optional structured filters to narrow results."
    )


class AgentToolCallEnvelope(BaseModel):
    """Encapsulates a tool invocation request emitted by an LLM."""
    call_id: str = Field(..., description="Unique tool call identifier.")
    tool_name: str = Field(..., description="Target tool name to execute.")
    arguments: SearchToolInput = Field(..., description="Validated tool arguments.")


def main() -> None:
    print("=== Module 03: Pydantic Schemas & Tool Generation Demo ===")

    # 1. Inspect generated JSON Schema for tool manifest
    schema = SearchToolInput.model_json_schema()
    print("Generated JSON Schema for SearchToolInput:")
    print(json.dumps(schema, indent=2))

    assert schema["type"] == "object"
    assert "query" in schema["required"]
    assert schema["properties"]["query"]["minLength"] == 2
    assert schema["properties"]["max_results"]["minimum"] == 1
    assert schema["properties"]["max_results"]["maximum"] == 25
    print("[OK] JSON Schema generated correctly with constraints.")

    # 2. Test successful validation and type coercion
    raw_llm_payload = {
        "call_id": "call_98765",
        "tool_name": "search_docs",
        "arguments": {
            "query": "asyncio event loops",
            "max_results": "10",  # String will be coerced to integer
            "filter": {
                "category": "documentation",
                "tags": ["python", "async"]
            }
        }
    }

    envelope = AgentToolCallEnvelope.model_validate(raw_llm_payload)
    assert envelope.call_id == "call_98765"
    assert envelope.arguments.max_results == 10
    assert isinstance(envelope.arguments.max_results, int)
    assert envelope.arguments.filter is not None
    assert envelope.arguments.filter.category == "documentation"
    print(f"[OK] Successfully validated envelope for tool: {envelope.tool_name}")

    # 3. Test serialization back to JSON
    json_repr = envelope.model_dump_json()
    assert '"max_results":10' in json_repr or '"max_results": 10' in json_repr
    print("[OK] model_dump_json() verified.")

    print("All tests in pydantic_schemas.py passed successfully!\n")


if __name__ == "__main__":
    main()
