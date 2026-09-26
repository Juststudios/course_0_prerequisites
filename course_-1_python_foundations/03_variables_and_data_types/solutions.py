"""
Module 03: Variables and Data Types — Reference Solutions
==========================================================
Complete, verified implementations for all four exercise tiers.
"""

from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def classify_primitive_types() -> Dict[str, str]:
    """
    Returns exact type names for the requested expressions.
    """
    return {
        "expr_int": type(42).__name__,
        "expr_float": type(3.14159).__name__,
        "expr_str": type("Agent 007").__name__,
        "expr_bool": type(True).__name__,
        "expr_none": type(None).__name__,
        "expr_truthy_zero": type(bool(0)).__name__,
        "expr_cast_int": type(int("99")).__name__,
    }


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def sanitize_agent_config(raw_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes raw configuration dictionary and coerces fields to typed representations.
    """
    # 1. agent_name
    raw_name = raw_config.get("agent_name")
    if raw_name and isinstance(raw_name, str) and raw_name.strip():
        agent_name = raw_name.strip()
    else:
        agent_name = "DefaultAgent"

    # 2. timeout
    try:
        timeout = int(raw_config.get("timeout", 30))
        if timeout <= 0:
            timeout = 30
    except (ValueError, TypeError):
        timeout = 30

    # 3. temperature
    try:
        temp = float(raw_config.get("temperature", 0.7))
        if temp < 0.0:
            temp = 0.0
        elif temp > 1.0:
            temp = 1.0
    except (ValueError, TypeError):
        temp = 0.7

    # 4. active
    active = bool(raw_config.get("active", False))

    # 5. last_error
    last_error = None

    return {
        "agent_name": agent_name,
        "timeout": timeout,
        "temperature": temp,
        "active": active,
        "last_error": last_error,
    }


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def coerce_and_validate_payload(
    schema: Dict[str, type],
    data: Dict[str, Any]
) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates that all schema fields exist and coerces them into target types.
    """
    coerced: Dict[str, Any] = {}

    for field_name, target_type in schema.items():
        if field_name not in data:
            return (False, {})

        val = data[field_name]

        try:
            if target_type is bool:
                if isinstance(val, str):
                    clean_str = val.strip().lower()
                    if clean_str in {"false", "0", "no", "off"}:
                        coerced[field_name] = False
                    elif clean_str in {"true", "1", "yes", "on"}:
                        coerced[field_name] = True
                    else:
                        coerced[field_name] = bool(val)
                else:
                    coerced[field_name] = bool(val)
            elif target_type is int:
                coerced[field_name] = int(val)
            elif target_type is float:
                coerced[field_name] = float(val)
            elif target_type is str:
                coerced[field_name] = str(val)
            else:
                coerced[field_name] = target_type(val)
        except (ValueError, TypeError):
            return (False, {})

    return (True, coerced)


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def calculate_normalized_metrics(scores: List[Any], baseline: Any) -> Dict[str, float]:
    """
    Safely normalizes scores against a baseline and computes mean, min, max.
    """
    if not scores:
        raise ValueError("Scores list cannot be empty")

    try:
        base = float(baseline)
    except (ValueError, TypeError) as err:
        raise ValueError(f"Invalid baseline value: {baseline}") from err

    if base == 0.0:
        raise ValueError("Baseline cannot be zero")

    norm_scores: List[float] = []
    for s in scores:
        try:
            val = float(s)
        except (ValueError, TypeError) as err:
            raise ValueError(f"Invalid score element: {s}") from err
        norm_scores.append(val / base)

    return {
        "mean": sum(norm_scores) / len(norm_scores),
        "min": min(norm_scores),
        "max": max(norm_scores),
    }


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    types_map = classify_primitive_types()
    assert types_map["expr_int"] == "int"
    assert types_map["expr_float"] == "float"
    assert types_map["expr_str"] == "str"
    assert types_map["expr_bool"] == "bool"
    assert types_map["expr_none"] == "NoneType"
    assert types_map["expr_truthy_zero"] == "bool"
    assert types_map["expr_cast_int"] == "int"

    # Test Level 2
    raw = {
        "agent_name": "  ResearcherBot  ",
        "timeout": "45",
        "temperature": "1.8",  # clamps to 1.0
        "active": 1,
    }
    cleaned = sanitize_agent_config(raw)
    assert cleaned["agent_name"] == "ResearcherBot"
    assert cleaned["timeout"] == 45
    assert cleaned["temperature"] == 1.0
    assert cleaned["active"] is True
    assert cleaned["last_error"] is None

    # Fallback checks
    fallback = sanitize_agent_config({"agent_name": "", "timeout": -5, "temperature": "invalid"})
    assert fallback["agent_name"] == "DefaultAgent"
    assert fallback["timeout"] == 30
    assert fallback["temperature"] == 0.7

    # Test Level 3
    schema = {"id": int, "score": float, "is_valid": bool, "label": str}
    valid_data = {"id": "101", "score": "98.5", "is_valid": "yes", "label": 12345}
    success, res = coerce_and_validate_payload(schema, valid_data)
    assert success is True
    assert res == {"id": 101, "score": 98.5, "is_valid": True, "label": "12345"}

    # Missing field check
    missing_success, _ = coerce_and_validate_payload(schema, {"id": 1})
    assert missing_success is False

    # Invalid casting check
    bad_success, _ = coerce_and_validate_payload(schema, {"id": "abc", "score": 1.0, "is_valid": True, "label": "ok"})
    assert bad_success is False

    # Test Level 4
    metrics = calculate_normalized_metrics(["80", 90.0, 70], "100")
    assert abs(metrics["mean"] - 0.8) < 1e-6
    assert abs(metrics["min"] - 0.7) < 1e-6
    assert abs(metrics["max"] - 0.9) < 1e-6

    # Test zero baseline error handling
    try:
        calculate_normalized_metrics([10, 20], 0)
        assert False, "Should have raised ValueError for zero baseline"
    except ValueError:
        pass

    # Test empty scores error handling
    try:
        calculate_normalized_metrics([], 10)
        assert False, "Should have raised ValueError for empty scores"
    except ValueError:
        pass

    print("Module 03: All Level 1-4 solutions verified successfully!")
