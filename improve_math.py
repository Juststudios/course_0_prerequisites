from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/engineering-mathematics")

def append_to_file(path_str, content):
    p = BASE_DIR / path_str
    if p.exists():
        with open(p, "a") as f:
            f.write("\n" + content.strip() + "\n")

append_to_file("README.md", """
## AI and Machine Learning Bridges

Engineering Mathematics isn't just for classical physics. These exact same mathematical foundations run modern AI.

* **Linear Algebra:** Vectors and matrices form the foundation of embeddings (word meanings) and LLM parameter weights.
* **Calculus:** Derivatives and gradients are the engine of Neural Network learning (Gradient Descent).
* **Probability:** LLMs don't "know" facts; they calculate conditional probabilities for the next token. 

*If you are preparing for AI Agent Engineering, see `Course 0: Prerequisites` for dedicated math bridges.*
""")

print("Mathematics improved.")
