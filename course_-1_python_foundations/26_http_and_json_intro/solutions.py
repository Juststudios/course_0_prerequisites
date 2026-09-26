"""
Module 26 Solutions: HTTP and JSON Introduction
===============================================

Reference implementations for all 4 exercise levels.
"""

import datetime
import json
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Level 1: Recall Solution
# ============================================================================

def serialize_and_deserialize_agent_state(state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Serializes a dictionary to formatted JSON and parses it back."""
    json_str = json.dumps(state, indent=2)
    deserialized = json.loads(json_str)
    return json_str, deserialized


# ============================================================================
# Level 2: Modify Solution
# ============================================================================

class _FlexibleJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder handling datetime, date, set, and frozenset."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, (set, frozenset)):
            return sorted(list(obj))
        return super().default(obj)


def custom_agent_json_serializer(data: Dict[str, Any]) -> str:
    """Serializes complex Python dictionaries containing datetime and set types."""
    return json.dumps(data, cls=_FlexibleJSONEncoder, indent=2)


# ============================================================================
# Level 3: Build Solution
# ============================================================================

def parse_and_validate_tool_call(raw_json: str, required_fields: List[str]) -> Dict[str, Any]:
    """Safely parses and validates incoming JSON tool calls from an LLM."""
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed tool call JSON") from exc

    if not isinstance(parsed, dict):
        raise TypeError("Tool call payload must be a JSON object")

    for field in required_fields:
        if field not in parsed:
            raise KeyError(f"Missing required field: {field}")

    return parsed


# ============================================================================
# Level 4: Debug Solution
# ============================================================================

def build_http_request_url(
    base_url: str,
    path: str,
    query_params: Optional[Dict[str, Any]] = None,
) -> str:
    """Constructs a clean, normalized HTTP URL with properly encoded query parameters."""
    # Strip trailing slash from base and leading slash from path to prevent double slash
    clean_base = base_url.rstrip("/")
    clean_path = path.lstrip("/")
    url = f"{clean_base}/{clean_path}" if clean_path else clean_base

    if query_params:
        # Encode key-value pairs as standard application/x-www-form-urlencoded
        encoded_query = urllib.parse.urlencode(query_params)
        if encoded_query:
            url = f"{url}?{encoded_query}"

    return url


# ============================================================================
# Verification Tests
# ============================================================================

def run_tests() -> None:
    print("Running Module 26 Verification Tests...")

    # Level 1 test
    sample_state = {"agent": "Tester", "level": 1, "active": True}
    json_txt, restored = serialize_and_deserialize_agent_state(sample_state)
    assert restored == sample_state, f"Level 1 failed: {restored}"
    assert "\n" in json_txt, "Level 1 failed: JSON string was not indented"
    print("  [✓] Level 1 (Recall: serialize & deserialize) passed.")

    # Level 2 test
    now = datetime.datetime(2026, 9, 21, 12, 0, 0)
    complex_data = {
        "timestamp": now,
        "tags": {"beta", "ai", "crawler"},
        "id": 101,
    }
    encoded_json = custom_agent_json_serializer(complex_data)
    decoded_again = json.loads(encoded_json)
    assert decoded_again["timestamp"] == "2026-09-21T12:00:00"
    assert decoded_again["tags"] == ["ai", "beta", "crawler"]
    print("  [✓] Level 2 (Modify: Custom JSONEncoder) passed.")

    # Level 3 test
    valid_payload = '{"tool_name": "calc", "arguments": {"x": 2}, "call_id": "c1"}'
    res = parse_and_validate_tool_call(valid_payload, ["tool_name", "arguments"])
    assert res["tool_name"] == "calc"

    # Test malformed JSON
    try:
        parse_and_validate_tool_call("{bad json}", ["tool_name"])
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass

    # Test non-dict JSON
    try:
        parse_and_validate_tool_call("[\"item1\", \"item2\"]", ["tool_name"])
        raise AssertionError("Should have raised TypeError")
    except TypeError:
        pass

    # Test missing field
    try:
        parse_and_validate_tool_call('{"arguments": {}}', ["tool_name"])
        raise AssertionError("Should have raised KeyError")
    except KeyError:
        pass

    print("  [✓] Level 3 (Build: parse & validate tool call) passed.")

    # Level 4 test
    url1 = build_http_request_url("https://api.openai.com/v1/", "/chat/completions")
    assert url1 == "https://api.openai.com/v1/chat/completions", f"Failed: {url1}"

    url2 = build_http_request_url(
        "https://api.search.com",
        "search",
        {"q": "agent frameworks", "page": 1}
    )
    assert url2 == "https://api.search.com/search?q=agent+frameworks&page=1", f"Failed: {url2}"

    url3 = build_http_request_url("https://example.com/api", "ping", None)
    assert url3 == "https://example.com/api/ping", f"Failed: {url3}"

    print("  [✓] Level 4 (Debug: URL builder) passed.")

    print("All Module 26 exercise solutions verified successfully!\n")


def main() -> None:
    run_tests()


if __name__ == "__main__":
    main()
