import os
from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/course_0_prerequisites")

# Structure definition
dirs = [
    "01_python_foundations",
    "02_type_hints",
    "03_async_python",
    "04_context_management",
    "05_http_and_apis",
    "06_configuration",
    "07_subprocesses",
    "08_sqlite",
    "09_software_architecture",
    "10_math_for_agents",
    "projects/mini_agent",
    "assessments",
    "reference"
]

for d in dirs:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

print("Directories created.")
