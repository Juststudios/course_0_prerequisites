# 05_ports / example.py

import socket
import threading
import time

def demo_server(port, name):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SO_REUSEADDR allows us to restart the script quickly without "Address in use" errors
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', port))
        s.listen(1)
        print(f"[{name}] Server listening on port {port}...")
        
        # Run for a short time
        s.settimeout(2.0)
        try:
            conn, addr = s.accept()
            print(f"[{name}] Connection received from ephemeral port {addr[1]}!")
            conn.close()
        except socket.timeout:
            print(f"[{name}] No connections received.")
        s.close()
    except Exception as e:
        print(f"[{name}] Error starting on port {port}: {e}")

def run_demonstration():
    # Start two servers on different ports on the same machine
    t1 = threading.Thread(target=demo_server, args=(8001, "Web App"))
    t2 = threading.Thread(target=demo_server, args=(8002, "Database"))
    
    t1.start()
    t2.start()
    
    time.sleep(0.5)
    
    # Client connecting to Web App
    c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c1.connect(('127.0.0.1', 8001))
    print(f"[Client 1] Connected to 8001. My assigned ephemeral port is: {c1.getsockname()[1]}")
    c1.close()
    
    t1.join()
    t2.join()

if __name__ == "__main__":
    run_demonstration()
