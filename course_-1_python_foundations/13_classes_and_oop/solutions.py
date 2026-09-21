"""Module 13 Solutions"""
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
    def reset(self):
        self.count = 0

class ToolRegistry:
    def __init__(self):
        self._tools = {}
    def register(self, name: str, func):
        self._tools[name] = func
    def call(self, name: str, **kwargs):
        return self._tools[name](**kwargs)

class LoggingRegistry(ToolRegistry):
    def call(self, name: str, **kwargs):
        print(f"[LOG] calling {name}")
        return super().call(name, **kwargs)
