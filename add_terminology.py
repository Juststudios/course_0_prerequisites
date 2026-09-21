import os
from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl")

# 1. Create Glossary
ref_dir = BASE_DIR / "reference"
ref_dir.mkdir(exist_ok=True)
with open(ref_dir / "glossary.md", "w") as f:
    f.write("""# Master Terminology Glossary

## Python
* **Callable**: An object that can be invoked like a function. Example: `add(2,3)`.

## Machine Learning
* **Feature**: An input variable used by a model.
* **Target**: The value the model is trying to predict.
* **Training**: Adjusting a model using data.
* **Model**: A system mapping inputs to outputs.

## AI Agents
* **Tool**: A callable function provided to the LLM.
* **Registry**: A mapping of tool names to implementations.
""")

def prepend_terminology(filepath, terminology_md):
    p = BASE_DIR / filepath
    if p.exists():
        content = p.read_text()
        if "## Key Terminology" not in content:
            # Insert after the first heading
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    lines.insert(i + 1, "\n" + terminology_md + "\n")
                    break
            p.write_text('\n'.join(lines))

prepend_terminology("machine-learning/README.md", """## Key Terminology
* **Feature:** An input variable used by a machine-learning model.
* **Target:** The value the model is trying to predict.
* **Training:** The process of adjusting a model using data.
* **Model:** A mathematical/computational system that maps inputs to outputs.
""")

prepend_terminology("networking/README.md", """## Key Terminology
* **Client:** The program making the request.
* **Server:** The program answering the request.
* **HTTP:** The protocol for web communication.
* **Endpoint:** A specific URL where an API lives.
""")

prepend_terminology("game-ai/README.md", """## Key Terminology
* **State:** The current condition of the game board.
* **Minimax:** An algorithm for finding the optimal move in a zero-sum game.
* **Heuristic:** A rule-of-thumb evaluation function.
""")

print("Terminology added.")
