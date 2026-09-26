# 07_tcp / example.py

import time
import random

def simulate_tcp_handshake():
    print("--- TCP Three-Way Handshake Simulation ---")
    
    # 1. SYN
    client_seq = random.randint(1000, 9000)
    print(f"[Client] Sending SYN. Seq={client_seq}")
    time.sleep(1)
    
    # 2. SYN-ACK
    server_seq = random.randint(1000, 9000)
    server_ack = client_seq + 1
    print(f"[Server] Received SYN. Sending SYN-ACK. Seq={server_seq}, Ack={server_ack}")
    time.sleep(1)
    
    # 3. ACK
    client_ack = server_seq + 1
    print(f"[Client] Received SYN-ACK. Sending ACK. Seq={server_ack}, Ack={client_ack}")
    time.sleep(1)
    
    print("--- Connection Established! ---")

def simulate_tcp_reliability(message):
    print("\n--- TCP Data Transmission with Packet Loss ---")
    
    packets = list(message)
    expected_seq = 0
    
    while expected_seq < len(packets):
        print(f"\n[Client] Sending packet Seq={expected_seq} Data='{packets[expected_seq]}'")
        time.sleep(0.5)
        
        # Simulate 30% chance of packet loss
        if random.random() < 0.30:
            print("[Network] ❌ PACKET LOST!")
            print("[Client] Timeout waiting for ACK. Retransmitting...")
            # Loop restarts, sending the same packet again
            continue
            
        print(f"[Server] ✅ Received '{packets[expected_seq]}'. Sending ACK={expected_seq + 1}")
        expected_seq += 1
        
    print("\n--- All Data Successfully Transmitted! ---")

if __name__ == "__main__":
    simulate_tcp_handshake()
    simulate_tcp_reliability("TCP")
