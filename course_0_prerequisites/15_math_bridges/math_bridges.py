"""math_bridges.py - Demonstrates Softmax temperature scaling, gradient descent step, and expected value utility.

Key concepts demonstrated:
1. Numerically stable Softmax with temperature scaling (T -> 0 vs T >> 1).
2. Gradient descent weight update formula (w = w - eta * grad).
3. Expected value utility calculation for agent decision tree planning.
"""

from typing import List, Dict, Any
import math


def softmax_with_temperature(logits: List[float], temperature: float = 1.0) -> List[float]:
    """Computes the softmax probability distribution with temperature scaling.

    Args:
        logits: Unnormalized logit values from model output.
        temperature: Scaling factor T > 0.
    """
    # Guard against division by zero
    t = max(1e-4, temperature)
    scaled_logits = [z / t for z in logits]

    # Subtract max for numerical stability (prevents exp overflow)
    max_val = max(scaled_logits)
    exp_values = [math.exp(z - max_val) for z in scaled_logits]
    sum_exp = sum(exp_values)

    return [ev / sum_exp for ev in exp_values]


def gradient_descent_step(current_weight: float, loss_gradient: float, learning_rate: float = 0.01) -> float:
    """Calculates one optimization step: w_new = w_old - (eta * dL/dw)."""
    return current_weight - (learning_rate * loss_gradient)


def calculate_plan_expected_utility(plan_branches: List[Dict[str, float]]) -> float:
    """Calculates the expected utility of an action trajectory.

    Formula: E[U] = sum( P(outcome) * Utility(outcome) )
    """
    total_expected = 0.0
    for branch in plan_branches:
        prob = branch["probability"]
        utility = branch["utility"]
        total_expected += prob * utility
    return total_expected


def main() -> None:
    print("=== Module 15: Math Bridges (Softmax, Gradients, Expected Value) Demo ===")

    # 1. Softmax with Temperature Scaling
    # Logits for 3 tool options: [calculator (4.0), search (2.0), finish (1.0)]
    logits = [4.0, 2.0, 1.0]

    # At low temperature (T=0.1) -> Argmax-like determinism (essential for tool calling)
    probs_low_temp = softmax_with_temperature(logits, temperature=0.1)
    assert probs_low_temp[0] > 0.99, f"Expected >0.99 for top logit at T=0.1, got {probs_low_temp[0]}"
    print(f"[OK] Low Temperature (T=0.1) Determinism: {probs_low_temp}")

    # At standard temperature (T=1.0)
    probs_normal = softmax_with_temperature(logits, temperature=1.0)
    assert math.isclose(sum(probs_normal), 1.0)
    assert probs_normal[0] > probs_normal[1] > probs_normal[2]
    print(f"[OK] Normal Temperature (T=1.0): {probs_normal}")

    # At high temperature (T=10.0) -> High entropy, uniform exploration
    probs_high_temp = softmax_with_temperature(logits, temperature=10.0)
    assert all(p > 0.25 for p in probs_high_temp)
    print(f"[OK] High Temperature (T=10.0) Exploration: {probs_high_temp}")

    # 2. Gradient Descent Step
    w = 5.0
    grad = 2.0  # Slope is positive, so stepping down requires reducing w
    w_new = gradient_descent_step(w, grad, learning_rate=0.1)
    assert w_new == 4.8
    print(f"[OK] Gradient descent step: w={w}, grad={grad}, lr=0.1 -> w_new={w_new}")

    # 3. Expected Value in Planning
    # Plan A: High reward, medium risk
    plan_a_outcomes = [
        {"probability": 0.8, "utility": 100.0},  # 80% success
        {"probability": 0.2, "utility": -50.0},  # 20% failure penalty
    ]
    # Plan B: Safe, low reward
    plan_b_outcomes = [
        {"probability": 0.98, "utility": 40.0},  # 98% success
        {"probability": 0.02, "utility": -10.0},
    ]

    ev_a = calculate_plan_expected_utility(plan_a_outcomes)
    ev_b = calculate_plan_expected_utility(plan_b_outcomes)

    # EV(A) = 0.8*100 + 0.2*(-50) = 80 - 10 = 70.0
    # EV(B) = 0.98*40 + 0.02*(-10) = 39.2 - 0.2 = 39.0
    assert math.isclose(ev_a, 70.0)
    assert math.isclose(ev_b, 39.0)
    print(f"[OK] Expected Utility calculated: Plan A = {ev_a:.1f}, Plan B = {ev_b:.1f}")
    assert ev_a > ev_b, "Plan A has higher expected value"

    print("All tests in math_bridges.py passed successfully!\n")


if __name__ == "__main__":
    main()
