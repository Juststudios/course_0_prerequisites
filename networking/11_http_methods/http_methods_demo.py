from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# A simple in-memory database
database = {
    "1": {"name": "Alice", "role": "Admin"},
    "2": {"name": "Bob", "role": "User"}
}

class MethodDemoHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests (Read)"""
        if self.path == "/users":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(database).encode('utf-8'))
        else:
            self.send_error(404, "Path not found")

    def do_POST(self):
        """Handle POST requests (Create)"""
        if self.path == "/users":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            new_user = json.loads(post_data.decode('utf-8'))
            
            # Generate a new ID
            new_id = str(len(database) + 1)
            database[new_id] = new_user
            
            self.send_response(201) # 201 Created
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {"message": "User created", "id": new_id}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Path not found")
            
    def do_DELETE(self):
        """Handle DELETE requests (Delete)"""
        if self.path.startswith("/users/"):
            user_id = self.path.split("/")[-1]
            if user_id in database:
                del database[user_id]
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "User deleted"}).encode('utf-8'))
            else:
                self.send_error(404, "User not found")
        else:
            self.send_error(404, "Path not found")

def run(server_class=HTTPServer, handler_class=MethodDemoHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    print("Test with:")
    print("  curl -X GET http://localhost:8000/users")
    print("  curl -X POST -H \"Content-Length: 35\" -d '{\"name\":\"Charlie\", \"role\":\"User\"}' http://localhost:8000/users")
    print("  curl -X DELETE http://localhost:8000/users/1")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()
