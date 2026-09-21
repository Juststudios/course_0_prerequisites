"""Module 13 Exercises"""
# Level 1: What does this print?
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
c = Counter()
c.increment()
c.increment()
print(c.count)

# Level 2: TODO — add a method `reset()` that sets count back to 0.

# Level 3: TODO — build a `ToolRegistry` class with:
#   register(name, func) and call(name, **kwargs)
class ToolRegistry:
    raise NotImplementedError("Implement ToolRegistry")

# Level 4: TODO — extend ToolRegistry with a subclass `LoggingRegistry`
# that prints the tool name before every call.
