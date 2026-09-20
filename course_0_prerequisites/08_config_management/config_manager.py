"""config_manager.py - Lightweight standalone configuration loader with precedence hierarchy.

Key concepts demonstrated:
1. Pure-Python .env file parser handling comments, exports, and quoted values.
2. Configuration precedence: OS Environment > .env File > Defaults.
3. Safe type coercion (string to int, float, bool).
"""

from typing import Dict, Any, Optional
import os
import io


class SimpleConfigManager:
    """Manages application settings across defaults, .env files, and OS environment."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self._config: Dict[str, Any] = defaults.copy() if defaults else {}

    def parse_dotenv(self, stream_or_text: str | io.StringIO) -> Dict[str, str]:
        """Parses .env syntax into a dictionary of key-value strings."""
        lines = stream_or_text.getvalue().splitlines() if isinstance(stream_or_text, io.StringIO) else stream_or_text.splitlines()
        parsed: Dict[str, str] = {}

        for line in lines:
            line = line.strip()
            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Handle 'export KEY=VAL'
            if line.startswith("export "):
                line = line[len("export "):].strip()
            if "=" not in line:
                continue

            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()

            # Strip matching quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]

            parsed[key] = val

        return parsed

    def load(self, dotenv_content: Optional[str] = None) -> Dict[str, Any]:
        """Applies precedence: OS Environment > .env text > Defaults."""
        # 1. Overlay .env if provided
        if dotenv_content:
            parsed_env = self.parse_dotenv(dotenv_content)
            self._config.update(parsed_env)

        # 2. Overlay OS environment variables if they match config keys
        for key in list(self._config.keys()):
            if key in os.environ:
                self._config[key] = os.environ[key]

        return self._config

    def get_int(self, key: str, default: int = 0) -> int:
        val = self._config.get(key, default)
        return int(val)

    def get_float(self, key: str, default: float = 0.0) -> float:
        val = self._config.get(key, default)
        return float(val)

    def get_bool(self, key: str, default: bool = False) -> bool:
        val = self._config.get(key, default)
        if isinstance(val, bool):
            return val
        return str(val).lower() in ("1", "true", "yes", "on")

    def get_str(self, key: str, default: str = "") -> str:
        val = self._config.get(key, default)
        return str(val)


def main() -> None:
    print("=== Module 08: Standalone Config Manager Demo ===")

    # Sample defaults
    defaults = {
        "AGENT_NAME": "DefaultAgent",
        "MAX_STEPS": 5,
        "TIMEOUT": 10.0,
        "ENABLE_SEARCH": False,
        "OVERRIDE_TEST": "from_defaults",
    }

    # Sample .env file text
    sample_dotenv = """
    # Agent Runtime Configuration
    AGENT_NAME="HermesAgent"
    MAX_STEPS=15
    TIMEOUT=25.5
    ENABLE_SEARCH=true
    OVERRIDE_TEST="from_dotenv"
    """

    # Set one OS environment variable to test top precedence
    os.environ["OVERRIDE_TEST"] = "from_os_environ"

    cfg = SimpleConfigManager(defaults)
    resolved = cfg.load(sample_dotenv)

    # Assertions
    assert cfg.get_str("AGENT_NAME") == "HermesAgent"
    assert cfg.get_int("MAX_STEPS") == 15
    assert cfg.get_float("TIMEOUT") == 25.5
    assert cfg.get_bool("ENABLE_SEARCH") is True
    # Verify OS env won over .env and defaults
    assert cfg.get_str("OVERRIDE_TEST") == "from_os_environ"

    print("[OK] Parsed .env configuration successfully:")
    for k, v in resolved.items():
        print(f"  - {k} = {v}")

    # Clean up os.environ
    del os.environ["OVERRIDE_TEST"]
    print("All tests in config_manager.py passed successfully!\n")


if __name__ == "__main__":
    main()
