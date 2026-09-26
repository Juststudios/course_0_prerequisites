import socket

def run_tcp_client(host='127.0.0.1', port=9999):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"Connecting to {host}:{port}...")
        
        # Connect to the server
        client_socket.connect((host, port))
        print("Connected!")
        
        # Send data
        message = "Hello, TCP Server!"
        client_socket.sendall(message.encode('utf-8'))
        
        # Receive response
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    run_tcp_client()
