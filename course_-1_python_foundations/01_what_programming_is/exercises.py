"""
Module 01: What Programming Is — Exercises
===========================================
Complete each of the four levels below.
Each level exercises your understanding of sequential execution, state, and instructions.
"""

from typing import List, Tuple, Dict, Any


# =====================================================================
# Level 1: Recall
# =====================================================================
def predict_final_state() -> Dict[str, int]:
    """
    Mental Simulation / Recall Exercise:
    Trace the following instructions step-by-step:
        a = 5
        b = 10
        a = a + b      # a is now 15
        b = a - 3      # b is now 12
        a = a * 2      # a is now 30
        b = b + 1      # b is now 13

    # TODO: Return a dictionary with the exact final values: {"a": ..., "b": ...}
    """
    # TODO: Replace the line below with your answer
    raise NotImplementedError("Level 1: Complete predict_final_state() with final values of a and b.")


# =====================================================================
# Level 2: Modify
# =====================================================================
def update_inventory(current_stock: int, items_sold: int, items_received: int, items_damaged: int) -> int:
    """
    Sequential State Modification:
    Given a starting warehouse inventory, apply transactions in order:
    1. Subtract items sold.
    2. Add newly received items.
    3. Subtract damaged items.
    4. Guard against negative inventory: if the resulting stock is less than 0, set it to 0.

    # TODO: Implement the sequential inventory calculations.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement update_inventory() with proper sequential state tracking.")


# =====================================================================
# Level 3: Build
# =====================================================================
def run_accumulator(instructions: List[Tuple[str, int]]) -> int:
    """
    Build a Mini Instruction Interpreter:
    Accepts a list of (operation, value) tuples and evaluates them sequentially
    starting from an initial accumulator value of 0.

    Supported operations:
        - ("ADD", n)   -> accumulator = accumulator + n
        - ("SUB", n)   -> accumulator = accumulator - n
        - ("MUL", n)   -> accumulator = accumulator * n
        - ("RESET", n) -> accumulator = n

    Returns the final integer accumulator value.

    # TODO: Implement the instruction execution loop.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement run_accumulator() processing all instruction tuples.")


# =====================================================================
# Level 4: Debug
# =====================================================================
def calculate_agent_fuel(
    starting_fuel: float,
    burn_per_km: float,
    distance_km: float,
    booster_fuel: float
) -> float:
    """
    Debugging Exercise:
    An autonomous rover plans its trip. The expected logic is:
      1. Compute fuel burned: distance_km * burn_per_km
      2. Compute net fuel after travel: starting_fuel - fuel_burned
      3. Add emergency booster fuel to net fuel: net_fuel + booster_fuel
      4. If remaining fuel is negative, return 0.0, else return remaining fuel.

    The buggy implementation below contains order-of-operation and sign errors:
        # BUG: It adds distance instead of multiplying by burn rate
        # BUG: It subtracts the booster instead of adding it
        fuel_burned = distance_km + burn_per_km
        remaining = starting_fuel - fuel_burned - booster_fuel
        return remaining

    # TODO: Fix the bugs so this function calculates remaining fuel accurately.
    """
    # TODO: Fix the buggy logic and return the correct remaining fuel
    raise NotImplementedError("Level 4: Fix bugs in calculate_agent_fuel().")


if __name__ == "__main__":
    print("Module 01 Exercises loaded successfully.")
    print("To test your solutions, implement the functions above or run solutions.py.")
