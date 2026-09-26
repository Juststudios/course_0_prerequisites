# Module 25: HTTP Client Architecture - Solutions

# Tier 1: Recall
persistent_object = "Session"
dto_meaning = "Data Transfer Object"

# Tier 2: Modify
import requests

class SimpleClient:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Auth": self.token})
        
    def get_data(self):
        # Fix: Use the initialized session
        return self.session.get("https://api.example.com/data")

# Tier 3: Build
class GitHubRepoClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github.v3+json"})

    def get_repo(self, owner, repo_name):
        url = f"{self.base_url}/repos/{owner}/{repo_name}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

# Tier 4: Debug
class BuggyApiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/') # Clean trailing slashes
        import requests
        self.session = requests.Session()

    def make_request(self, endpoint):
        # Fix: Clean leading slashes to ensure consistent joining
        clean_endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{clean_endpoint}"
        return self.session.get(url).json()
