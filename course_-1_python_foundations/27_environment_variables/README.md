# Topic: Environment Variables and Configuration Management

## What You Will Learn
In this module, you will learn:
- What environment variables are and how operating systems pass state to running processes.
- Why hardcoding configuration and secret credentials inside source code is dangerous.
- How to access environment variables in Python using `os.environ` and `os.getenv()`.
- How to handle missing variables safely with default values vs strictly enforcing required keys.
- How to properly parse types from environment variables (converting string values to `int`, `float`, and `bool`).
- The Twelve-Factor App methodology principle: "Store config in the environment".
- How `.env` files work during local development and how to parse `.env` files from scratch.
- Best practices for secret hygiene: `.gitignore`, environment masking, and keeping credentials out of logs.
- How autonomous AI agents dynamically load LLM API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`), database credentials, and execution runtime modes.

## Prerequisites
Before tackling this module, you should be familiar with:
- Module 03: Variables and Primitive Data Types.
- Module 06: Collections (Dictionaries and key lookups).
- Module 10: Errors and Exception Handling (`KeyError`, `ValueError`).
- Module 11: File Reading and Context Managers.

## The Problem
Suppose you are writing an AI agent that calls an external LLM API and connects to a production database. A naive developer might write:
```python
# DANGEROUS! NEVER DO THIS!
API_KEY = "sk-proj-998877665544332211aabbccddeeff"
DB_PASSWORD = "super_secret_admin_pass"
DATABASE_URL = "postgres://admin:super_secret_admin_pass@db.internal:5432/agent_prod"
```
This pattern leads to critical security disasters:
1. **Accidental Public Exposure**: The moment you run `git push origin main`, your private API keys and database credentials are permanently recorded in Git history. Automated web scrapers harvest exposed keys within seconds, running up thousands of dollars in unauthorized API bills or deleting production databases.
2. **Environment Inflexibility**: If you want to test your agent on your local machine using a mock endpoint, you must manually edit the code. When deploying to staging, you edit the code again. When deploying to production, you edit the code a third time. Code should be immutable; configuration should be externalized.

We need a way to completely separate **code** (how the agent executes) from **configuration** (which credentials and endpoints the agent connects to). The universal solution is **Environment Variables**.

## Key Terminology
- **Environment Variable**: A dynamic key-value string pair maintained by the operating system for a running process.
- **Process Environment**: The table of environment variables inherited by a program when the OS launches it.
- **`os.environ`**: A Python dictionary-like mapping object that wraps the operating system's process environment.
- **`os.getenv()`**: A convenience function for retrieving environment variables with fallback default values.
- **`.env` File**: A simple text file containing `KEY=VALUE` pairs used to populate environment variables during local development.
- **Twelve-Factor App**: A widely adopted software methodology advocating for strict separation of config from code via environment variables.
- **Secret Masking / Redaction**: Obscuring sensitive credential tokens in logs or console output (e.g. `sk-...11ff`) to prevent accidental leaks.

## Intuition
Think of a rental car:
- **The Code** is the car itself: the engine, steering wheel, transmission, and pedals. The manufacturer builds the car the exact same way for every driver.
- **The Environment Variables** are the driver's personalized settings: the driver's mirror angle, seat position, temperature setting, and Bluetooth pairing.

When you get into a rental car, you don't rebuild the engine—you just adjust the environment settings. Similarly, your AI agent codebase remains identical whether running on a developer laptop, inside a GitHub Actions CI test runner, or deployed inside a Kubernetes cloud cluster. The environment variables tell the agent which persona, endpoints, and API credentials to use.

## Concept
### 1. Process Inheritance
When an operating system launches a new process (such as `python main.py`):
1. The OS creates a new process space.
2. The child process receives an isolated **copy** of all environment variables present in the parent process (the terminal shell).
3. If Python modifies an environment variable via `os.environ["KEY"] = "new_val"`, the change is visible to Python and any child subprocesses it spawns, but it does **not** alter the parent terminal shell.

### 2. Everything is a String
The operating system stores all environment variable keys and values exclusively as **strings**.
```python
import os
os.environ["MAX_RETRIES"] = "5"
# type(os.environ["MAX_RETRIES"]) is ALWAYS str!
retries = int(os.environ["MAX_RETRIES"])  # Must explicitly cast!
```

### 3. The Boolean Trap
A notorious trap in Python:
```python
os.environ["DEBUG"] = "False"
is_debug = bool(os.environ.get("DEBUG"))
# DANGER: bool("False") is TRUE because non-empty strings are truthy!
```
Always parse booleans by comparing against recognized strings (e.g., `os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")`).

## Syntax
### Reading and Setting Environment Variables
```python
import os

# 1. Reading with mandatory requirement (raises KeyError if missing)
try:
    api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    raise RuntimeError("Missing required environment variable: OPENAI_API_KEY")

# 2. Reading with default fallback (returns None or specified default)
db_port = int(os.getenv("DB_PORT", "5432"))
log_level = os.getenv("LOG_LEVEL", "INFO")

# 3. Setting environment variables within the Python process
os.environ["AGENT_NAME"] = "Sentinel-1"

# 4. Deleting an environment variable from the current process
if "TEMP_SECRET" in os.environ:
    del os.environ["TEMP_SECRET"]
```

### Parsing a `.env` File from Scratch
```python
def load_dotenv_simple(filepath: str = ".env") -> None:
    """Reads a .env file and injects variables into os.environ."""
    import os
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")  # Strip surrounding quotes
                # Only set if not already set in OS environment
                if key not in os.environ:
                    os.environ[key] = val
```

## Example
Here is an executable configuration loader pattern designed for autonomous agents:

```python
import os
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AgentConfig:
    api_key: str
    environment: str
    max_tokens: int
    debug: bool

    @classmethod
    def from_environment(cls) -> "AgentConfig":
        # 1. Required key validation
        key = os.getenv("AGENT_API_KEY")
        if not key:
            raise ValueError("AGENT_API_KEY environment variable is required!")

        # 2. Optional keys with sensible defaults
        env = os.getenv("AGENT_ENV", "development").lower()
        
        # 3. Numeric type conversion
        try:
            tokens = int(os.getenv("AGENT_MAX_TOKENS", "4096"))
        except ValueError:
            tokens = 4096

        # 4. Safe boolean parsing
        raw_debug = os.getenv("AGENT_DEBUG", "false").lower()
        debug_mode = raw_debug in ("true", "1", "yes", "on")

        return cls(api_key=key, environment=env, max_tokens=tokens, debug=debug_mode)

    def mask_key(self) -> str:
        """Safely mask API key for logging purposes."""
        if len(self.api_key) <= 8:
            return "***"
        return f"{self.api_key[:4]}...{self.api_key[-4:]}"

if __name__ == "__main__":
    os.environ["AGENT_API_KEY"] = "sk-ai-agent-9876543210abcdef"
    os.environ["AGENT_ENV"] = "production"
    os.environ["AGENT_MAX_TOKENS"] = "8192"
    os.environ["AGENT_DEBUG"] = "true"

    config = AgentConfig.from_environment()
    print(f"Loaded Config: env={config.environment}, tokens={config.max_tokens}, debug={config.debug}")
    print(f"Masked Credential: {config.mask_key()}")
```

## Line-by-Line Explanation
1. `@dataclass(frozen=True)`: Creates an immutable configuration object ensuring parameters cannot be modified during agent execution.
2. `key = os.getenv("AGENT_API_KEY")`: Looks up the variable without crashing if it is absent.
3. `if not key: raise ValueError(...)`: Explicitly fails fast with a descriptive error message if a critical credential is missing.
4. `tokens = int(os.getenv("AGENT_MAX_TOKENS", "4096"))`: Casts the string to an integer, guarding with a fallback default.
5. `raw_debug in ("true", "1", "yes", "on")`: Avoids the `bool("False") == True` trap by checking against recognized truthy strings.
6. `mask_key()`: Slices the first and last four characters, replacing the middle with ellipses to protect secrets from leaking into log files.

## What Python Is Doing
1. During startup, Python's C bootstrap initialization code accesses the POSIX global `extern char **environ` pointer (or Windows equivalent via `GetEnvironmentStringsW`).
2. It populates an internal `os._Environ` instance that mirrors this memory table.
3. When you read `os.environ[k]`, Python performs a lookup in its internal mapping.
4. When you modify `os.environ[k] = v`, Python updates its internal dictionary and invokes the C library `setenv()` function, updating the operating system's native process environment memory block.
5. When Python spawns a subprocess (e.g. via `subprocess.run()`), the OS clones Python's current environment table and assigns it to the child process.

## Common Mistakes
1. **Falling for the `bool("False")` Truthiness Trap**:
   `bool(os.getenv("FEATURE_FLAG", "False"))` evaluates to `True`! You must inspect the string contents.
2. **Crashing on Missing Variables**:
   Using `os.environ["OPTIONAL_KEY"]` raises `KeyError`. Use `os.getenv("OPTIONAL_KEY", default)` for optional settings.
3. **Accidentally Committing `.env` to Git**:
   Always add `.env` to `.gitignore`. Commit a `.env.example` file instead, containing variable names without actual secret values.
4. **Expecting Child Edits to Alter Parent Shell**:
   Modifying `os.environ["FOO"] = "BAR"` inside Python does not persist after the script exits; the parent bash/zsh shell remains unchanged.
5. **Logging Full Environment Dumps**:
   Executing `print(dict(os.environ))` in error handlers will dump all API keys, access tokens, and passwords directly into log files.

## Real-World Uses
- **Twelve-Factor Web Services**: Web apps deployed to AWS, Google Cloud, or Heroku configure ports, database credentials, and redis URLs via environment variables.
- **Docker Containers**: Passing configuration at container launch using `docker run -e DB_HOST=prod-db my-app`.
- **CI/CD Pipelines**: GitHub Actions and GitLab CI inject repository secrets (deploy keys, cloud tokens) into runner environments.
- **Database Connection Strings**: Dynamically routing queries to read replicas or staging databases without altering application code.

## Connection to AI Agents
AI agents depend heavily on environment variables:
- **Provider API Keys**: Connecting to OpenAI (`OPENAI_API_KEY`), Anthropic (`ANTHROPIC_API_KEY`), HuggingFace (`HF_TOKEN`), and Pinecone (`PINECONE_API_KEY`).
- **Telemetry and Tracing**: LangSmith and OpenTelemetry use environment variables (`LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_API_KEY=...`) to record agent execution traces.
- **Runtime Sandboxing**: Agents use environment variables (e.g. `AGENT_SANDBOX_DIR=/workspace/sandbox`) to restrict tool execution to safe directory boundaries.
- **Safety Toggles**: Emergency kill-switches and dry-run flags (`AGENT_DRY_RUN=true`, `AGENT_MAX_STEPS=15`) configured at deployment time.

## Practice
1. Inspect your current Python environment using `os.environ.get("USER")` or `os.environ.get("PATH")`.
2. Write a function that reads an environment variable `TIMEOUT` and returns it as an integer, defaulting to 10 if missing or invalid.
3. Create a test `.env` file containing 3 lines of key-value pairs, parse it, and verify the values.

## Challenge
Can you build an enterprise-grade agent configuration manager that supports type parsing, secret masking, validation rules, and `.env` fallback loading? (We will build this in `exercises.py`!)

## Summary
- Environment variables decouple application code from environment-specific configuration and secrets.
- `os.environ` provides a dictionary interface to process environment variables; `os.getenv` provides fallback defaults.
- All environment variables are strings and must be explicitly converted to `int`, `float`, or `bool`.
- Never commit secrets to version control; use `.env` files locally and `.gitignore` them.
- Autonomous AI agents rely on environment variables for API tokens, database connections, and safety runtime parameters.

## What You Should Know Before Moving On
- The difference between `os.environ["KEY"]` and `os.getenv("KEY", default)`.
- How to safely parse boolean environment variables without falling into the truthy string trap.
- Why `.env` files must be excluded from Git repositories.
- How to mask sensitive API keys in logging output.
- How AI agents load and manage external provider credentials.
