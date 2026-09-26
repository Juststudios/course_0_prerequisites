import requests
from typing import Optional

class BaseClient:
    """A robust base client handling sessions, timeouts, and errors."""
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def request(self, method: str, path: str, params: Optional[dict] = None, json_data: Optional[dict] = None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        
        # Centralized timeout config
        response = self.session.request(
            method, 
            url, 
            params=params, 
            json=json_data,
            timeout=(3.0, 10.0) # 3s connect timeout, 10s read timeout
        )
        
        response.raise_for_status()
        return response.json()

class TodoClient(BaseClient):
    """Specific implementation for a Todo API."""
    def get_todo(self, todo_id: int):
        return self.request("GET", f"/todos/{todo_id}")
        
    def create_todo(self, title: str, completed: bool = False):
        return self.request("POST", "/todos", json_data={"title": title, "completed": completed})

if __name__ == "__main__":
    # Example usage against jsonplaceholder
    client = TodoClient(base_url="https://jsonplaceholder.typicode.com", api_key="dummy_key")
    
    print("Fetching todo 1...")
    todo = client.get_todo(1)
    print(todo)
