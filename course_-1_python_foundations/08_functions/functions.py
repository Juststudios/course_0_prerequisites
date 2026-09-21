
def add(a: int, b: int) -> int:
    return a + b

tools = {
    "add": add
}
print(tools["add"](2, 3))
