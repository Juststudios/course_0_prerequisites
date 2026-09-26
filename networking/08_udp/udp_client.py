import socket

def run_udp_client(server_host='127.0.0.1', server_port=8888):
    # AF_INET indicates IPv4, SOCK_DGRAM indicates UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # We don't need to bind or connect for UDP!
        
        message = "Hello, UDP Server!"
        print(f"Sending: {message}")
        
        # Send data directly to the server address
        client_socket.sendto(message.encode('utf-8'), (server_host, server_port))
        
        # Wait for response
        # Using a timeout so it doesn't block forever if packet is lost
        client_socket.settimeout(2.0)
        try:
            data, server_address = client_socket.recvfrom(1024)
            print(f"Received from {server_address}: {data.decode('utf-8')}")
        except socket.timeout:
            print("Request timed out. Packet might have been lost!")

if __name__ == "__main__":
    run_udp_client()
