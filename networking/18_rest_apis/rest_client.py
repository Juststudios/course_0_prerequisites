import requests
import json

# We will use JSONPlaceholder, a free fake API for testing and prototyping.
BASE_URL = "https://jsonplaceholder.typicode.com"

def get_posts():
    """GET: Retrieve a list of resources."""
    print("--- GET /posts ---")
    response = requests.get(f"{BASE_URL}/posts?userId=1")
    if response.status_code == 200:
        posts = response.json()
        print(f"Retrieved {len(posts)} posts for User 1.")
        print(f"First post title: {posts[0]['title']}\n")
    else:
        print(f"Error: {response.status_code}")

def get_single_post(post_id: int):
    """GET: Retrieve a specific resource."""
    print(f"--- GET /posts/{post_id} ---")
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    if response.status_code == 200:
        post = response.json()
        print(f"Post {post_id} Title: {post['title']}\n")
    else:
        print(f"Error: {response.status_code}")

def create_post():
    """POST: Create a new resource."""
    print("--- POST /posts ---")
    payload = {
        "title": "Learning REST APIs",
        "body": "REST stands for Representational State Transfer.",
        "userId": 1
    }
    # requests.post(..., json=payload) automatically sets Content-Type to application/json
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    
    if response.status_code == 201: # 201 Created is the standard REST status for successful POST
        new_post = response.json()
        print(f"Successfully created post! Assigned ID: {new_post.get('id')}\n")
    else:
        print(f"Error: {response.status_code}")

def update_post_put(post_id: int):
    """PUT: Replace an entire resource."""
    print(f"--- PUT /posts/{post_id} ---")
    payload = {
        "id": post_id,
        "title": "Updated Title via PUT",
        "body": "This completely replaces the old resource.",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=payload)
    if response.status_code == 200:
        print(f"Successfully replaced post {post_id}: {response.json()['title']}\n")

def update_post_patch(post_id: int):
    """PATCH: Partially update a resource."""
    print(f"--- PATCH /posts/{post_id} ---")
    payload = {
        "title": "Updated Title via PATCH"
        # Notice we don't send the body or userId. We are only updating the title.
    }
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", json=payload)
    if response.status_code == 200:
        print(f"Successfully patched post {post_id}: {response.json()['title']}\n")

def delete_post(post_id: int):
    """DELETE: Remove a resource."""
    print(f"--- DELETE /posts/{post_id} ---")
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    if response.status_code in (200, 202, 204): 
        # 204 No Content is very common for successful DELETE requests
        print(f"Successfully deleted post {post_id} (Status: {response.status_code})\n")
    else:
        print(f"Failed to delete. Status: {response.status_code}")

if __name__ == "__main__":
    get_posts()
    get_single_post(1)
    create_post()
    update_post_put(1)
    update_post_patch(1)
    delete_post(1)
    
    print("Note: Because this is a mock API, POST/PUT/PATCH/DELETE requests return successful status codes but do not actually modify the server database.")
