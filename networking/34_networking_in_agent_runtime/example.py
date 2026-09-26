import socket
import ipaddress
import requests
from urllib.parse import urlparse

def is_safe_url(url: str) -> bool:
    """Checks if a URL resolves to a public, safe IP address."""
    try:
        # Parse the hostname from the URL
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Resolve hostname to IP
        # Note: this is a basic check. DNS rebinding can still bypass this!
        ip_str = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(ip_str)
        
        # Check if the IP is global (public) and not loopback/private/reserved
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            print(f"Blocked SSRF attempt to {ip_str} ({hostname})")
            return False
            
        return True
    except Exception as e:
        print(f"Error resolving {url}: {e}")
        return False

def safe_fetch(url: str):
    if is_safe_url(url):
        # Disable redirects to prevent redirect-based SSRF!
        response = requests.get(url, allow_redirects=False)
        return response.text
    else:
        raise PermissionError("Access to internal network is forbidden.")

if __name__ == '__main__':
    # Test cases
    print("Testing http://google.com:", is_safe_url("http://google.com"))
    print("Testing http://localhost:", is_safe_url("http://localhost"))
    print("Testing http://169.254.169.254:", is_safe_url("http://169.254.169.254"))
