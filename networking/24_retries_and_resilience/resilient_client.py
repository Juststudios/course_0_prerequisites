import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_resilient_session():
    """
    Creates a requests Session that automatically handles retries,
    exponential backoff, and connection pooling. This is the recommended
    way to handle retries in production Python applications.
    """
    session = requests.Session()
    
    # Define the retry strategy
    retry_strategy = Retry(
        total=3, # Total number of retries
        backoff_factor=1, # wait 1, 2, 4 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504], # Status codes to retry on
        allowed_methods=["HEAD", "GET", "OPTIONS", "PUT", "DELETE"] # Idempotent methods
    )
    
    # Create an adapter with the strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # Mount it for both http and https
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

if __name__ == "__main__":
    session = create_resilient_session()
    print("Session created. If you use session.get('http://httpbin.org/status/503'), it will retry automatically.")
    
    # Uncomment to test (it will take a few seconds as it backs off)
    # try:
    #     response = session.get("http://httpbin.org/status/503")
    # except requests.exceptions.RetryError as e:
    #     print("Failed after all retries.")
