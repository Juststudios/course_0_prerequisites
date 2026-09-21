# Module 13: Classes and Object-Oriented Programming

## Key Terminology
| Term | Definition |
|------|------------|
| **Class** | Blueprint / template for objects |
| **Object / Instance** | A specific thing created from a class |
| **Attribute** | Data attached to an object (`self.name`) |
| **Method** | A function defined inside a class |
| **`__init__`** | Constructor — called when an object is created |
| **`self`** | Reference to the current instance |
| **Inheritance** | A class that extends another class |
| **Composition** | A class that *contains* another object |

## When to Use Classes
Use classes when you need multiple independent copies of something that holds state and behaviour together — like multiple agents running concurrently.

## Connection to AI Agents
Every agent runtime represents agents as classes. The `Agent` class holds the model name, tool registry, memory, and execution methods.
