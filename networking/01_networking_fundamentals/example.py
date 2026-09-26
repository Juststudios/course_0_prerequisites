import socket
import threading
import time

def simple_server():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen(1)
    print("[Server] Listening on port 8000...")

    # Accept a connection
    conn, addr = server_socket.accept()
    print(f"[Server] Connected to {addr}")
    
    # Receive data
    data = conn.recv(1024)
    print(f"[Server] Received: {data.decode('utf-8')}")
    
    # Send response
    conn.sendall(b"Hello from the server!")
    
    # Close connection
    conn.close()
    server_socket.close()

def simple_client():
    # Wait a moment for the server to start
    time.sleep(1)
    
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect(('127.0.0.1', 8000))
    print("[Client] Connected to server!")
    
    # Send data
    client_socket.sendall(b"Hello from the client!")
    
    # Receive data
    data = client_socket.recv(1024)
    print(f"[Client] Received: {data.decode('utf-8')}")
    
    # Close connection
    client_socket.close()

if __name__ == "__main__":
    # Run server in a separate thread so they can talk to each other
    t = threading.Thread(target=simple_server)
    t.start()
    
    simple_client()
    
    t.join()
