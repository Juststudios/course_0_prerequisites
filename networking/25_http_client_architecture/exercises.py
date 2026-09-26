# Module 25: HTTP Client Architecture - Exercises

# Tier 1: Recall
# 1. What object in the `requests` library allows you to persist settings (like headers) and TCP connections across multiple requests?
# TODO: Write your answer as a string.
persistent_object = ""

# 2. What does DTO stand for?
# TODO: Write your answer as a string.
dto_meaning = ""


# Tier 2: Modify
class SimpleClient:
    def __init__(self, token):
        self.token = token
        
    def get_data(self):
        # TODO: Modify this method to use a requests Session instead of making a one-off request.
        # You will need to add a Session to the __init__ method.
        import requests
        return requests.get("https://api.example.com/data", headers={"Auth": self.token})


# Tier 3: Build
class GitHubRepoClient:
    # TODO: Build a client that initializes a requests.Session with a base URL of "https://api.github.com".
    # Add a method `get_repo(owner, repo_name)` that makes a GET request to `/repos/{owner}/{repo_name}`
    # and returns the JSON dictionary.
    pass


# Tier 4: Debug
class BuggyApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        import requests
        self.session = requests.Session()

    def make_request(self, endpoint):
        # TODO: This method has a bug that will cause URL formation errors (e.g. missing slashes or double slashes).
        # Fix the URL joining logic to be robust regardless of whether base_url ends with a slash or endpoint begins with one.
        
        # Buggy code:
        url = self.base_url + endpoint
        return self.session.get(url).json()
