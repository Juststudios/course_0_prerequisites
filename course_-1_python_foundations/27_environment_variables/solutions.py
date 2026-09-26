"""
Module 27 Solutions: Environment Variables & Configuration Management
======================================================================

Reference implementations for all 4 exercise levels.
"""

import os
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Level 1: Recall Solution
# ============================================================================

def get_strictly_required(key: str) -> str:
    """Accesses a strictly required environment variable or raises descriptive KeyError."""
    if key not in os.environ:
        raise KeyError(f"Missing required environment variable: {key}")
    return os.environ[key]


def get_with_default(key: str, default: str) -> str:
    """Retrieves an environment variable with a default fallback."""
    return os.getenv(key, default)


# ============================================================================
# Level 2: Modify Solution
# ============================================================================

def parse_agent_feature_flags(env_map: Dict[str, str]) -> Dict[str, bool]:
    """Safely converts string pairs into evaluated boolean feature flags."""
    true_literals = {"true", "1", "yes", "on"}
    false_literals = {"false", "0", "no", "off"}
    result: Dict[str, bool] = {}

    for k, v in env_map.items():
        lowered = v.strip().lower()
        if lowered in true_literals:
            result[k] = True
        elif lowered in false_literals:
            result[k] = False
        else:
            result[k] = False

    return result


# ============================================================================
# Level 3: Build Solution
# ============================================================================

def load_dotenv_string(content: str) -> Dict[str, str]:
    """Parses key-value pairs from .env formatted text into a dictionary."""
    records: Dict[str, str] = {}
    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue
        if "=" in trimmed:
            key_part, val_part = trimmed.split("=", 1)
            key = key_part.strip()
            val = val_part.strip()

            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]

            records[key] = val

    return records


# ============================================================================
# Level 4: Debug Solution
# ============================================================================

def load_agent_runtime_port(env_var_name: str = "PORT", default_port: int = 8080) -> int:
    """
    Safely retrieves and validates a network port number, handling missing keys,
    non-numeric strings, and out-of-range port numbers.
    """
    raw_val = os.getenv(env_var_name)
    if raw_val is None:
        return default_port

    try:
        port = int(raw_val.strip())
        if 1 <= port <= 65535:
            return port
        return default_port
    except ValueError:
        return default_port


# ============================================================================
# Verification Tests
# ============================================================================

def run_tests() -> None:
    print("Running Module 27 Verification Tests...")

    # Level 1 test
    os.environ["TEST_M5_KEY"] = "active_value"
    val1 = get_strictly_required("TEST_M5_KEY")
    assert val1 == "active_value"

    try:
        get_strictly_required("MISSING_KEY_12345")
        raise AssertionError("Should have raised KeyError")
    except KeyError as e:
        assert "Missing required environment variable" in str(e)

    val2 = get_with_default("MISSING_KEY_12345", "fallback_val")
    assert val2 == "fallback_val"
    print("  [✓] Level 1 (Recall: required & default) passed.")

    # Level 2 test
    flags = {
        "ENABLE_WEB_SEARCH": "True",
        "USE_SANDBOX": "1",
        "ENABLE_TRACING": "yes",
        "DEBUG_LOGS": "False",
        "DRY_RUN": "0",
        "ALLOW_MUTATIONS": "no",
        "UNKNOWN_FLAG": "maybe",
    }
    parsed_flags = parse_agent_feature_flags(flags)
    assert parsed_flags["ENABLE_WEB_SEARCH"] is True
    assert parsed_flags["USE_SANDBOX"] is True
    assert parsed_flags["ENABLE_TRACING"] is True
    assert parsed_flags["DEBUG_LOGS"] is False
    assert parsed_flags["DRY_RUN"] is False
    assert parsed_flags["ALLOW_MUTATIONS"] is False
    assert parsed_flags["UNKNOWN_FLAG"] is False
    print("  [✓] Level 2 (Modify: boolean parsing) passed.")

    # Level 3 test
    sample_env = """
    # Comments should be ignored
    APP_NAME=SuperAgent
    DB_HOST="localhost"
    SECRET_TOKEN='secret_123'
    COMPLEX_URL=postgres://user:pass@host:5432/db?ssl=true
    
    # Empty lines ignored
    """
    dotenv_dict = load_dotenv_string(sample_env)
    assert dotenv_dict["APP_NAME"] == "SuperAgent"
    assert dotenv_dict["DB_HOST"] == "localhost"
    assert dotenv_dict["SECRET_TOKEN"] == "secret_123"
    assert dotenv_dict["COMPLEX_URL"] == "postgres://user:pass@host:5432/db?ssl=true"
    print("  [✓] Level 3 (Build: .env parser) passed.")

    # Level 4 test
    # Case 1: missing
    if "PORT_TEST" in os.environ:
        del os.environ["PORT_TEST"]
    assert load_agent_runtime_port("PORT_TEST", 3000) == 3000

    # Case 2: valid numeric
    os.environ["PORT_TEST"] = " 8000 "
    assert load_agent_runtime_port("PORT_TEST", 3000) == 8000

    # Case 3: invalid non-numeric
    os.environ["PORT_TEST"] = "not_a_number"
    assert load_agent_runtime_port("PORT_TEST", 3000) == 3000

    # Case 4: out of range
    os.environ["PORT_TEST"] = "70000"
    assert load_agent_runtime_port("PORT_TEST", 3000) == 3000

    # Clean up test variable
    del os.environ["PORT_TEST"]
    if "TEST_M5_KEY" in os.environ:
        del os.environ["TEST_M5_KEY"]

    print("  [✓] Level 4 (Debug: port parsing) passed.")

    print("All Module 27 exercise solutions verified successfully!\n")


def main() -> None:
    run_tests()


if __name__ == "__main__":
    main()
