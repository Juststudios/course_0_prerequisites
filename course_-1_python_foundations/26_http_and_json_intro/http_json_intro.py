"""Module 26: HTTP and JSON Introduction"""
import json

# JSON is how Python objects travel over HTTP.
python_obj = {
    "model": "hermes-v1",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7
}

# Serialization: Python → JSON string (for sending)
json_string = json.dumps(python_obj, indent=2)
print("JSON string:\n", json_string)

# Deserialization: JSON string → Python (for receiving)
parsed = json.loads(json_string)
print("\nParsed:", parsed["model"])

# HTTP Request breakdown (conceptual):
print("""
POST /v1/chat/completions HTTP/1.1
Host: api.example.com
Authorization: Bearer sk-...
Content-Type: application/json

{"model": "hermes-v1", "messages": [...]}

↑ That JSON body is what json.dumps() produces.
""")
# For actual HTTP, see httpx in Module 04 of Course 0.
