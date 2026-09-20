"""json_validation.py - Demonstrates custom JSON encoders and schema validation for agent payloads.

Key concepts demonstrated:
1. Custom JSONEncoder for serializing complex agent state (datetimes, UUIDs).
2. Catching json.JSONDecodeError with helpful context.
3. Validating JSON dictionary shapes against expected agent action schemas.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
import json
import uuid


class AgentJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder handling datetimes, UUIDs, and custom object reprs."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)


class AgentActionSchema:
    """Lightweight schema validator for agent action envelopes."""

    REQUIRED_FIELDS = {"thought", "action", "action_input"}

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Agent action must be a JSON object, got {type(data).__name__}")

        missing = cls.REQUIRED_FIELDS - set(data.keys())
        if missing:
            raise ValueError(f"Missing required action fields: {sorted(missing)}")

        if not isinstance(data["action"], str) or not data["action"].strip():
            raise ValueError("Field 'action' must be a non-empty string.")

        if not isinstance(data["action_input"], dict):
            raise ValueError("Field 'action_input' must be a JSON dictionary.")


def main() -> None:
    print("=== Module 07: JSON Serialization & Schema Validation Demo ===")

    # 1. Custom JSON serialization
    event = {
        "event_id": uuid.uuid4(),
        "timestamp": datetime.now(timezone.utc),
        "agent": "coder_agent_v1",
        "step_data": {"completed": True, "return_code": 0}
    }

    serialized = json.dumps(event, cls=AgentJSONEncoder, indent=2)
    print("Serialized Agent Event with custom types:")
    print(serialized)

    deserialized = json.loads(serialized)
    assert deserialized["agent"] == "coder_agent_v1"
    assert "event_id" in deserialized
    print("[OK] Custom serialization & deserialization verified.")

    # 2. Validate compliant action payload
    valid_payload = {
        "thought": "I need to search the repo for configuration files.",
        "action": "file_search",
        "action_input": {"pattern": "*.env", "max_results": 5}
    }
    AgentActionSchema.validate(valid_payload)
    print("[OK] Compliant agent action validated successfully.")

    # 3. Catch non-compliant payloads
    invalid_payload = {
        "thought": "Missing action input",
        "action": "bash_command"
        # missing action_input
    }
    try:
        AgentActionSchema.validate(invalid_payload)
        raise AssertionError("Should have raised ValueError")
    except ValueError as err:
        assert "Missing required action fields" in str(err)
        print(f"[OK] Caught expected schema violation: {err}")

    # 4. Handle JSONDecodeError
    malformed_json_str = '{"thought": "broken JSON'
    try:
        json.loads(malformed_json_str)
        raise AssertionError("Should have raised JSONDecodeError")
    except json.JSONDecodeError as err:
        print(f"[OK] Caught standard JSONDecodeError at line {err.lineno}, col {err.colno}")

    print("All tests in json_validation.py completed successfully!\n")


if __name__ == "__main__":
    main()
