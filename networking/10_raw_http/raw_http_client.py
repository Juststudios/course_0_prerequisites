import socket

def run_raw_http_client(host='127.0.0.1', port=8080, path="/"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        
        # Construct the raw HTTP GET request
        # \r\n is crucial!
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"User-Agent: Raw-Python-Client/1.0\r\n"
            f"Accept: */*\r\n"
            f"\r\n" # Blank line separates headers from body
        )
        
        print(f"Sending request to {path}...\n")
        client.sendall(request.encode('utf-8'))
        
        # Read the response
        response = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            response += chunk
            
        print("--- Server Response ---")
        print(response.decode('utf-8'))

if __name__ == "__main__":
    # Test root path
    run_raw_http_client(path="/")
    print("\n" + "="*40 + "\n")
    # Test API path
    run_raw_http_client(path="/api")
