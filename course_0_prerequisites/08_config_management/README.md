# Module 08: Configuration Management, Environment Variables, and Secret Masking

## 1. Learning Objectives
By the end of this module, you will be able to:
- Understand the 12-Factor App methodology for separating code from configuration.
- Read, coerce, and validate environment variables with fallback precedence hierarchies (CLI flags > Process Env > `.env` file > Hardcoded defaults).
- Author a lightweight pure-Python `.env` parser capable of handling comments, unquoted and quoted strings, and exports.
- Leverage `pydantic-settings` to declare strongly typed, validated agent configuration classes.
- Prevent disastrous production credential leakage using Pydantic's `SecretStr` to mask API keys and database passwords in logs and traces.

---

## 2. Why AI Agent Engineers Need This
Autonomous agents are configuration-intensive systems. A typical agent requires:
- Multiple LLM vendor API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- Base URLs (for local vLLM or Ollama instances).
- Operational parameters (`MAX_STEPS=10`, `TEMPERATURE=0.2`, `TIMEOUT_SECONDS=30`).
- Persistence settings (`SQLITE_DB_PATH=/var/data/agent.db`).

Hardcoding these values into Python code:
1. Prevents deployment across multiple environments (local development, staging, production).
2. Guarantees catastrophic security breaches when code containing live API keys is pushed to public GitHub repositories or written to application logs.

Proper configuration management ensures your agent behaves dynamically across environments while keeping secrets securely isolated.

---

## 3. Structured Concept Breakdown

### Concept 1: Environment Variables & Precedence
- **TERM**: Environment Variables & Precedence
- **DEFINITION**: Key-value string pairs maintained by the operating system kernel for a running process, resolved according to a defined hierarchy of precedence.
- **INTUITION**: A traveler packing for a trip. They bring standard clothing (defaults), but check the local weather report (.env), receive updated instructions at the airport (environment variables), and make immediate emergency purchases at the destination (CLI arguments). The most specific instructions override the general ones.
- **WHY IT EXISTS**: Docker containers and cloud platforms (Kubernetes, AWS ECS, Fly.io) inject credentials and configurations directly as environment variables.
- **HOW IT WORKS**: Python accesses process environment variables via `os.environ`. When resolving a setting, the application checks sources in priority order:
  $$\text{CLI Arguments} > \text{OS Environment Variables} > \text{.env File} > \text{Default Values}$$
- **CODE**:
```python
import os

def get_int_setting(key: str, default: int) -> int:
    val = os.environ.get(key)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        raise ValueError(f"Environment variable '{key}' must be an integer, got: {val!r}")
```

---

### Concept 2: `.env` File Format & Parsing
- **TERM**: `.env` File Parsing
- **DEFINITION**: Reading line-delimited key-value configuration text files, ignoring comments (`#`) and empty lines, and stripping surrounding quotes.
- **INTUITION**: A local scratchpad. During development on your laptop, you don't want to type `export API_KEY=xyz` every time you open a terminal; a `.env` file automatically populates those variables for your project.
- **WHY IT EXISTS**: Provides reproducible local environments without polluting the system-wide shell environment or accidentally committing secrets to git.
- **HOW IT WORKS**: A parser iterates line-by-line:
  - Strips leading/trailing whitespace.
  - Skips empty lines and lines starting with `#`.
  - Splits on the first `=` into key and value.
  - Strips matching enclosing double (`"`) or single (`'`) quotes.
- **CODE**:
```python
def load_dotenv_text(content: str) -> dict[str, str]:
    config = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            config[key] = val
    return config
```

---

### Concept 3: Pydantic Settings (`BaseSettings`)
- **TERM**: Pydantic BaseSettings
- **DEFINITION**: A specialized class from `pydantic-settings` that automatically reads environment variables and `.env` files into a strongly typed Pydantic model with validation.
- **INTUITION**: An automated smart receptionist who takes raw sticky notes left on their desk (string env vars), verifies every phone number and email address, and hands you an organized, typed binder.
- **WHY IT EXISTS**: Writing custom coercion and validation logic for 20 configuration variables is tedious and error-prone. `BaseSettings` handles type conversion (e.g. converting `"false"` to `False`, `"1.5"` to `1.5`, or comma-separated lists to `list[str]`) automatically.
- **HOW IT WORKS**: Upon instantiation, `BaseSettings` inspects its fields and queries `os.environ` and any configured `.env` files for matching variable names (case-insensitively or with a custom prefix).
- **CODE**:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AgentSettings(BaseSettings):
    agent_name: str = "MiniAgent"
    max_steps: int = Field(default=10, ge=1, le=50)
    debug_mode: bool = False

    model_config = SettingsConfigDict(env_prefix="AGENT_")
```

---

### Concept 4: Secret Masking via `SecretStr`
- **TERM**: `SecretStr`
- **DEFINITION**: A Pydantic data type designed for sensitive text (passwords, tokens, keys) that displays as `'**********'` when converted to a string or printed in logs.
- **INTUITION**: A credit card number on a printed receipt showing only `************1234`. Anyone glancing at the receipt cannot steal the card number.
- **WHY IT EXISTS**: Developers frequently log configuration at startup (`logger.info(f"Loaded config: {config}")`) or print state when debugging crashes. Without `SecretStr`, real OpenAI and database credentials end up in Datadog, CloudWatch, or Sentry logs.
- **HOW IT WORKS**: `SecretStr` overrides `__str__`, `__repr__`, and JSON serialization methods to return masked asterisks. To access the raw secret value in trusted code, the developer must explicitly call `secret.get_secret_value()`.
- **CODE**:
```python
from pydantic import BaseModel, SecretStr

class APIConfig(BaseModel):
    api_key: SecretStr

cfg = APIConfig(api_key="sk-live-super-secret-12345")
print(cfg)  # api_key=SecretStr('**********')
print(str(cfg.api_key))  # '**********'

# Explicit unmasking only when needed:
raw_key = cfg.api_key.get_secret_value()  # 'sk-live-super-secret-12345'
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Leaking Secrets in Trace Logs
- **The Bug**: Logging raw agent tool payloads containing an API key or bearer token to stdout.
- **The Consequence**: Trace logs indexed by third-party services (e.g. PostHog, LangSmith, DataDog) expose administrative keys to anyone with log read access.
- **The Fix**: Wrap sensitive fields in `SecretStr` and sanitize all outbound logs.

### Anti-Pattern 2: Committing `.env` to Version Control
- **The Bug**: Forgetting to add `.env` to `.gitignore`.
- **The Consequence**: Automated bots scraping GitHub commit history clone the repository and drain thousands of dollars in LLM API credits within minutes.
- **The Fix**: Always provide `.env.example` in git and add `.env` to `.gitignore`.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What method must be called on a Pydantic `SecretStr` to retrieve the underlying unmasked string?
2. In what order of precedence should configuration values resolve?
3. How does Pydantic `BaseSettings` coerce the environment string `"true"` or `"1"` for a `bool` field?

### Tier 2 (Debugging)
Find the bug in this configuration class:
```python
class AppConfig:
    DB_PORT = os.environ.get("DB_PORT", 5432)
    # What is the bug when DB_PORT is set in the OS environment?
```
*Hint*: `os.environ.get()` returns a string! If `DB_PORT="5432"`, it is a `str`, but default is `int`.

### Tier 3 (Application)
Write a Python function `load_config(env_path: str, defaults: dict) -> dict` that loads key-value pairs from a `.env` file, overlays them onto `defaults`, and allows any existing environment variables in `os.environ` to take top precedence.

### Tier 4 (Challenge)
Build a `SecureAgentSettings` class using `pydantic-settings` that:
- Loads `OPENAI_API_KEY` as a `SecretStr`.
- Loads `MAX_RETRIES` as an integer between 1 and 10.
- Validates that `DB_URL` starts with `sqlite:///` or `postgresql://`.
- Demonstrates safe logging where secrets are masked, but verified valid.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/08_config_management/config_manager.py
python3 course_0_prerequisites/08_config_management/env_settings.py
```
