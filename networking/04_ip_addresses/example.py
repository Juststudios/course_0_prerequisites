# 04_ip_addresses / example.py

import socket

def demonstrate_ip_lookups():
    # 1. Get the local hostname
    hostname = socket.gethostname()
    print(f"Local Hostname: {hostname}")
    
    # 2. Get local IP address (This might return a private IP or loopback)
    local_ip = socket.gethostbyname(hostname)
    print(f"Local IP Address: {local_ip}")
    
    # 3. Resolve a domain name to an IP address
    domain = "google.com"
    try:
        domain_ip = socket.gethostbyname(domain)
        print(f"The IP address of {domain} is: {domain_ip}")
    except socket.gaierror:
        print(f"Could not resolve IP for {domain}")
        
    # 4. Demonstrate loopback
    loopback_ip = "127.0.0.1"
    print(f"The Loopback address is always {loopback_ip} (localhost).")

if __name__ == "__main__":
    demonstrate_ip_lookups()
