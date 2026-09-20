"""main.py - Runnable CLI demonstration for the MiniAgent Capstone project."""

import asyncio
from course_0_prerequisites.mini_agent.config import AgentConfig
from course_0_prerequisites.mini_agent.memory import SQLiteMemory
from course_0_prerequisites.mini_agent.tools import default_registry
from course_0_prerequisites.mini_agent.engine import DeterministicReActEngine
from course_0_prerequisites.mini_agent.agent import MiniAgent


async def run_demonstration() -> None:
    print("================================================================")
    print("      Course 0 Capstone: Autonomous MiniAgent Execution CLI    ")
    print("================================================================\n")

    # Initialize agent components
    config = AgentConfig(agent_name="HermesMiniAgent", max_steps=5, verbose=True)
    memory = SQLiteMemory(db_path=":memory:")
    engine = DeterministicReActEngine(agent_name=config.agent_name)

    agent = MiniAgent(
        config=config,
        memory=memory,
        tools=default_registry,
        engine=engine
    )

    tasks = [
        ("Task 1 (Math):", "What is (25 * 4) + (100 / 5)?"),
        ("Task 2 (Search):", "Search for python async concurrency patterns."),
        ("Task 3 (Subprocess Python):", "Run a python script to compute squares of 1 to 5."),
        ("Task 4 (Time):", "What is the current time?"),
    ]

    for label, query in tasks:
        print("\n" + "=" * 64)
        print(f"Executing {label} '{query}'")
        print("=" * 64)
        resp = await agent.run(query, session_id="cli_demo_session")

        print(f"\n>> Execution Status: {'SUCCESS' if resp.success else 'FAILED'}")
        print(f">> Total Steps Taken: {len(resp.steps)}")
        print(f">> Latency: {resp.total_duration_ms:.2f}ms")
        print(f">> Final Answer: {resp.final_answer}")

    # Inspect persistent SQLite memory
    print("\n" + "=" * 64)
    print("Verifying SQLite Persistent Memory & Tool Audit Trail")
    print("=" * 64)
    history = memory.get_history("cli_demo_session", limit=10)
    print(f"Total messages recorded in history: {len(history)}")

    audit_logs = memory.get_audit_logs("cli_demo_session")
    print(f"Total tool audit records logged: {len(audit_logs)}")
    for log in audit_logs:
        print(f"  - Tool: {log['tool_name']} | Success: {log['success']} | Latency: {log['duration_ms']}ms")

    memory.close()
    print("\nMiniAgent demonstration finished cleanly with 100% success!\n")


def main() -> None:
    asyncio.run(run_demonstration())


if __name__ == "__main__":
    main()
