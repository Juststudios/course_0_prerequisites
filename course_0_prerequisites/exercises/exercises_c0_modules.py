"""exercises_c0_modules.py - Practical Coding Exercises for Course 0 Modules.

Run this file with pytest or python3 to test exercise implementations.
"""

from typing import List, Dict, Any, Optional
import math
import re


# Exercise 1: Safe AST Calculator (Module 01 & 09)
def student_safe_add(a: float, b: float) -> float:
    """Exercise 1.1: Return the sum of two numbers."""
    return a + b


# Exercise 2: Dunder representation (Module 02)
class StudentAgentMessage:
    """Exercise 2.1: Implement __repr__ and __str__."""
    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        return f"StudentAgentMessage(role={self.role!r}, content={self.content!r})"

    def __str__(self) -> str:
        return f"[{self.role.upper()}]: {self.content}"


# Exercise 3: Code fence stripper (Module 07)
def student_strip_fences(text: str) -> str:
    """Exercise 7.1: Extract JSON from markdown backticks."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1].strip()
    return text


# Exercise 4: Cosine similarity (Module 15)
def student_cosine_similarity(u: List[float], v: List[float]) -> float:
    """Exercise 15.1: Calculate cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(u, v))
    norm_u = math.sqrt(sum(a * a for a in u))
    norm_v = math.sqrt(sum(b * b for b in v))
    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    return dot / (norm_u * norm_v)


# Exercise 5: Softmax with temperature (Module 15)
def student_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
    """Exercise 15.2: Calculate numerically stable softmax with temperature."""
    t = max(1e-4, temp)
    scaled = [z / t for z in logits]
    max_z = max(scaled)
    exp_vals = [math.exp(z - max_z) for z in scaled]
    sum_exp = sum(exp_vals)
    return [ev / sum_exp for ev in exp_vals]


def test_student_exercises() -> None:
    # 1. Test math
    assert student_safe_add(15.0, 27.0) == 42.0

    # 2. Test dunders
    msg = StudentAgentMessage("user", "Hello agent!")
    assert str(msg) == "[USER]: Hello agent!"
    assert "StudentAgentMessage(role='user'" in repr(msg)

    # 3. Test fence stripper
    fenced = "Here is the json:\n```json\n{\"test\": true}\n```\nDone."
    assert student_strip_fences(fenced) == '{"test": true}'

    # 4. Test cosine similarity
    assert math.isclose(student_cosine_similarity([1, 0], [1, 0]), 1.0)
    assert math.isclose(student_cosine_similarity([1, 0], [0, 1]), 0.0)

    # 5. Test softmax
    probs = student_softmax([5.0, 1.0], temp=0.1)
    assert probs[0] > 0.99
    assert math.isclose(sum(probs), 1.0)

    print("All exercise validation checks passed successfully!")


if __name__ == "__main__":
    test_student_exercises()
