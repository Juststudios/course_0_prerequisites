"""
Module 13: Classes and Object-Oriented Programming (OOP)
=========================================================
A deep exploration of Python's object-oriented capabilities: blueprints,
instance state, the role of self, dunder methods, encapsulation, inheritance,
polymorphism, and compositional agent architectures.

Run this script directly:
    python3 classes.py
"""

from typing import Any, Callable, Dict, List, Optional
import time


def banner(title: str) -> None:
    """Helper to format section headers for clear terminal readability."""
    print("\n" + "=" * 75)
    print(f"  {title.upper()}")
    print("=" * 75)


# =============================================================================
# Section 1: The Blueprint and The Instance — Understanding 'self'
# =============================================================================
banner("Section 1: The Blueprint and the Instance")

# A class is a blueprint; an instance is a concrete object created in memory.
# When an instance method is called, Python automatically passes the instance itself
# as the first argument, conventionally named `self`.

class RoboticRover:
    """Represents an autonomous planetary rover."""

    def __init__(self, designation: str, battery_capacity_kwh: float) -> None:
        # Instance attributes — unique to each individual rover instance:
        self.designation: str = designation
        self.battery_capacity: float = battery_capacity_kwh
        self.current_battery: float = battery_capacity_kwh
        self.distance_traveled_km: float = 0.0

    def drive(self, distance_km: float) -> bool:
        """Consumes battery to travel a given distance."""
        energy_needed = distance_km * 0.25  # 0.25 kWh per km
        if self.current_battery >= energy_needed:
            self.current_battery -= energy_needed
            self.distance_traveled_km += distance_km
            print(f"[{self.designation}] Drove {distance_km:.1f} km. Battery: {self.current_battery:.1f} kWh left.")
            return True
        else:
            print(f"[{self.designation}] Insufficient power to drive {distance_km:.1f} km!")
            return False

# Create two independent instances:
curiosity = RoboticRover("Curiosity", 50.0)
perseverance = RoboticRover("Perseverance", 75.0)

curiosity.drive(20.0)
perseverance.drive(10.0)

print(f"\nCuriosity state: traveled {curiosity.distance_traveled_km} km (Battery: {curiosity.current_battery})")
print(f"Perseverance state: traveled {perseverance.distance_traveled_km} km (Battery: {perseverance.current_battery})")
print(f"Are instances independent objects? {curiosity is not perseverance}")


# =============================================================================
# Section 2: Instance Attributes vs Class Attributes (The Shared Trap)
# =============================================================================
banner("Section 2: Instance Attributes vs Class Attributes")

# Class attributes are defined at the class level and shared by ALL instances.
# Instance attributes are bound to `self` inside `__init__`.
# DANGER: Never use a mutable object (list, dict) as a class attribute!

class SafeAgent:
    # Class attribute (immutable metadata shared across all agents)
    SYSTEM_VERSION: str = "3.2.0"

    def __init__(self, agent_id: str) -> None:
        # CORRECT: Each agent receives its own distinct list instance in memory
        self.agent_id: str = agent_id
        self.scratchpad: List[str] = []

agent_alpha = SafeAgent("agent-001")
agent_beta = SafeAgent("agent-002")

agent_alpha.scratchpad.append("Discovered optimal route.")
print(f"Agent Alpha scratchpad: {agent_alpha.scratchpad}")
print(f"Agent Beta scratchpad:  {agent_beta.scratchpad} (Clean and independent!)")
print(f"Both share version: {agent_alpha.SYSTEM_VERSION} == {agent_beta.SYSTEM_VERSION}")


# =============================================================================
# Section 3: Methods — Instance, Class, and Static
# =============================================================================
banner("Section 3: Instance Methods, @classmethod, and @staticmethod")

class AgentConfig:
    def __init__(self, model_name: str, max_tokens: int, temperature: float) -> None:
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

    # 1. Instance Method: Receives `self`, acts on instance data
    def summary(self) -> str:
        return f"{self.model_name} (T={self.temperature}, MaxTokens={self.max_tokens})"

    # 2. Class Method: Receives `cls` (the class), commonly used for alternative constructors
    @classmethod
    def create_creative(cls, model_name: str) -> "AgentConfig":
        """Factory method for high-temperature creative mode."""
        return cls(model_name=model_name, max_tokens=2048, temperature=0.9)

    @classmethod
    def create_deterministic(cls, model_name: str) -> "AgentConfig":
        """Factory method for zero-temperature reasoning mode."""
        return cls(model_name=model_name, max_tokens=1024, temperature=0.0)

    # 3. Static Method: Does not receive `self` or `cls`, like a regular function grouped in the class
    @staticmethod
    def is_valid_temperature(temp: float) -> bool:
        return 0.0 <= temp <= 2.0

creative_cfg = AgentConfig.create_creative("gpt-4o")
precise_cfg = AgentConfig.create_deterministic("claude-3-opus")
print(f"Creative config:    {creative_cfg.summary()}")
print(f"Precise config:     {precise_cfg.summary()}")
print(f"Is temperature 1.5 valid? {AgentConfig.is_valid_temperature(1.5)}")


# =============================================================================
# Section 4: Encapsulation & Properties (@property)
# =============================================================================
banner("Section 4: Encapsulation and @property")

# In Python, encapsulation is achieved via naming conventions (_protected, __private)
# and `@property` decorators which allow managed attribute access with validation.

class SecureTokenWallet:
    def __init__(self, initial_tokens: int = 1000) -> None:
        self._tokens: int = initial_tokens  # Protected by convention

    @property
    def balance(self) -> int:
        """Getter: Read-only access or computed property."""
        return self._tokens

    @balance.setter
    def balance(self, new_amount: int) -> None:
        """Setter: Enforces domain rules and data integrity."""
        if new_amount < 0:
            raise ValueError("Token balance cannot be negative!")
        self._tokens = new_amount

    def consume(self, amount: int) -> bool:
        if amount <= self._tokens:
            self._tokens -= amount
            return True
        return False

wallet = SecureTokenWallet(500)
print(f"Initial wallet balance: {wallet.balance}")
wallet.consume(120)
print(f"Balance after consumption: {wallet.balance}")


# =============================================================================
# Section 5: Special Dunder Methods (__repr__, __str__, __eq__, __call__)
# =============================================================================
banner("Section 5: Special Dunder Methods")

class AgentMessage:
    """Represents a structured conversation turn in an LLM dialog."""

    def __init__(self, role: str, content: str) -> None:
        self.role: str = role
        self.content: str = content

    def __repr__(self) -> str:
        """Unambiguous string for debugging and logging."""
        return f"AgentMessage(role={self.role!r}, content={self.content!r})"

    def __str__(self) -> str:
        """User-facing friendly formatted string."""
        return f"[{self.role.upper()}]: {self.content}"

    def __eq__(self, other: Any) -> bool:
        """Defines value equality with == operator."""
        if not isinstance(other, AgentMessage):
            return False
        return self.role == other.role and self.content == other.content

    def __len__(self) -> int:
        """Allows calling len(message) to get character count."""
        return len(self.content)

msg1 = AgentMessage("assistant", "Observation: Task completed.")
msg2 = AgentMessage("assistant", "Observation: Task completed.")
msg3 = AgentMessage("user", "What is the status?")

print(f"__str__ representation:  {msg1}")
print(f"__repr__ representation: {repr(msg1)}")
print(f"Equality msg1 == msg2:   {msg1 == msg2} (Different objects, identical values)")
print(f"Equality msg1 == msg3:   {msg1 == msg3}")
print(f"Length of msg1 content:  {len(msg1)} characters")


# =============================================================================
# Section 6: Inheritance, Method Overriding, and super()
# =============================================================================
banner("Section 6: Inheritance and Polymorphism")

class BaseTool:
    """Base class for all tools in an agent environment."""

    def __init__(self, name: str, description: str) -> None:
        self.name: str = name
        self.description: str = description

    def execute(self, **kwargs: Any) -> Any:
        raise NotImplementedError("Subclasses must implement execute()!")


class CalculatorTool(BaseTool):
    """Subclass inheriting from BaseTool and overriding execute()."""

    def __init__(self) -> None:
        super().__init__(name="calculator", description="Evaluates safe arithmetic expressions.")

    def execute(self, expression: str = "0", **kwargs: Any) -> float:
        # Safe mathematical evaluation for simple expressions
        allowed = {"+", "-", "*", "/", " ", ".", "(", ")"}
        if not all(c.isdigit() or c in allowed for c in expression):
            raise ValueError(f"Invalid characters in expression: {expression}")
        return float(eval(expression, {"__builtins__": None}, {}))


class EchoTool(BaseTool):
    """Subclass inheriting from BaseTool for echo testing."""

    def __init__(self) -> None:
        super().__init__(name="echo", description="Echoes back input text.")

    def execute(self, text: str = "", **kwargs: Any) -> str:
        return f"ECHO: {text}"


# Polymorphism: Different classes implement the same interface (execute).
# An agent can treat all tools identically through the BaseTool contract!
tools: List[BaseTool] = [CalculatorTool(), EchoTool()]
print("Demonstrating Polymorphism across tool collection:")
for tool in tools:
    print(f"  Tool '{tool.name}': {tool.description}")

calc_res = tools[0].execute(expression="15 * 4 + 10")
echo_res = tools[1].execute(text="Agent online")
print(f"Calculator result: {calc_res}")
print(f"Echo result:       {echo_res}")


# =============================================================================
# Section 7: Composition over Inheritance — Real-World AI Agent
# =============================================================================
banner("Section 7: Composition over Inheritance (Agent Architecture)")

# In modern software engineering, "composition" (has-a) is far more flexible
# than inheritance (is-a). An Agent HAS-A memory and HAS-A tool registry.

class MemoryBuffer:
    """Encapsulates interaction history."""
    def __init__(self, max_turns: int = 10) -> None:
        self.max_turns = max_turns
        self.history: List[str] = []

    def record(self, event: str) -> None:
        self.history.append(event)
        if len(self.history) > self.max_turns:
            self.history.pop(0)


class ToolRegistry:
    """Encapsulates tool lookup and dispatch."""
    def __init__(self) -> None:
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def dispatch(self, tool_name: str, **kwargs: Any) -> Any:
        if tool_name not in self._tools:
            raise KeyError(f"Tool '{tool_name}' is not registered.")
        return self._tools[tool_name].execute(**kwargs)


class ReActAgent:
    """An autonomous agent composing MemoryBuffer and ToolRegistry."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        # Composition: Agent HAS-A memory and HAS-A registry
        self.memory: MemoryBuffer = MemoryBuffer(max_turns=5)
        self.registry: ToolRegistry = ToolRegistry()

    def run_step(self, tool_name: str, **kwargs: Any) -> str:
        self.memory.record(f"THINK: Calling tool '{tool_name}' with {kwargs}")
        try:
            result = self.registry.dispatch(tool_name, **kwargs)
            self.memory.record(f"OBSERVE: Result = {result}")
            return str(result)
        except Exception as e:
            err_msg = f"ERROR: {e}"
            self.memory.record(f"OBSERVE: {err_msg}")
            return err_msg


agent = ReActAgent("Hermes-Agent")
agent.registry.register(CalculatorTool())
agent.registry.register(EchoTool())

step_1 = agent.run_step("calculator", expression="100 / 4")
step_2 = agent.run_step("echo", text="Target coordinates reached.")

print(f"\nAgent '{agent.name}' executed 2 steps successfully:")
print(f"Step 1 output: {step_1}")
print(f"Step 2 output: {step_2}")
print("Agent memory history:")
for entry in agent.memory.history:
    print(f"  {entry}")

banner("Module 13 Lesson Complete")
