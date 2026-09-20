"""abstract_providers.py - Demonstrates Abstract Base Classes, Polymorphism, and Composition for LLM Providers.

Key concepts demonstrated:
1. Abstract Base Classes (ABC) and @abstractmethod interface contracts.
2. Polymorphic provider implementations (MockProvider vs RuleBasedProvider).
3. Composition pattern: Injecting interchangeable providers into an Agent core.
"""

from typing import List, Dict, Any, Optional
import abc


class BaseLLMProvider(abc.ABC):
    """Abstract interface that every LLM provider must implement."""

    def __init__(self, model_name: str, temperature: float = 0.0) -> None:
        self.model_name = model_name
        self.temperature = temperature

    @abc.abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """Generates a text completion given a list of chat messages."""
        pass

    @abc.abstractmethod
    def count_tokens(self, text: str) -> int:
        """Returns the approximate token count for a string."""
        pass


class MockDeterministicProvider(BaseLLMProvider):
    """A deterministic mock provider designed for testing and offline development."""

    def __init__(self, responses: Optional[List[str]] = None) -> None:
        super().__init__(model_name="mock-model-v1", temperature=0.0)
        self._responses = responses or ["I am a mock assistant.", "Task completed."]
        self._call_index = 0

    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        if not messages:
            raise ValueError("Messages list cannot be empty.")
        response = self._responses[self._call_index % len(self._responses)]
        self._call_index += 1
        return response

    def count_tokens(self, text: str) -> int:
        # Standard heuristic: ~4 characters per token
        return max(1, len(text) // 4)


class LocalRuleProvider(BaseLLMProvider):
    """A rule-based reasoning provider simulating basic tool intent detection."""

    def __init__(self) -> None:
        super().__init__(model_name="rule-based-v1", temperature=0.0)

    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        if not messages:
            raise ValueError("Messages list cannot be empty.")
        last_user_msg = messages[-1].get("content", "").lower()

        if "calculate" in last_user_msg or "compute" in last_user_msg:
            return 'ACTION: calculator {"expr": "40 + 2"}'
        elif "search" in last_user_msg or "find" in last_user_msg:
            return 'ACTION: search {"query": "python async patterns"}'
        else:
            return "FINAL ANSWER: I understand your query and am ready to assist."

    def count_tokens(self, text: str) -> int:
        return len(text.split())


class AutonomousAgentCore:
    """Agent core built using composition over inheritance."""

    def __init__(self, provider: BaseLLMProvider, system_prompt: str) -> None:
        self.provider = provider
        self.system_prompt = system_prompt
        self.message_history: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]

    def interact(self, user_input: str) -> str:
        """Processes user input using the injected polymorphic provider."""
        self.message_history.append({"role": "user", "content": user_input})
        output = self.provider.generate(self.message_history)
        self.message_history.append({"role": "assistant", "content": output})
        return output


def main() -> None:
    print("=== Module 02: Abstract Providers & Polymorphism Demo ===")

    # 1. Verify ABC instantiation restrictions
    try:
        # Should fail because generate and count_tokens are abstract
        BaseLLMProvider("invalid")  # type: ignore[abstract]
        raise AssertionError("Instantiating BaseLLMProvider must raise TypeError")
    except TypeError as err:
        print(f"[OK] Instantiating ABC raised expected TypeError: {err}")

    # 2. Test MockDeterministicProvider
    mock_llm = MockDeterministicProvider(["Mock Step 1", "Mock Step 2"])
    agent_with_mock = AutonomousAgentCore(mock_llm, "System: Test Mode")
    res1 = agent_with_mock.interact("Hello?")
    res2 = agent_with_mock.interact("What next?")
    assert res1 == "Mock Step 1"
    assert res2 == "Mock Step 2"
    assert mock_llm.count_tokens("Hello world from mock") == 5
    print("[OK] MockDeterministicProvider responded predictably.")

    # 3. Test LocalRuleProvider via identical Agent interface (Polymorphism)
    rule_llm = LocalRuleProvider()
    agent_with_rules = AutonomousAgentCore(rule_llm, "System: Rule Mode")
    calc_res = agent_with_rules.interact("Please calculate 40 + 2")
    search_res = agent_with_rules.interact("Can you find articles?")
    general_res = agent_with_rules.interact("Thanks for the help!")

    assert 'ACTION: calculator' in calc_res
    assert 'ACTION: search' in search_res
    assert 'FINAL ANSWER' in general_res
    print("[OK] LocalRuleProvider correctly triggered actions via polymorphism.")

    print("All tests in abstract_providers.py completed successfully!\n")


if __name__ == "__main__":
    main()
