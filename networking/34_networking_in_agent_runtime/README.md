# How Networking Appears Inside an Agent Runtime

## What You Will Learn
You will see exactly how all the networking concepts we've covered (TCP, HTTP, WebSockets, Databases) snap together to form the architecture of a real AI-agent runtime like Hermes.

## Prerequisites
All previous modules in this course.

## Key Terminology
| Term | Definition |
|------|------------|
| **Gateway** | The front door of the agent (e.g., a Telegram bot or a FastAPI web server). |
| **Orchestrator** | The brain of the agent that plans tasks and calls the LLM. |
| **Tool Execution Server** | An isolated environment (Docker/MCP) where dangerous code tools are run. |

## The Problem
An AI agent isn't just a single Python script. It needs to talk to the user, talk to the LLM, read the database, and execute tools. If you run all of this in one script, a slow API call to OpenAI will freeze the entire agent, making it unresponsive to the user.

## How It Works
Modern agents are distributed systems. 
1. The Gateway receives messages asynchronously.
2. The Database persists state.
3. The Orchestrator talks to the LLM via HTTP.
4. The Tools run in sandboxes and communicate via MCP or REST.

## Intuition
Think of an agent like a busy restaurant:
- **Gateway:** The waiter taking orders (WebSockets / HTTP).
- **Database:** The ticket rail where orders are stored (PostgreSQL / TCP).
- **Orchestrator:** The head chef reading the tickets and planning (Async Python).
- **Model API:** An external consultant the chef calls for advice (HTTPS / HTTPX).
- **Tools:** The sous-chefs chopping vegetables in a separate room so they don't cause a fire (Docker / MCP).

## Technical Explanation
Let's trace a single user message:
1. User types "What is the weather?" on a web frontend.
2. **WebSocket (Module 21)** carries the message to our **FastAPI Gateway (Module 19)**.
3. FastAPI writes the message to **PostgreSQL (Module 27)** so memory isn't lost if the server crashes.
4. The Orchestrator triggers an **async HTTPX POST (Module 15)** to `api.anthropic.com`.
5. The LLM responds: *"Call the weather tool."*
6. The Orchestrator makes an **MCP (Module 33)** call to a local Tool Server.
7. Tool Server responds via JSON. Orchestrator sends it back to the LLM.
8. LLM streams the final answer via **Server-Sent Events (Module 17)**.
9. FastAPI pushes the chunks back down the **WebSocket** to the user.

## Example
We will build a miniature version of this in the Capstone project.

## Python Implementation
See `agent_networking.py` for a diagrammatic code representation of the system.

## What Happens Underneath
Dozens of TCP handshakes, DNS lookups, and TLS negotiations are happening for every single turn of conversation! Connection pooling (keeping TCP connections alive) is critical here, otherwise the latency of doing a TLS handshake for every single LLM call will make the agent agonizingly slow.

## Common Mistakes
- **No connection pooling:** Using `requests.post()` instead of an `httpx.AsyncClient` instance, causing a new TCP handshake every time.
- **Blocking the event loop:** Doing heavy CPU work or synchronous database calls in the Orchestrator, which freezes the WebSocket connection and disconnects the user.

## Security Considerations
- Tool execution servers MUST be heavily sandboxed (Docker).
- API keys must NEVER be logged.
- The Gateway must rate-limit users, or an attacker can drain your LLM credits.

## Real-World Applications
This is exactly how Hermes, AutoGPT, and LangChain deployed systems operate.

## AI-Agent Connection
This module *is* the AI-agent connection.

## Exercises
See `exercises.py`.

## Challenge
Draw a sequence diagram mapping out the network flow of an agent.

## Summary
Agents are distributed systems bound together by HTTP, WebSockets, and database protocols.

## What You Should Know Before Moving On
You should be able to look at any agent architecture diagram and immediately understand the protocols being used to connect the boxes.
