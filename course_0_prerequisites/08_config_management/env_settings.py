"""env_settings.py - Production-grade configuration with pydantic-settings and SecretStr masking.

Key concepts demonstrated:
1. Subclassing pydantic_settings.BaseSettings.
2. Field-level validation and environment prefixing.
3. SecretStr masking to protect API keys in logs and representations.
"""

import os
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProductionAgentSettings(BaseSettings):
    """Strongly-typed production settings for an autonomous agent service."""

    # Agent Metadata
    agent_name: str = Field(default="ProductionMiniAgent", description="Identifier for this agent cluster")
    max_steps: int = Field(default=10, ge=1, le=100, description="Max reasoning steps per run")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0, description="Sampling temperature")

    # Storage & Persistence
    db_path: str = Field(default="./agent_memory.db", description="Path to SQLite memory file")

    # Sensitive API Keys
    openai_api_key: SecretStr = Field(
        default=SecretStr("mock-sk-unconfigured"),
        description="LLM provider API key"
    )

    # Configuration options
    model_config = SettingsConfigDict(
        env_prefix="AGENT_",
        case_sensitive=False
    )

    @field_validator("db_path")
    @classmethod
    def validate_sqlite_path(cls, v: str) -> str:
        if not v.endswith(".db") and ":memory:" not in v:
            raise ValueError("db_path must end with '.db' or be ':memory:'")
        return v


def main() -> None:
    print("=== Module 08: Pydantic Settings & Secret Masking Demo ===")

    # Set mock environment variables using the AGENT_ prefix
    os.environ["AGENT_AGENT_NAME"] = "SwarmCoordinator"
    os.environ["AGENT_MAX_STEPS"] = "20"
    os.environ["AGENT_OPENAI_API_KEY"] = "sk-live-production-secret-998877"

    settings = ProductionAgentSettings()

    # 1. Verify environment values were loaded and coerced
    assert settings.agent_name == "SwarmCoordinator"
    assert settings.max_steps == 20
    assert isinstance(settings.max_steps, int)
    print(f"[OK] Settings loaded: agent_name={settings.agent_name}, max_steps={settings.max_steps}")

    # 2. Verify SecretStr masking
    repr_str = repr(settings)
    assert "sk-live-production-secret" not in repr_str
    assert "**********" in repr_str
    print(f"[OK] Masked settings representation:\n{repr_str}")

    # 3. Verify accessing unmasked secret explicitly
    raw_secret = settings.openai_api_key.get_secret_value()
    assert raw_secret == "sk-live-production-secret-998877"
    print(f"[OK] Explicit secret retrieval successful (length: {len(raw_secret)} chars).")

    # 4. Clean up environment
    del os.environ["AGENT_AGENT_NAME"]
    del os.environ["AGENT_MAX_STEPS"]
    del os.environ["AGENT_OPENAI_API_KEY"]

    print("All tests in env_settings.py passed successfully!\n")


if __name__ == "__main__":
    main()
