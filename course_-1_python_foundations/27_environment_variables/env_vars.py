"""
Module 27: Environment Variables & Configuration Management
===========================================================

This lesson explores how Python interacts with operating system environment
variables to manage application configuration and sensitive API credentials.

Managing configuration via environment variables is the foundation of the
modern Twelve-Factor App methodology. It allows the exact same code to run in
local development, testing, staging, and production environments without
hardcoding sensitive secrets like API tokens into source code.

Sections in this Lesson:
------------------------
1. Reading Environment Variables: `os.environ` vs `os.getenv()`.
2. The String-Only Constraint and Safe Type Parsing (int, float, bool).
3. Modifying the Process Environment and Inheritance Mechanics.
4. Building a Complete `.env` File Parser from Scratch.
5. Structured, Immutable Agent Configuration Objects.
6. Secret Sanitization & Masking for Safe Agent Logging.
7. Multi-Environment Profile Switching (Dev, Test, Prod).
"""

import io
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Section 1: Reading Environment Variables
# ============================================================================

def demonstrate_reading_env_vars() -> None:
    """
    Demonstrates the difference between direct os.environ indexing and os.getenv().
    """
    print("=" * 70)
    print("1. READING ENVIRONMENT VARIABLES (os.environ vs os.getenv)")
    print("=" * 70)

    # Inspect common system environment variables provided by the OS
    user = os.getenv("USER") or os.getenv("USERNAME") or "anonymous_user"
    shell = os.getenv("SHELL", "/bin/sh")
    print(f"Current System User: {user}")
    print(f"Current System Shell: {shell}")

    # Set temporary demo variables
    os.environ["DEMO_APP_NAME"] = "AutonomousAgentEngine"

    # Reading with os.environ: raises KeyError if key is missing
    app_name = os.environ["DEMO_APP_NAME"]
    print(f"os.environ['DEMO_APP_NAME'] -> '{app_name}'")

    # Reading with os.getenv: returns default if missing
    non_existent = os.getenv("NON_EXISTENT_KEY", "DefaultFallbackValue")
    print(f"os.getenv('NON_EXISTENT_KEY', default) -> '{non_existent}'")

    # Demonstrating KeyError on missing direct index
    try:
        _ = os.environ["CRITICAL_MISSING_SECRET"]
    except KeyError as exc:
        print(f"Direct index of missing key properly raised KeyError: {exc}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 2: The String-Only Constraint and Safe Type Parsing
# ============================================================================

def parse_env_bool(val: Optional[str], default: bool = False) -> bool:
    """
    Safely converts an environment variable string into a boolean.
    Guards against the notorious `bool('False') == True` trap!
    """
    if val is None:
        return default
    normalized = val.strip().lower()
    if normalized in ("true", "1", "yes", "on", "t"):
        return True
    if normalized in ("false", "0", "no", "off", "f"):
        return False
    return default


def parse_env_int(val: Optional[str], default: int) -> int:
    """Safely converts an environment variable string to an integer with fallback."""
    if val is None:
        return default
    try:
        return int(val.strip())
    except ValueError:
        return default


def demonstrate_type_parsing() -> None:
    """
    Demonstrates parsing numbers and booleans from environment variable strings.
    """
    print("=" * 70)
    print("2. SAFE TYPE PARSING & THE BOOLEAN TRAP")
    print("=" * 70)

    os.environ["AGENT_MAX_ITERATIONS"] = "25"
    os.environ["AGENT_TEMPERATURE"] = "0.7"
    os.environ["AGENT_DEBUG_FLAG"] = "False"

    # Numeric conversion
    iterations = parse_env_int(os.getenv("AGENT_MAX_ITERATIONS"), default=10)
    temperature = float(os.getenv("AGENT_TEMPERATURE", "0.0"))
    print(f"Parsed iterations (int): {iterations} (type: {type(iterations).__name__})")
    print(f"Parsed temperature (float): {temperature} (type: {type(temperature).__name__})")

    # The Boolean Trap demonstration
    naive_bool = bool(os.getenv("AGENT_DEBUG_FLAG"))
    safe_bool = parse_env_bool(os.getenv("AGENT_DEBUG_FLAG"), default=True)

    print(f"\nEvaluating AGENT_DEBUG_FLAG='False':")
    print(f"   Naive bool(os.getenv('AGENT_DEBUG_FLAG')) -> {naive_bool} [TRAP! String 'False' is truthy]")
    print(f"   Safe parse_env_bool(...)                  -> {safe_bool} [CORRECT! Evaluated semantically]")
    print("-" * 70 + "\n")


# ============================================================================
# Section 3: Modifying Environment Variables and Process Isolation
# ============================================================================

def demonstrate_env_modification() -> None:
    """
    Demonstrates setting, updating, and removing environment variables within Python.
    """
    print("=" * 70)
    print("3. ENVIRONMENT MODIFICATION & PROCESS ISOLATION")
    print("=" * 70)

    key = "AGENT_EPHEMERAL_TOKEN"
    os.environ[key] = "tok_session_12345"
    print(f"Set {key} -> '{os.environ[key]}'")

    # Update value
    os.environ[key] = "tok_session_67890"
    print(f"Updated {key} -> '{os.environ[key]}'")

    # Remove value
    deleted_val = os.environ.pop(key, None)
    print(f"Popped {key} -> '{deleted_val}'")
    print(f"Key still in os.environ? {key in os.environ}")

    print("\nNote: Process modifications affect this Python process and any child")
    print("subprocesses it spawns, but NEVER alter the parent terminal shell.")
    print("-" * 70 + "\n")


# ============================================================================
# Section 4: Building a Complete .env File Parser
# ============================================================================

def parse_dotenv_content(content: str, override: bool = False) -> Dict[str, str]:
    """
    Parses key-value pairs from .env formatted content and optionally updates os.environ.
    
    Rules:
    1. Lines beginning with '#' or empty lines are ignored.
    2. Strips surrounding whitespace and quotes (' or ") around values.
    3. Handles keys with values containing '=' (e.g. CONNECTION_STRING=a=1&b=2).
    4. If override is False, does not overwrite existing os.environ variables.
    """
    parsed: Dict[str, str] = {}
    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue
        if "=" in trimmed:
            key_part, val_part = trimmed.split("=", 1)
            clean_key = key_part.strip()
            clean_val = val_part.strip()

            # Strip surrounding single or double quotes
            if (clean_val.startswith('"') and clean_val.endswith('"')) or \
               (clean_val.startswith("'") and clean_val.endswith("'")):
                clean_val = clean_val[1:-1]

            parsed[clean_key] = clean_val
            if override or clean_key not in os.environ:
                os.environ[clean_key] = clean_val

    return parsed


def demonstrate_dotenv_parsing() -> None:
    """
    Demonstrates loading simulated .env file content.
    """
    print("=" * 70)
    print("4. COMPLETE .env FILE PARSER IMPLEMENTATION")
    print("=" * 70)

    sample_dotenv = """
    # Agent Runtime Local Development Configuration
    AGENT_ENV=staging
    AGENT_MAX_RETRIES=5
    AGENT_API_ENDPOINT="https://staging.ai.internal/v1"
    AGENT_API_KEY='sk-staging-secret-key-9988'
    # Flags
    AGENT_TELEMETRY_ENABLED=true
    """

    parsed_records = parse_dotenv_content(sample_dotenv, override=True)
    print(f"Parsed {len(parsed_records)} variables from .env content:")
    for k, v in parsed_records.items():
        print(f"   {k:<26} = {v}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 5: Structured, Immutable Agent Configuration
# ============================================================================

@dataclass(frozen=True)
class AgentRuntimeConfig:
    """Immutable agent configuration schema with strict validation."""
    api_key: str
    environment: str
    max_retries: int
    api_endpoint: str
    telemetry_enabled: bool

    @classmethod
    def load_from_env(cls) -> "AgentRuntimeConfig":
        """Loads and validates configuration from os.environ."""
        # 1. Required API Key validation
        key = os.getenv("AGENT_API_KEY")
        if not key or not key.strip():
            raise ValueError("Configuration Error: AGENT_API_KEY is required and cannot be empty!")

        # 2. Environment mode validation
        env = os.getenv("AGENT_ENV", "development").lower()
        allowed_envs = {"development", "testing", "staging", "production"}
        if env not in allowed_envs:
            raise ValueError(f"Configuration Error: Invalid AGENT_ENV '{env}'. Must be one of: {allowed_envs}")

        # 3. Numeric parameters
        retries = parse_env_int(os.getenv("AGENT_MAX_RETRIES"), default=3)

        # 4. Endpoint with fallback
        endpoint = os.getenv("AGENT_API_ENDPOINT", "https://api.default.ai/v1")

        # 5. Boolean flags
        telemetry = parse_env_bool(os.getenv("AGENT_TELEMETRY_ENABLED"), default=False)

        return cls(
            api_key=key,
            environment=env,
            max_retries=retries,
            api_endpoint=endpoint,
            telemetry_enabled=telemetry,
        )


def demonstrate_structured_config() -> None:
    """
    Demonstrates instantiating an immutable configuration object from the environment.
    """
    print("=" * 70)
    print("5. STRUCTURED IMMUTABLE AGENT CONFIGURATION")
    print("=" * 70)

    config = AgentRuntimeConfig.load_from_env()
    print("Loaded Validated Configuration Object:")
    print(f"   Environment: {config.environment}")
    print(f"   Endpoint:    {config.api_endpoint}")
    print(f"   Retries:     {config.max_retries}")
    print(f"   Telemetry:   {config.telemetry_enabled}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 6: Secret Masking & Sanitization for Agent Logging
# ============================================================================

def mask_credential(secret: str, unmasked_prefix: int = 3, unmasked_suffix: int = 4) -> str:
    """
    Safely redacts a sensitive secret token for secure logging.
    Example: 'sk-proj-1234567890abcdef' -> 'sk-...cdef'
    """
    if not secret:
        return "[EMPTY]"
    total_len = len(secret)
    if total_len <= (unmasked_prefix + unmasked_suffix):
        return "*" * total_len
    
    prefix = secret[:unmasked_prefix]
    suffix = secret[-unmasked_suffix:]
    return f"{prefix}...{suffix}"


def sanitize_dict_for_logging(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively masks dictionary fields whose names suggest sensitive credentials.
    """
    sensitive_keywords = {"key", "secret", "token", "password", "auth", "credential"}
    sanitized: Dict[str, Any] = {}

    for k, v in data.items():
        is_sensitive = any(kw in k.lower() for kw in sensitive_keywords)
        if isinstance(v, str) and is_sensitive:
            sanitized[k] = mask_credential(v)
        elif isinstance(v, dict):
            sanitized[k] = sanitize_dict_for_logging(v)
        else:
            sanitized[k] = v

    return sanitized


def demonstrate_secret_masking() -> None:
    """
    Demonstrates redacting secrets from configuration dictionaries before logging.
    """
    print("=" * 70)
    print("6. SECRET MASKING FOR AGENT AUDIT LOGS")
    print("=" * 70)

    raw_agent_log_payload = {
        "event": "agent_boot",
        "agent_name": "Auditor-M5",
        "openai_api_key": "sk-proj-abc1234567890xyz9988",
        "database_password": "SuperSecretDbPassword2026",
        "session_token": "bearer_9876543210fedcba",
        "timeout_seconds": 30,
    }

    sanitized_log = sanitize_dict_for_logging(raw_agent_log_payload)
    print("Sanitized Log Payload (Safe to output to console/logs):")
    for k, v in sanitized_log.items():
        print(f"   {k:<20}: {v}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 7: Multi-Environment Profile Switching
# ============================================================================

def get_active_profile_settings() -> Dict[str, Any]:
    """
    Returns environment-specific thresholds and resource allocations.
    """
    env_name = os.getenv("AGENT_ENV", "development").lower()
    profiles = {
        "development": {"rate_limit": 10, "log_level": "DEBUG", "sandbox": True},
        "staging":     {"rate_limit": 50, "log_level": "INFO", "sandbox": True},
        "production":  {"rate_limit": 500, "log_level": "WARNING", "sandbox": False},
    }
    return profiles.get(env_name, profiles["development"])


def demonstrate_profile_switching() -> None:
    """
    Demonstrates resolving configuration profiles based on AGENT_ENV.
    """
    print("=" * 70)
    print("7. MULTI-ENVIRONMENT PROFILE SWITCHING")
    print("=" * 70)

    for env_target in ["development", "staging", "production"]:
        os.environ["AGENT_ENV"] = env_target
        settings = get_active_profile_settings()
        print(f"Profile [{env_target.upper()}]: RateLimit={settings['rate_limit']}, Log={settings['log_level']}, Sandbox={settings['sandbox']}")
    print("-" * 70 + "\n")


# ============================================================================
# Main Entry Point
# ============================================================================

def main() -> None:
    print("Starting Module 27: Environment Variables & Configuration Management\n")
    demonstrate_reading_env_vars()
    demonstrate_type_parsing()
    demonstrate_env_modification()
    demonstrate_dotenv_parsing()
    demonstrate_structured_config()
    demonstrate_secret_masking()
    demonstrate_profile_switching()
    print("Module 27 demonstration completed successfully!")


if __name__ == "__main__":
    main()
