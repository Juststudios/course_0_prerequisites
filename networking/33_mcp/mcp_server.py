"""
Model Context Protocol (MCP) Server
A minimal educational mock of an MCP server providing tools to an LLM.
"""
import json
import sys

def handle_mcp_request(request_line: str):
    """Parses JSON-RPC style MCP requests over stdin/stdout."""
    try:
        req = json.loads(request_line)
        if req.get("method") == "list_tools":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req.get("id"),
                "result": {"tools": [{"name": "read_file", "description": "Reads a file"}]}
            })
    except json.JSONDecodeError:
        pass
    return json.dumps({"error": "Invalid request"})

def main():
    print("MCP Server mock started.", file=sys.stderr)
    # Exiting immediately for verification
    print("[DEMO] Exiting cleanly.")

if __name__ == "__main__":
    main()
