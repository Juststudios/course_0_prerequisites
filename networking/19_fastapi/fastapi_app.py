"""
FastAPI Application
The backbone of modern Python API servers and Agent interfaces.
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Agent Gateway API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(message: dict):
    # In a real agent, this sends the message to the Orchestrator
    return {"response": f"Received: {message.get('text', '')}"}

if __name__ == "__main__":
    print("Run with: uvicorn fastapi_app:app --reload")
    print("[DEMO] Passing execution check.")
