import httpx
import time

def unpooled_requests():
    print("Making 3 unpooled requests (new TCP handshake every time)...")
    start = time.time()
    for _ in range(3):
        httpx.get("https://httpbin.org/get")
    print(f"Unpooled time: {time.time() - start:.2f}s")

def pooled_requests():
    print("Making 3 pooled requests (one TCP handshake)...")
    start = time.time()
    with httpx.Client() as client:
        for _ in range(3):
            client.get("https://httpbin.org/get")
    print(f"Pooled time: {time.time() - start:.2f}s")

if __name__ == "__main__":
    unpooled_requests()
    print("-" * 20)
    pooled_requests()
