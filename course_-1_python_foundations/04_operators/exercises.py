"""
Module 04: Operators — Exercises
=================================
Complete each of the four levels below.
Each level exercises your understanding of arithmetic, comparison, logical,
and bitwise operators, including precedence and short-circuit evaluation.
"""

from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
def eval_operator_expressions() -> Dict[str, Any]:
    """
    Recall Exercise:
    Evaluate the following expressions mentally or in Python and return
    a dictionary containing their exact evaluated values:

    Keys to return:
        - "div_true": result of `15 / 4`
        - "div_floor_pos": result of `15 // 4`
        - "div_floor_neg": result of `-15 // 4`
        - "mod_pos": result of `15 % 4`
        - "mod_neg": result of `-15 % 4`
        - "short_circuit_or": result of `"" or "default"`
        - "short_circuit_and": result of `0 and "never"`
        - "chained_comp": result of `(10 <= 20 <= 30)`
        - "bitwise_and": result of `6 & 3`
        - "bitwise_shift": result of `1 << 4`

    # TODO: Return dictionary with the exact evaluated results.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 1: Implement eval_operator_expressions().")


# =====================================================================
# Level 2: Modify
# =====================================================================
def calculate_token_allowance(
    total_budget: int,
    num_agents: int,
    reserved_pct: float
) -> Dict[str, int]:
    """
    Modify Exercise:
    Distribute a total token budget evenly among multiple active subagents.

    Requirements:
    1. Validate inputs:
       - If `num_agents <= 0`: raise ValueError("num_agents must be positive")
       - If not `(0.0 <= reserved_pct < 1.0)`: raise ValueError("reserved_pct must be between 0.0 and 1.0")
       - If `total_budget < 0`: raise ValueError("total_budget cannot be negative")
    2. Compute reserved emergency tokens:
       - `reserved_tokens = int(total_budget * reserved_pct)`
    3. Compute distributable tokens:
       - `distributable = total_budget - reserved_tokens`
    4. Compute equal allocation per agent using floor division:
       - `tokens_per_agent = distributable // num_agents`
    5. Compute leftover remainder tokens:
       - `leftover_tokens = distributable % num_agents`
    6. Return a dictionary with:
       {
           "reserved": reserved_tokens,
           "distributable": distributable,
           "per_agent": tokens_per_agent,
           "leftover": leftover_tokens
       }

    # TODO: Implement token allowance calculations using arithmetic operators.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement calculate_token_allowance().")


# =====================================================================
# Level 3: Build
# =====================================================================
class PermissionEngine:
    """
    Build Exercise:
    Implement a bitwise permission management system for AI tool capabilities.

    Permission Bit Constants:
        READ    = 1 << 0  (1)
        WRITE   = 1 << 1  (2)
        EXECUTE = 1 << 2  (4)
        NETWORK = 1 << 3  (8)
        ADMIN   = 1 << 4  (16)

    Implement the four methods below using bitwise operations:
    """
    PERM_READ = 1 << 0
    PERM_WRITE = 1 << 1
    PERM_EXECUTE = 1 << 2
    PERM_NETWORK = 1 << 3
    PERM_ADMIN = 1 << 4

    @staticmethod
    def grant(current_mask: int, *perms: int) -> int:
        """
        Grants (sets) one or more permissions in the mask using bitwise OR.
        # TODO: Implement grant using bitwise operations.
        """
        # TODO: Replace the line below with your implementation
        raise NotImplementedError("Level 3: Implement PermissionEngine.grant().")

    @staticmethod
    def revoke(current_mask: int, *perms: int) -> int:
        """
        Revokes (clears) one or more permissions in the mask using bitwise AND and NOT.
        # TODO: Implement revoke using bitwise operations.
        """
        # TODO: Replace the line below with your implementation
        raise NotImplementedError("Level 3: Implement PermissionEngine.revoke().")

    @staticmethod
    def has_all(current_mask: int, *perms: int) -> bool:
        """
        Returns True if current_mask possesses ALL specified permissions.
        # TODO: Implement has_all using bitwise operations.
        """
        # TODO: Replace the line below with your implementation
        raise NotImplementedError("Level 3: Implement PermissionEngine.has_all().")

    @staticmethod
    def has_any(current_mask: int, *perms: int) -> bool:
        """
        Returns True if current_mask possesses AT LEAST ONE of the specified permissions.
        # TODO: Implement has_any using bitwise operations.
        """
        # TODO: Replace the line below with your implementation
        raise NotImplementedError("Level 3: Implement PermissionEngine.has_any().")


# =====================================================================
# Level 4: Debug
# =====================================================================
def validate_agent_transition(
    agent_state: Dict[str, Any],
    action: Dict[str, Any]
) -> bool:
    """
    Debug Exercise:
    Validates whether an agent state transition is authorized and safe.

    The correct business logic requires:
    1. The agent must NOT be locked (`agent_state["is_locked"] is False`).
    2. The action must be authorized:
       - Either the agent is an administrator (`agent_state.get("is_admin", False) is True`),
       - OR the action's risk score is strictly below 0.8 AND the agent's confidence score
         is at least 0.7 (`action["risk"] < 0.8 and agent_state["confidence"] >= 0.7`).
    3. If `action.get("requires_network", False)` is True:
       - The agent MUST have network permission (`agent_state.get("has_network", False) is True`).

    The buggy implementation below contains operator precedence errors,
    missing parentheses, and flawed short-circuiting:
        # BUG: Missing parentheses around (is_admin or (risk < 0.8 and conf >= 0.7))
        # causing not is_locked to interact improperly with or!
        # BUG: Network check fails to guard properly when requires_network is True!
        return not agent_state["is_locked"] and agent_state.get("is_admin", False) or \
               action["risk"] < 0.8 and agent_state["confidence"] >= 0.7 and \
               agent_state.get("has_network", False)

    # TODO: Fix the bugs using explicit parentheses and proper logical operators.
    """
    # TODO: Replace the line below with your fixed implementation
    raise NotImplementedError("Level 4: Fix validate_agent_transition().")


if __name__ == "__main__":
    print("Module 04 Exercises loaded successfully.")
    print("Implement the functions above or run solutions.py to verify.")
