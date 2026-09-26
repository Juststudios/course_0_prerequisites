import socket

def raw_http_get():
    # 1. Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Connect to example.com on port 80 (HTTP)
    s.connect(("example.com", 80))
    
    # 3. Build the raw HTTP text string
    request = "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
    
    # 4. Send the bytes over the wire
    s.sendall(request.encode("utf-8"))
    
    # 5. Receive the response
    response = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk
        
    print(response.decode("utf-8"))
    s.close()

if __name__ == "__main__":
    raw_http_get()
