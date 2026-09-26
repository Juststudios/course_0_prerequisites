import httpx

def run_httpx_demo():
    print("--- 1. Simple GET Request ---")
    response = httpx.get("https://httpbin.org/get")
    print(f"Status: {response.status_code}")
    # httpbin returns exactly what we sent it in a JSON format
    data = response.json()
    print(f"Your IP according to httpbin: {data['origin']}")
    
    print("\n--- 2. POST Request with JSON ---")
    payload = {"name": "Alice", "role": "Agent"}
    response = httpx.post("https://httpbin.org/post", json=payload)
    print(f"Status: {response.status_code}")
    print("Response JSON data parsed back:")
    print(response.json()['json'])
    
    print("\n--- 3. Handling Errors ---")
    response = httpx.get("https://httpbin.org/status/404")
    print(f"Requested a 404 page. Status code is: {response.status_code}")
    print(f"Is success? {response.is_success}")
    print(f"Is error? {response.is_error}")
    
    try:
        # This will raise an exception because it's a 4xx error
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"Caught HTTP Error: {e}")
        
    print("\n--- 4. Connection Pooling (Client) ---")
    # Using a Client keeps the TCP connection alive across multiple requests
    with httpx.Client() as client:
        r1 = client.get("https://httpbin.org/get")
        r2 = client.get("https://httpbin.org/get")
        print("Made two requests using the same underlying TCP connection!")

if __name__ == "__main__":
    # Note: requires `pip install httpx`
    try:
        run_httpx_demo()
    except ImportError:
        print("Please install httpx to run this demo: pip install httpx")
