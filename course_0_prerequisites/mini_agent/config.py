"""config.py - Strongly-typed Pydantic settings for MiniAgent."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Runtime configuration settings for MiniAgent."""

    agent_name: str = Field(
        default="MiniAgent",
        description="Name identifier of the agent runtime."
    )
    max_steps: int = Field(
        default=8,
        ge=1,
        le=50,
        description="Maximum ReAct reasoning steps before forced termination."
    )
    db_path: str = Field(
        default=":memory:",
        description="SQLite database path (use ':memory:' for ephemeral state)."
    )
    timeout_seconds: float = Field(
        default=10.0,
        ge=1.0,
        le=120.0,
        description="Global timeout in seconds for agent operations."
    )
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Sampling temperature for reasoning decisions."
    )
    verbose: bool = Field(
        default=True,
        description="Whether to print step-by-step reasoning traces."
    )

    model_config = SettingsConfigDict(
        env_prefix="MINI_AGENT_",
        case_sensitive=False,
        extra="ignore"
    )
