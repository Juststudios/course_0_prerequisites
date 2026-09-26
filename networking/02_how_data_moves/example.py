import time
import random

def simulate_packet_transmission(data, chunk_size=4):
    print(f"Original Data: '{data}'")
    
    # 1. Packetize the data
    packets = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        # Packet format: (sequence_number, payload)
        packet = (i // chunk_size, chunk)
        packets.append(packet)
        
    print(f"Generated Packets: {packets}\n")
    
    # 2. Simulate network routing (packets might arrive out of order!)
    print("Simulating network transmission (shuffling packets to simulate out-of-order delivery)...")
    random.shuffle(packets)
    
    received_packets = []
    for packet in packets:
        # Simulate varying latency
        time.sleep(random.uniform(0.1, 0.5))
        print(f"Router received packet: {packet}")
        received_packets.append(packet)
        
    print("\nAll packets received. Reassembling...")
    
    # 3. Reassemble the data
    # Sort based on sequence number
    received_packets.sort(key=lambda x: x[0])
    
    reassembled_data = ""
    for packet in received_packets:
        reassembled_data += packet[1]
        
    print(f"Reassembled Data: '{reassembled_data}'")
    
if __name__ == "__main__":
    simulate_packet_transmission("Hello, World! Networking is awesome.")
