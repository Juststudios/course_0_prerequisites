# 06_dns / example.py

import socket

def demonstrate_dns():
    domains_to_lookup = [
        "example.com",
        "google.com",
        "github.com",
        "localhost"
    ]
    
    for domain in domains_to_lookup:
        try:
            # gethostbyname is Python's standard way to do an A-record DNS lookup
            ip_address = socket.gethostbyname(domain)
            print(f"Domain: {domain.ljust(15)} -> IP Address: {ip_address}")
        except socket.gaierror as e:
            print(f"Failed to resolve {domain}: {e}")

# Simulating a local DNS cache / Hosts file
class LocalDNSCache:
    def __init__(self):
        self.cache = {
            "my-custom-website.local": "192.168.1.100"
        }
        
    def resolve(self, domain):
        print(f"\n[DNS Cache] Attempting to resolve {domain}...")
        if domain in self.cache:
            print(f"[DNS Cache] Cache HIT! IP is {self.cache[domain]}")
            return self.cache[domain]
            
        print("[DNS Cache] Cache MISS! Going out to the internet...")
        try:
            ip = socket.gethostbyname(domain)
            print(f"[DNS Cache] Internet returned {ip}. Caching it.")
            self.cache[domain] = ip
            return ip
        except socket.gaierror:
            print("[DNS Cache] Domain not found anywhere.")
            return None

if __name__ == "__main__":
    print("--- Standard DNS Lookups ---")
    demonstrate_dns()
    
    print("\n--- Simulated DNS Cache ---")
    my_dns = LocalDNSCache()
    my_dns.resolve("my-custom-website.local")
    my_dns.resolve("python.org")
    my_dns.resolve("python.org") # Second time should hit cache!
