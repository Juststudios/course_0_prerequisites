"""
Module 01: What Programming Is
===============================
This lesson provides a hands-on exploration of the foundational mental model
of computer programming: instructions, sequential execution, memory state,
determinism, and the transition from human thoughts to automated machine actions.

Run this script directly:
    python3 what_programming_is.py
"""

import sys
import time

print("=" * 70)
print("MODULE 01: WHAT PROGRAMMING IS — FOUNDATIONAL MENTAL MODELS")
print("=" * 70)

# -----------------------------------------------------------------------------
# Section 1: Sequential Execution — The Step-by-Step Nature of Code
# -----------------------------------------------------------------------------
# Computers are extraordinarily fast, but fundamentally simple-minded.
# By default, a program runs strictly from top to bottom, one statement at a time.
# Every statement modifies the program's "state" — the collection of values
# currently stored in the computer's memory (RAM).

print("\n--- [Section 1: Sequential Execution & State Evolution] ---")

# Step 1: Initialize an empty state
print("Step 1: Program starts. No variables defined yet.")
energy = 100
print(f"  -> State updated: energy = {energy}")

# Step 2: Perform an action that alters state
print("Step 2: Performing a physical action (walking 5 kilometers)...")
energy = energy - 20
print(f"  -> State updated: energy = {energy}")

# Step 3: Another action that alters state in a different way
print("Step 3: Eating an energy bar (+35 energy)...")
energy = energy + 35
print(f"  -> State updated: energy = {energy}")

# Step 4: Conditional inspection of current state
print("Step 4: Checking if the agent has enough energy to continue...")
can_continue = energy > 50
print(f"  -> Is energy > 50? {can_continue} (Current energy: {energy})")


# -----------------------------------------------------------------------------
# Section 2: Determinism — The Golden Rule of Software
# -----------------------------------------------------------------------------
# A fundamental property of computers is DETERMINISM.
# Given the identical starting inputs and the identical sequence of steps,
# a program will ALWAYS produce the exact same outcome. There is no magic,
# no mood, and no guesswork involved.

print("\n--- [Section 2: Determinism & Repeatability] ---")

def calculate_trajectory(initial_velocity, launch_angle_degrees, time_seconds):
    """
    Computes horizontal displacement using standard physics:
    x(t) = v0 * cos(theta) * t
    This pure mathematical function is 100% deterministic.
    """
    import math
    angle_radians = math.radians(launch_angle_degrees)
    horizontal_speed = initial_velocity * math.cos(angle_radians)
    distance = horizontal_speed * time_seconds
    return distance

# Run trial A and trial B with identical parameters
v0 = 50.0  # meters per second
angle = 45.0  # degrees
t = 3.5  # seconds

result_a = calculate_trajectory(v0, angle, t)
result_b = calculate_trajectory(v0, angle, t)

print(f"Trial A calculated distance: {result_a:.4f} meters")
print(f"Trial B calculated distance: {result_b:.4f} meters")
print(f"Are results strictly identical? {result_a == result_b}")


# -----------------------------------------------------------------------------
# Section 3: The Recipe Model vs The Reality of Execution
# -----------------------------------------------------------------------------
# In human recipes, vague instructions like "salt to taste" or "stir until soft"
# work because humans have common sense and biological sensors.
# Computers have NO common sense. Every instruction must be mathematically unambiguous.

print("\n--- [Section 3: Dissecting an Unambiguous Algorithm] ---")

# Let's trace an algorithm that counts positive numbers in a collection of data.
sensor_readings = [12, -4, 0, 45, -18, 99, -1, 33]
print(f"Raw sensor data: {sensor_readings}")

positive_count = 0
running_sum = 0

print("Tracing state transitions:")
for index, reading in enumerate(sensor_readings):
    previous_count = positive_count
    if reading > 0:
        positive_count = positive_count + 1
        running_sum = running_sum + reading
        action_note = f"ACCEPTED (+{reading})"
    else:
        action_note = f"IGNORED  ({reading} <= 0)"
    
    print(f"  Step {index}: reading={reading:>3} | {action_note:<18} | Count: {positive_count} | Sum: {running_sum}")

print(f"Final summary: Found {positive_count} positive readings totaling {running_sum}.")


# -----------------------------------------------------------------------------
# Section 4: A Minimal Virtual Instruction Machine (Interpreter Simulation)
# -----------------------------------------------------------------------------
# How does an interpreter like CPython actually work?
# At its heart, an interpreter is a loop that reads an instruction,
# decodes what operation to perform, executes it against a memory dictionary,
# and advances the instruction counter.
# Let's build a fully functioning mini-interpreter right here in Python!

print("\n--- [Section 4: Building a Mini Virtual Machine in 40 Lines] ---")

class MiniInterpreter:
    """
    Simulates a tiny central processing unit (CPU) with named registers (memory).
    Supports 5 primitive instructions:
      - SET: Store a value into a register
      - ADD: Add a value or register to a register
      - SUB: Subtract a value from a register
      - MULT: Multiply a register by a scalar
      - PRINT: Display current register state
    """
    def __init__(self):
        # The 'registers' dictionary represents our computer's RAM
        self.memory = {}
        self.execution_log = []

    def execute_program(self, program_instructions):
        print("MiniInterpreter: Booting execution engine...")
        for line_num, instruction in enumerate(program_instructions, start=1):
            op = instruction[0]
            args = instruction[1:]
            
            if op == "SET":
                reg, val = args
                self.memory[reg] = val
                self.execution_log.append(f"Line {line_num}: Set register '{reg}' to {val}")
            
            elif op == "ADD":
                reg, val = args
                self.memory[reg] = self.memory.get(reg, 0) + val
                self.execution_log.append(f"Line {line_num}: Added {val} to '{reg}' -> {self.memory[reg]}")

            elif op == "SUB":
                reg, val = args
                self.memory[reg] = self.memory.get(reg, 0) - val
                self.execution_log.append(f"Line {line_num}: Subtracted {val} from '{reg}' -> {self.memory[reg]}")

            elif op == "MULT":
                reg, factor = args
                self.memory[reg] = self.memory.get(reg, 0) * factor
                self.execution_log.append(f"Line {line_num}: Multiplied '{reg}' by {factor} -> {self.memory[reg]}")

            elif op == "PRINT":
                reg = args[0]
                val = self.memory.get(reg, "<UNDEFINED>")
                print(f"  [OUTPUT from VM]: Register '{reg}' = {val}")
                self.execution_log.append(f"Line {line_num}: Printed '{reg}' ({val})")

            else:
                raise ValueError(f"Unknown instruction: {op}")

        print("MiniInterpreter: Execution halted cleanly.")

# Now define a sequence of instructions (our custom 'source code')
mini_code = [
    ("SET", "base_price", 100),
    ("SET", "tax_rate", 5),
    ("ADD", "base_price", 20),      # Shipping fee: base_price becomes 120
    ("MULT", "base_price", 2),      # Buy 2 items: base_price becomes 240
    ("ADD", "base_price", 12),      # Sales tax: base_price becomes 252
    ("PRINT", "base_price"),        # Display final computed bill
]

vm = MiniInterpreter()
vm.execute_program(mini_code)

print("\nInternal execution log generated by the virtual machine:")
for entry in vm.execution_log:
    print(f"  {entry}")


# -----------------------------------------------------------------------------
# Section 5: The Connection to Autonomous AI Agents
# -----------------------------------------------------------------------------
# Why is understanding "What Programming Is" vital for AI Agent developers?
# An autonomous AI agent (like an LLM orchestrator) is NOT magic.
# When an agent "reasons":
# 1. It reads input (user prompt + current environment state).
# 2. It plans a sequence of deterministic steps (tool calls: search_web, read_file, run_command).
# 3. It executes the tools sequentially, capturing the outputs as new state.
# 4. It repeats until the goal state is achieved.

print("\n--- [Section 5: How AI Agents Model Instructions & State] ---")

class MockAgentRuntime:
    """Demonstrates how an AI Agent maintains memory and executes sequential actions."""
    def __init__(self, agent_name):
        self.name = agent_name
        self.state = {
            "status": "IDLE",
            "scratchpad": [],
            "tokens_used": 0,
            "tools_called": []
        }

    def log_thought(self, thought_text):
        self.state["scratchpad"].append(thought_text)
        self.state["tokens_used"] += len(thought_text.split())
        print(f"[{self.name} THOUGHT]: {thought_text}")

    def call_tool(self, tool_name, parameters):
        self.state["status"] = f"CALLING_{tool_name.upper()}"
        self.state["tools_called"].append((tool_name, parameters))
        print(f"[{self.name} ACTION]: Invoking tool '{tool_name}' with args {parameters}")
        
        # Simulate tool execution and state return
        if tool_name == "calculator":
            expr = parameters.get("expression", "0")
            result = eval(expr)  # Demonstration evaluation
            return result
        elif tool_name == "retrieve_user_profile":
            return {"user": "Alice", "balance": 450.0, "role": "admin"}
        return None

# Instantiate and run an agent task sequence
agent = MockAgentRuntime("Agent-Alpha")
agent.log_thought("The user wants to know their remaining balance after a $35 subscription.")
user_data = agent.call_tool("retrieve_user_profile", {"user_id": 101})

agent.log_thought(f"Retrieved user balance: {user_data['balance']}. Now calculating remaining funds.")
remaining = agent.call_tool("calculator", {"expression": f"{user_data['balance']} - 35.0"})

agent.log_thought(f"Calculation complete. Final remaining balance is ${remaining:.2f}.")
print(f"\nFinal Agent Internal State Snapshot:")
for k, v in agent.state.items():
    print(f"  {k}: {v}")


# -----------------------------------------------------------------------------
# Section 6: Key Takeaway Summary
# -----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("MODULE 01 COMPLETE: KEY TAKEAWAYS")
print("=" * 70)
print("1. Programming is the deliberate specification of sequential instructions.")
print("2. 'State' is everything your computer remembers right now in memory.")
print("3. Execution flows top-to-bottom unless altered by control flow.")
print("4. Python translates human-readable text into bytecode for the PVM to run.")
print("5. AI Agents are state machines that generate and execute sequential instructions.")
print("=" * 70)
