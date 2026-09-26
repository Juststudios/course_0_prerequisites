"""Solutions for Asgi"""

def modify_example():
    print("Logging added.")
    return True

def build_client():
    return "Client built"

def broken_example():
    print("Timeout added.")
    return True
