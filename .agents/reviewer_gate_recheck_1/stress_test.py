import sys
import math
import pytest

from course_0_prerequisites.exercises.exercises_c0_modules import (
    student_safe_add,
    StudentAgentMessage,
    student_strip_fences,
    student_cosine_similarity,
    student_softmax,
)

from course_0_prerequisites.solutions.solutions_c0_modules import (
    solution_safe_add,
    SolutionAgentMessage,
    solution_strip_fences,
    solution_cosine_similarity,
    solution_softmax,
)

print("=== 1. Stress-testing Student Exercises (Must raise NotImplementedError) ===")
# Exercise 1.1
try:
    student_safe_add(1.0, 2.0)
    assert False, "student_safe_add did not raise NotImplementedError!"
except NotImplementedError as e:
    print(f"PASS: student_safe_add -> {e}")

# Exercise 2.1
msg = StudentAgentMessage("user", "test")
try:
    repr(msg)
    assert False, "StudentAgentMessage.__repr__ did not raise NotImplementedError!"
except NotImplementedError as e:
    print(f"PASS: StudentAgentMessage.__repr__ -> {e}")

try:
    str(msg)
    assert False, "StudentAgentMessage.__str__ did not raise NotImplementedError!"
except NotImplementedError as e:
    print(f"PASS: StudentAgentMessage.__str__ -> {e}")

# Exercise 7.1
try:
    student_strip_fences("```json {} ```")
    assert False, "student_strip_fences did not raise NotImplementedError!"
except NotImplementedError as e:
    print(f"PASS: student_strip_fences -> {e}")

# Exercise 15.1
try:
    student_cosine_similarity([1.0, 0.0], [1.0, 0.0])
    assert False, "student_cosine_similarity did not raise NotImplementedError!"
except NotImplementedError as e:
    print(f"PASS: student_cosine_similarity -> {e}")

# Exercise 15.2
try:
    student_softmax([1.0, 2.0])
    assert False, "student_softmax did not raise NotImplementedError!"
except NotImplementedError as e:
    print(f"PASS: student_softmax -> {e}")


print("\n=== 2. Stress-testing Reference Solutions (Edge cases & numerical stability) ===")

# Safe add edge cases
assert solution_safe_add(0.0, 0.0) == 0.0
assert solution_safe_add(-100.5, 100.5) == 0.0
print("PASS: solution_safe_add boundaries")

# Dunder edge cases
m = SolutionAgentMessage("SYSTEM", "alert")
assert str(m) == "[SYSTEM]: alert"
assert "role='SYSTEM'" in repr(m)
print("PASS: SolutionAgentMessage dunders")

# Strip fences edge cases
assert solution_strip_fences("") == ""
assert solution_strip_fences("No fences here") == "No fences here"
assert solution_strip_fences("```json\n{\"a\": 1}\n```") == '{"a": 1}'
assert solution_strip_fences("```\n{\"b\": 2}\n```") == '{"b": 2}'
assert solution_strip_fences("Prefix { \"c\": 3 } Suffix") == '{ \"c\": 3 }'
print("PASS: solution_strip_fences edge cases")

# Cosine similarity edge cases
# Zero norm vectors must return 0.0 without ZeroDivisionError
assert solution_cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0
assert solution_cosine_similarity([1.0, 1.0], [0.0, 0.0]) == 0.0
assert solution_cosine_similarity([0.0, 0.0], [0.0, 0.0]) == 0.0
# Opposite vectors
assert math.isclose(solution_cosine_similarity([1.0, 0.0], [-1.0, 0.0]), -1.0)
# Orthogonal vectors
assert math.isclose(solution_cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)
print("PASS: solution_cosine_similarity zero-norm and orthogonality")

# Softmax edge cases
# Extreme logits (numerical overflow test)
extreme_probs = solution_softmax([1000.0, 1000.0, 1000.0], temp=1.0)
assert len(extreme_probs) == 3
for p in extreme_probs:
    assert math.isclose(p, 1.0 / 3.0, rel_tol=1e-5)
assert math.isclose(sum(extreme_probs), 1.0)

# Low/zero temperature test (clamp to 1e-4)
sharp_probs = solution_softmax([10.0, 5.0, 1.0], temp=0.0)
assert sharp_probs[0] > 0.999
assert math.isclose(sum(sharp_probs), 1.0)

# Negative temperature clamp test
neg_probs = solution_softmax([10.0, 5.0, 1.0], temp=-0.5)
assert neg_probs[0] > 0.999
assert math.isclose(sum(neg_probs), 1.0)

print("PASS: solution_softmax numerical stability, extreme logits, and temperature clamp")

print("\nALL ADVERSARIAL STRESS TESTS PASSED CLEANLY!")
