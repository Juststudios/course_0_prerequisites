"""
Module 01: What Programming Is — Reference Solutions
=====================================================
Clean, working implementations for all four exercise tiers.
"""

from typing import List, Tuple, Dict, Any


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def predict_final_state() -> Dict[str, int]:
    """
    Step-by-step trace:
        a = 5
        b = 10
        a = 5 + 10 = 15
        b = 15 - 3 = 12
        a = 15 * 2 = 30
        b = 12 + 1 = 13
    """
    return {"a": 30, "b": 13}


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def update_inventory(current_stock: int, items_sold: int, items_received: int, items_damaged: int) -> int:
    """
    Calculates stock transitions sequentially with a non-negative floor.
    """
    stock = current_stock - items_sold
    stock = stock + items_received
    stock = stock - items_damaged
    if stock < 0:
        stock = 0
    return stock


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def run_accumulator(instructions: List[Tuple[str, int]]) -> int:
    """
    Evaluates sequential arithmetic instructions starting from accumulator = 0.
    """
    accumulator = 0
    for op, val in instructions:
        if op == "ADD":
            accumulator += val
        elif op == "SUB":
            accumulator -= val
        elif op == "MUL":
            accumulator *= val
        elif op == "RESET":
            accumulator = val
        else:
            raise ValueError(f"Unknown instruction operation: {op}")
    return accumulator


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def calculate_agent_fuel(
    starting_fuel: float,
    burn_per_km: float,
    distance_km: float,
    booster_fuel: float
) -> float:
    """
    Calculates net remaining fuel correctly after consumption and boost.
    """
    fuel_burned = distance_km * burn_per_km
    remaining = (starting_fuel - fuel_burned) + booster_fuel
    if remaining < 0.0:
        return 0.0
    return remaining


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    state = predict_final_state()
    assert state == {"a": 30, "b": 13}, f"Level 1 failed: {state}"

    # Test Level 2
    stock = update_inventory(100, 20, 50, 10)
    assert stock == 120, f"Level 2 failed: expected 120, got {stock}"
    depleted = update_inventory(10, 50, 5, 2)
    assert depleted == 0, f"Level 2 floor failed: expected 0, got {depleted}"

    # Test Level 3
    test_instructions = [
        ("ADD", 10),
        ("MUL", 3),
        ("SUB", 5),
        ("RESET", 100),
        ("ADD", 25),
    ]
    acc_res = run_accumulator(test_instructions)
    assert acc_res == 125, f"Level 3 failed: expected 125, got {acc_res}"

    # Test Level 4
    fuel_res = calculate_agent_fuel(100.0, 0.5, 40.0, 15.0)
    # burned = 20.0, net = 80.0, boost = 15.0 -> 95.0
    assert abs(fuel_res - 95.0) < 1e-6, f"Level 4 failed: expected 95.0, got {fuel_res}"

    exhausted = calculate_agent_fuel(10.0, 2.0, 20.0, 5.0)
    # burned = 40.0, net = -30.0 + 5.0 = -25.0 -> floor 0.0
    assert exhausted == 0.0, f"Level 4 floor failed: expected 0.0, got {exhausted}"

    print("Module 01: All Level 1-4 solutions verified successfully!")
