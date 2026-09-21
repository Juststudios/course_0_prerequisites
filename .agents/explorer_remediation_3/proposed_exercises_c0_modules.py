"""exercises_c0_modules.py - Practical Coding Exercises for Course 0 Modules.

Student Exercise Workbook:
- Fill in the `# TODO` sections and replace `raise NotImplementedError` stubs.
- To verify your implementations, run: python3 course_0_prerequisites/exercises/exercises_c0_modules.py
- Complete reference implementations are in: course_0_prerequisites/solutions/solutions_c0_modules.py
"""

from typing import List, Dict, Any, Optional
import math
import re


# Exercise 1: Safe AST Calculator (Module 01 & 09)
def student_safe_add(a: float, b: float) -> float:
    """Exercise 1.1: Return the sum of two numbers."""
    # TODO: Implement safe addition of two floating-point numbers
    raise NotImplementedError("Exercise 1.1: student_safe_add not implemented")


# Exercise 2: Dunder representation (Module 02)
class StudentAgentMessage:
    """Exercise 2.1: Implement __repr__ and __str__."""
    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        # TODO: Return formal representation: StudentAgentMessage(role='...', content='...')
        raise NotImplementedError("Exercise 2.1: StudentAgentMessage.__repr__ not implemented")

    def __str__(self) -> str:
        # TODO: Return user-facing string representation: [ROLE]: content (with role in uppercase)
        raise NotImplementedError("Exercise 2.1: StudentAgentMessage.__str__ not implemented")


# Exercise 3: Code fence stripper (Module 07)
def student_strip_fences(text: str) -> str:
    """Exercise 7.1: Extract JSON from markdown backticks."""
    # TODO: Extract raw JSON content from markdown code fences (```json ... ``` or ``` ... ```),
    # or isolate the outermost balanced curly braces { ... }
    raise NotImplementedError("Exercise 7.1: student_strip_fences not implemented")


# Exercise 4: Cosine similarity (Module 15)
def student_cosine_similarity(u: List[float], v: List[float]) -> float:
    """Exercise 15.1: Calculate cosine similarity between two vectors."""
    # TODO: Compute cosine similarity = (u . v) / (||u|| * ||v||)
    # Return 0.0 if either norm is zero.
    raise NotImplementedError("Exercise 15.1: student_cosine_similarity not implemented")


# Exercise 5: Softmax with temperature (Module 15)
def student_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
    """Exercise 15.2: Calculate numerically stable softmax with temperature."""
    # TODO: Calculate numerically stable softmax with temperature scaling:
    # 1. Clamp temperature to minimum 1e-4 to avoid division by zero.
    # 2. Scale logits: scaled = [z / t for z in logits].
    # 3. Shift by max(scaled) for numerical stability.
    # 4. Compute exponentials and return normalized probability distribution.
    raise NotImplementedError("Exercise 15.2: student_softmax not implemented")


def test_student_exercises() -> None:
    """Test suite for students to verify their implementations once completed."""
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

    print("All student exercise validation checks passed successfully!")


if __name__ == "__main__":
    print("=== Course 0 Student Exercises Workbook ===")
    print("Complete all # TODO items across the 5 exercises above.")
    print("For reference solutions, run: python3 course_0_prerequisites/solutions/solutions_c0_modules.py\n")
    try:
        test_student_exercises()
    except NotImplementedError as exc:
        print(f"[PENDING IMPLEMENTATION] {exc}")
        print("Keep going! Implement each TODO stub to pass the verification suite.")
