"""tenant_isolation.py - Demonstrates multi-tenant isolation under high concurrency with ContextVars.

Key concepts demonstrated:
1. Concurrently executing multiple agent sessions on a single event loop.
2. Proving zero cross-talk or context bleeding between tenants.
3. Nested asynchronous context assertions.
"""

import asyncio
import contextvars
import random
from typing import Dict, List, Tuple

# Context variables for tenant and request identification
tenant_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("tenant_id_var", default="public")
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id_var", default="req_none")


async def simulated_tool_execution(tool_name: str, expected_tenant: str, expected_request: str) -> None:
    """A simulated tool asserting that current context matches expected caller identity."""
    # Introduce random async suspension to maximize task interleaving
    await asyncio.sleep(random.uniform(0.01, 0.04))

    current_tenant = tenant_id_var.get()
    current_request = request_id_var.get()

    if current_tenant != expected_tenant:
        raise AssertionError(
            f"CRITICAL CONTEXT BLEED: Expected tenant '{expected_tenant}', but found '{current_tenant}'!"
        )
    if current_request != expected_request:
        raise AssertionError(
            f"CRITICAL CONTEXT BLEED: Expected request '{expected_request}', but found '{current_request}'!"
        )


async def execute_tenant_agent_session(tenant_id: str, request_id: str, steps: int = 3) -> Dict[str, Any]:
    """Runs a multi-step agent session bound to a specific tenant."""
    # Set context variables for this task
    t_token = tenant_id_var.set(tenant_id)
    r_token = request_id_var.set(request_id)

    tool_names = ["search_customer_db", "verify_permissions", "compute_analytics"]
    try:
        for step in range(steps):
            tool = tool_names[step % len(tool_names)]
            await simulated_tool_execution(tool, tenant_id, request_id)

        return {
            "tenant": tenant_id,
            "request_id": request_id,
            "steps_completed": steps,
            "isolated": True,
        }
    finally:
        tenant_id_var.reset(t_token)
        request_id_var.reset(r_token)


async def main() -> None:
    print("=== Module 05: Multi-Tenant Concurrency Isolation Demo ===")

    # Spawn 10 concurrent tenant requests
    tenants = [f"tenant_{i:02d}" for i in range(1, 11)]
    tasks = []

    for i, t in enumerate(tenants):
        req_id = f"req_{t}_{i*100}"
        tasks.append(execute_tenant_agent_session(t, req_id, steps=4))

    print(f"Launching {len(tasks)} concurrent multi-tenant agent sessions...")
    results = await asyncio.gather(*tasks)

    print(f"Successfully completed {len(results)} tenant sessions without collision.")
    for res in results:
        assert res["isolated"] is True
        assert res["steps_completed"] == 4

    # Verify root context remains intact
    assert tenant_id_var.get() == "public"
    assert request_id_var.get() == "req_none"

    print("[OK] All 10 tenants executed concurrently with 100% strict isolation.")
    print("All tests in tenant_isolation.py passed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
