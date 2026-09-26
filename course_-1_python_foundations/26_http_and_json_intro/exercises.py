"""
Module 26 Exercises: HTTP and JSON Introduction
===============================================

Practice working with JSON serialization, deserialization, custom encoders,
and HTTP communication patterns used by autonomous AI agents.

Follow the instructions for each level. Replace `raise NotImplementedError`
with your solution.
"""

import datetime
import json
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Level 1: Recall
# ============================================================================

def serialize_and_deserialize_agent_state(state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Recall how to serialize a Python dictionary to a JSON string and parse it back.

    Requirements:
    1. Serialize `state` to a formatted JSON string with `indent=2`.
    2. Deserialize the resulting JSON string back into a Python dictionary.
    3. Return a tuple `(json_string, deserialized_dict)`.
    """
    # TODO: Serialize to JSON string with indent=2 and deserialize back.
    raise NotImplementedError("Level 1: Implement serialize_and_deserialize_agent_state")


# ============================================================================
# Level 2: Modify
# ============================================================================

def custom_agent_json_serializer(data: Dict[str, Any]) -> str:
    """
    Modify JSON serialization to support non-standard Python types.

    Requirements:
    1. Define or use a custom JSON encoder that handles:
       - `datetime.datetime` or `datetime.date` -> ISO format string (`obj.isoformat()`).
       - `set` or `frozenset` -> sorted list of its elements (`sorted(list(obj))`).
    2. Serialize `data` to a JSON string using this custom encoder.
    3. Return the resulting JSON string.
    """
    # TODO: Implement custom JSON encoder for datetime and set types.
    raise NotImplementedError("Level 2: Implement custom_agent_json_serializer")


# ============================================================================
# Level 3: Build
# ============================================================================

def parse_and_validate_tool_call(raw_json: str, required_fields: List[str]) -> Dict[str, Any]:
    """
    Build a robust tool call parser and validator for AI agent runtime systems.

    Requirements:
    1. Parse `raw_json` using `json.loads()`. If `json.JSONDecodeError` is raised,
       catch it and raise a `ValueError("Malformed tool call JSON")`.
    2. Verify that the parsed object is a Python `dict`. If it is not a dictionary
       (e.g., a list or a primitive), raise `TypeError("Tool call payload must be a JSON object")`.
    3. Check that every field name in `required_fields` exists as a key in the parsed dictionary.
       If any field is missing, raise `KeyError(f"Missing required field: {missing_field}")`.
    4. Return the validated dictionary.
    """
    # TODO: Build safe JSON parsing and validation pipeline.
    raise NotImplementedError("Level 3: Implement parse_and_validate_tool_call")


# ============================================================================
# Level 4: Debug
# ============================================================================

def build_http_request_url(
    base_url: str,
    path: str,
    query_params: Optional[Dict[str, Any]] = None,
) -> str:
    """
    DEBUG CHALLENGE:
    The following function is supposed to assemble a clean, encoded HTTP URL from
    a base URL, a path segment, and optional query parameters.

    However, the buggy code has multiple defects:
    1. It blindly concatenates `base_url + "/" + path`, causing double slashes
       like `http://api.example.com//v1/status` if base_url ends with `/` or path starts with `/`.
    2. It forgets to format query parameters with `urllib.parse.urlencode` and fails
       to prefix them with `?`.
    3. When query_params is None or empty, it still leaves a trailing `?`.

    Fix the implementation so it correctly formats and encodes the full URL.
    """
    # BUGGY CODE:
    # url = base_url + "/" + path
    # if query_params:
    #     url += "?" + str(query_params)  # BUG: Produces '?{\'key\': \'val\'}', not URL query string!
    # else:
    #     url += "?"  # BUG: Unnecessary trailing question mark!
    # return url

    # TODO: Fix URL construction and parameter encoding.
    raise NotImplementedError("Level 4: Debug build_http_request_url")
