import socket

def run_tcp_server(host='127.0.0.1', port=9999):
    # Create a TCP socket
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow the port to be reused immediately after the server closes
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to address and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections (queue size of 5)
    server_socket.listen(5)
    print(f"TCP Server listening on {host}:{port}")
    
    try:
        while True:
            # Accept a connection (blocks until a client connects)
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            
            with client_socket:
                # Receive data
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                message = data.decode('utf-8')
                print(f"Received: {message}")
                
                # Send a response
                response = f"Server acknowledges: {message}"
                client_socket.sendall(response.encode('utf-8'))
                
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_tcp_server()
