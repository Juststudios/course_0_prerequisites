"""solutions_c0_modules.py - Reference Solutions and Automated Verification Suite for Course 0 Exercises."""

from typing import List, Dict, Any, Optional
import math
import re


# Exercise 1: Safe AST Calculator
def solution_safe_add(a: float, b: float) -> float:
    return float(a + b)


# Exercise 2: Dunder Representation
class SolutionAgentMessage:
    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        return f"SolutionAgentMessage(role={self.role!r}, content={self.content!r})"

    def __str__(self) -> str:
        return f"[{self.role.upper()}]: {self.content}"


# Exercise 3: Code Fence Stripper
def solution_strip_fences(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1].strip()
    return text


# Exercise 4: Cosine Similarity
def solution_cosine_similarity(u: List[float], v: List[float]) -> float:
    dot = sum(a * b for a, b in zip(u, v))
    norm_u = math.sqrt(sum(a * a for a in u))
    norm_v = math.sqrt(sum(b * b for b in v))
    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    return dot / (norm_u * norm_v)


# Exercise 5: Softmax with Temperature
def solution_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
    t = max(1e-4, temp)
    scaled = [z / t for z in logits]
    max_z = max(scaled)
    exp_vals = [math.exp(z - max_z) for z in scaled]
    sum_exp = sum(exp_vals)
    return [ev / sum_exp for ev in exp_vals]


def main() -> None:
    print("=== Course 0 Reference Solutions Test Runner ===")

    # 1. Math check
    assert solution_safe_add(15.0, 27.0) == 42.0
    print("[OK] Solution 1 (safe_add) passed.")

    # 2. Dunder check
    msg = SolutionAgentMessage("user", "Hello agent!")
    assert str(msg) == "[USER]: Hello agent!"
    assert "SolutionAgentMessage(role='user'" in repr(msg)
    print("[OK] Solution 2 (AgentMessage dunders) passed.")

    # 3. Fence stripper check
    fenced = "Here is the json:\n```json\n{\"test\": true}\n```\nDone."
    assert solution_strip_fences(fenced) == '{"test": true}'
    print("[OK] Solution 3 (strip_fences) passed.")

    # 4. Cosine similarity check
    assert math.isclose(solution_cosine_similarity([1, 0], [1, 0]), 1.0)
    assert math.isclose(solution_cosine_similarity([1, 0], [0, 1]), 0.0)
    print("[OK] Solution 4 (cosine_similarity) passed.")

    # 5. Softmax check
    probs = solution_softmax([5.0, 1.0], temp=0.1)
    assert probs[0] > 0.99
    assert math.isclose(sum(probs), 1.0)
    print("[OK] Solution 5 (softmax) passed.")

    print("\nAll reference solutions verified with 100% pass rate!\n")


if __name__ == "__main__":
    main()
