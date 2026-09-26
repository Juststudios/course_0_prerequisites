import socket
import ssl

def run_https_client(host='example.com', port=443, path="/"):
    # 1. Create a standard TCP socket
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Create a default SSL context
    # create_default_context() loads the system's trusted root certificates
    context = ssl.create_default_context()
    
    # 3. Wrap the socket
    # server_hostname is required for SNI (Server Name Indication) 
    # so the server knows which certificate to serve
    secure_socket = context.wrap_socket(raw_socket, server_hostname=host)
    
    try:
        print(f"Connecting to https://{host}{path}...")
        # 4. Connect (this performs the TCP handshake AND the TLS handshake)
        secure_socket.connect((host, port))
        
        # We can inspect the secure connection
        print("TLS Version:", secure_socket.version())
        print("Cipher:", secure_socket.cipher()[0])
        
        # 5. Send raw HTTP request over the secure tunnel
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Connection: close\r\n\r\n"
        )
        secure_socket.sendall(request.encode('utf-8'))
        
        # 6. Read the response
        response = b""
        while True:
            chunk = secure_socket.recv(4096)
            if not chunk:
                break
            response += chunk
            
        print("\n--- Response Headers ---")
        # Just printing the headers for brevity
        headers = response.decode('utf-8').split('\r\n\r\n')[0]
        print(headers)
        
    except ssl.SSLError as e:
        print(f"TLS/SSL Error: {e}")
    except Exception as e:
        print(f"Network Error: {e}")
    finally:
        secure_socket.close()

if __name__ == "__main__":
    run_https_client()
    
    # Challenge Hint: Uncomment below to see a certificate error
    # print("\nTesting bad certificate...")
    # run_https_client(host="expired.badssl.com")
