# 03_osi_and_tcp_ip / example.py

def simulate_encapsulation_decapsulation():
    # 1. Application Layer (Data)
    application_data = "GET /index.html HTTP/1.1"
    print(f"1. Application Data: {application_data}")
    
    # 2. Transport Layer (Adds TCP Header)
    tcp_header = "[TCP: SrcPort=5000, DstPort=80] "
    transport_segment = tcp_header + application_data
    print(f"2. Transport Segment: {transport_segment}")
    
    # 3. Network Layer (Adds IP Header)
    ip_header = "[IP: Src=192.168.1.5, Dst=10.0.0.1] "
    network_packet = ip_header + transport_segment
    print(f"3. Network Packet: {network_packet}")
    
    # 4. Data Link Layer (Adds MAC Header and Footer)
    mac_header = "[MAC: Src=AA:BB:CC, Dst=DD:EE:FF] "
    mac_footer = " [FCS: Checksum]"
    ethernet_frame = mac_header + network_packet + mac_footer
    print(f"4. Ethernet Frame (Sent over wire): {ethernet_frame}\n")
    
    print("--- Data Travels Over the Network ---\n")
    
    # Decapsulation on the receiving end
    print("Receiver decapsulating data:")
    
    # Strip Link Layer
    decapped_network = ethernet_frame.replace(mac_header, "").replace(mac_footer, "")
    print(f"3. Decapsulated Network Packet: {decapped_network}")
    
    # Strip Network Layer
    decapped_transport = decapped_network.replace(ip_header, "")
    print(f"2. Decapsulated Transport Segment: {decapped_transport}")
    
    # Strip Transport Layer
    received_app_data = decapped_transport.replace(tcp_header, "")
    print(f"1. Received Application Data: {received_app_data}")

if __name__ == "__main__":
    simulate_encapsulation_decapsulation()
