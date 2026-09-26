"""
Module 04: Operators — Reference Solutions
==========================================
Complete, verified implementations for all four exercise tiers.
"""

from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def eval_operator_expressions() -> Dict[str, Any]:
    """
    Evaluates requested expressions with exact arithmetic and logical rules.
    """
    return {
        "div_true": 15 / 4,          # 3.75
        "div_floor_pos": 15 // 4,    # 3
        "div_floor_neg": -15 // 4,   # -4
        "mod_pos": 15 % 4,           # 3
        "mod_neg": -15 % 4,          # 1
        "short_circuit_or": "" or "default",     # "default"
        "short_circuit_and": 0 and "never",      # 0
        "chained_comp": 10 <= 20 <= 30,          # True
        "bitwise_and": 6 & 3,                    # 2
        "bitwise_shift": 1 << 4,                 # 16
    }


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def calculate_token_allowance(
    total_budget: int,
    num_agents: int,
    reserved_pct: float
) -> Dict[str, int]:
    """
    Distributes token budget evenly among active agents using arithmetic operators.
    """
    if num_agents <= 0:
        raise ValueError("num_agents must be positive")
    if not (0.0 <= reserved_pct < 1.0):
        raise ValueError("reserved_pct must be between 0.0 and 1.0")
    if total_budget < 0:
        raise ValueError("total_budget cannot be negative")

    reserved_tokens = int(total_budget * reserved_pct)
    distributable = total_budget - reserved_tokens
    tokens_per_agent = distributable // num_agents
    leftover_tokens = distributable % num_agents

    return {
        "reserved": reserved_tokens,
        "distributable": distributable,
        "per_agent": tokens_per_agent,
        "leftover": leftover_tokens,
    }


# =====================================================================
# Level 3: Build Solution
# =====================================================================
class PermissionEngine:
    """
    Bitwise role-based access control engine.
    """
    PERM_READ = 1 << 0     # 1
    PERM_WRITE = 1 << 1    # 2
    PERM_EXECUTE = 1 << 2  # 4
    PERM_NETWORK = 1 << 3  # 8
    PERM_ADMIN = 1 << 4    # 16

    @staticmethod
    def grant(current_mask: int, *perms: int) -> int:
        """Grants permissions using bitwise OR."""
        mask = current_mask
        for p in perms:
            mask |= p
        return mask

    @staticmethod
    def revoke(current_mask: int, *perms: int) -> int:
        """Revokes permissions using bitwise AND and NOT."""
        mask = current_mask
        for p in perms:
            mask &= ~p
        return mask

    @staticmethod
    def has_all(current_mask: int, *perms: int) -> bool:
        """Checks if current_mask possesses all specified permissions."""
        if not perms:
            return True
        for p in perms:
            if (current_mask & p) != p:
                return False
        return True

    @staticmethod
    def has_any(current_mask: int, *perms: int) -> bool:
        """Checks if current_mask possesses at least one of the specified permissions."""
        if not perms:
            return False
        for p in perms:
            if (current_mask & p) != 0:
                return True
        return False


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def validate_agent_transition(
    agent_state: Dict[str, Any],
    action: Dict[str, Any]
) -> bool:
    """
    Validates whether an agent state transition is authorized and safe.
    """
    # 1. Agent must not be locked
    if agent_state.get("is_locked", False):
        return False

    # 2. Authorization check
    is_admin = bool(agent_state.get("is_admin", False))
    risk = float(action.get("risk", 1.0))
    confidence = float(agent_state.get("confidence", 0.0))

    is_authorized = is_admin or (risk < 0.8 and confidence >= 0.7)
    if not is_authorized:
        return False

    # 3. Network check if required
    if action.get("requires_network", False):
        if not agent_state.get("has_network", False):
            return False

    return True


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    evals = eval_operator_expressions()
    assert evals["div_true"] == 3.75
    assert evals["div_floor_pos"] == 3
    assert evals["div_floor_neg"] == -4
    assert evals["mod_pos"] == 3
    assert evals["mod_neg"] == 1
    assert evals["short_circuit_or"] == "default"
    assert evals["short_circuit_and"] == 0
    assert evals["chained_comp"] is True
    assert evals["bitwise_and"] == 2
    assert evals["bitwise_shift"] == 16

    # Test Level 2
    allowance = calculate_token_allowance(10000, 3, 0.10)
    assert allowance["reserved"] == 1000
    assert allowance["distributable"] == 9000
    assert allowance["per_agent"] == 3000
    assert allowance["leftover"] == 0

    allowance2 = calculate_token_allowance(100, 3, 0.25)
    assert allowance2["reserved"] == 25
    assert allowance2["distributable"] == 75
    assert allowance2["per_agent"] == 25
    assert allowance2["leftover"] == 0

    try:
        calculate_token_allowance(1000, 0, 0.1)
        assert False, "Should raise ValueError on 0 agents"
    except ValueError:
        pass

    try:
        calculate_token_allowance(1000, 2, 1.5)
        assert False, "Should raise ValueError on invalid pct"
    except ValueError:
        pass

    # Test Level 3
    engine = PermissionEngine()
    mask = 0
    mask = engine.grant(mask, PermissionEngine.PERM_READ, PermissionEngine.PERM_WRITE)
    assert mask == 3
    assert engine.has_all(mask, PermissionEngine.PERM_READ) is True
    assert engine.has_all(mask, PermissionEngine.PERM_READ, PermissionEngine.PERM_WRITE) is True
    assert engine.has_all(mask, PermissionEngine.PERM_READ, PermissionEngine.PERM_EXECUTE) is False
    assert engine.has_any(mask, PermissionEngine.PERM_EXECUTE, PermissionEngine.PERM_READ) is True
    assert engine.has_any(mask, PermissionEngine.PERM_EXECUTE, PermissionEngine.PERM_ADMIN) is False

    mask = engine.revoke(mask, PermissionEngine.PERM_WRITE)
    assert mask == PermissionEngine.PERM_READ
    assert engine.has_all(mask, PermissionEngine.PERM_WRITE) is False

    # Test Level 4
    admin_state = {"is_locked": False, "is_admin": True, "confidence": 0.5, "has_network": True}
    dangerous_act = {"risk": 0.95, "requires_network": True}
    assert validate_agent_transition(admin_state, dangerous_act) is True

    locked_admin = {"is_locked": True, "is_admin": True, "confidence": 0.99, "has_network": True}
    assert validate_agent_transition(locked_admin, dangerous_act) is False

    standard_agent = {"is_locked": False, "is_admin": False, "confidence": 0.85, "has_network": False}
    low_risk_act = {"risk": 0.4, "requires_network": False}
    assert validate_agent_transition(standard_agent, low_risk_act) is True

    high_risk_act = {"risk": 0.85, "requires_network": False}
    assert validate_agent_transition(standard_agent, high_risk_act) is False

    net_act = {"risk": 0.2, "requires_network": True}
    assert validate_agent_transition(standard_agent, net_act) is False

    print("Module 04: All Level 1-4 solutions verified successfully!")
