"""exercises_c0_modules.py - Practical Coding Exercises for Course 0 Modules.

Student exercise workbook containing problem stubs with TODO markers.
Reference solutions are located in ../solutions/solutions_c0_modules.py.
"""

from typing import List, Dict, Any, Optional
import math
import re


# Exercise 1: Safe AST Calculator (Module 01 & 09)
def student_safe_add(a: float, b: float) -> float:
    """Exercise 1.1: Return the sum of two numbers.

    TODO: Implement safe numeric addition returning a float.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 1.1 (student_safe_add) not yet implemented by student.")


# Exercise 2: Dunder representation (Module 02)
class StudentAgentMessage:
    """Exercise 2.1: Implement __repr__ and __str__ for Agent Message."""

    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        # TODO: Implement unambiguous developer representation: StudentAgentMessage(role='...', content='...')
        raise NotImplementedError("Exercise 2.1 (__repr__) not yet implemented by student.")

    def __str__(self) -> str:
        # TODO: Implement clean user-facing prompt representation: [ROLE]: content
        raise NotImplementedError("Exercise 2.1 (__str__) not yet implemented by student.")


# Exercise 3: Code fence stripper (Module 07)
def student_strip_fences(text: str) -> str:
    """Exercise 7.1: Extract JSON from markdown backticks.

    TODO: Extract JSON substring from markdown backticks (```json ... ``` or ``` ... ```)
    or find the outer matching braces { ... }. Return original string if no fence/braces found.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 7.1 (student_strip_fences) not yet implemented by student.")


# Exercise 4: Cosine similarity (Module 15)
def student_cosine_similarity(u: List[float], v: List[float]) -> float:
    """Exercise 15.1: Calculate cosine similarity between two vectors.

    TODO: Compute the dot product and Euclidean L2 norms of vectors u and v.
    Return dot / (norm_u * norm_v), or 0.0 if either vector has norm 0.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 15.1 (student_cosine_similarity) not yet implemented by student.")


# Exercise 5: Softmax with temperature (Module 15)
def student_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
    """Exercise 15.2: Calculate numerically stable softmax with temperature.

    TODO: Scale logits by max(1e-4, temp), subtract maximum logit for stability,
    compute exp(z_scaled), and normalize by the sum of exponentials.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 15.2 (student_softmax) not yet implemented by student.")


def test_student_exercises() -> None:
    """Unit test suite for student to verify their implementations once completed."""
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
    try:
        test_student_exercises()
    except NotImplementedError as exc:
        print(f"[EXERCISE WORKBOOK] Unimplemented exercise stub encountered: {exc}")
        print("Please implement all # TODO stubs above, or run reference solutions:")
        print("  python3 course_0_prerequisites/solutions/solutions_c0_modules.py")
