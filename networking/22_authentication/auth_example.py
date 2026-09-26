import requests
import base64

def manual_basic_auth(username, password):
    """Demonstrates how basic auth headers are constructed manually."""
    credentials = f"{username}:{password}"
    # Base64 encode the string
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    return headers

def mock_request():
    headers = manual_basic_auth("admin", "secret")
    print("Generated Headers:", headers)
    # response = requests.get("https://api.example.com/protected", headers=headers)
    # return response

if __name__ == "__main__":
    mock_request()
