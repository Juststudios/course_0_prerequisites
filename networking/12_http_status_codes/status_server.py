from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class StatusDemoHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/":
            # 200 OK
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Success! 200 OK")
            
        elif self.path == "/created":
            # 201 Created (normally used with POST, but just for demo)
            self.send_response(201)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Resource Created! 201 Created")
            
        elif self.path == "/redirect":
            # 301 Moved Permanently
            self.send_response(301)
            # The Location header tells the browser where to go
            self.send_header('Location', '/')
            self.end_headers()
            
        elif self.path == "/bad":
            # 400 Bad Request
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"You sent a bad request! 400 Bad Request")
            
        elif self.path == "/secret":
            # 401 Unauthorized or 403 Forbidden
            # Let's return 403 for demo
            self.send_response(403)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Forbidden! You do not have access. 403 Forbidden")
            
        elif self.path == "/crash":
            # 500 Internal Server Error
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"The server encountered an error. 500 Internal Server Error")
            
        else:
            # 404 Not Found
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Path not found. 404 Not Found")

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, StatusDemoHandler)
    print(f"Status Code Demo Server running on port {port}...")
    print("Try browsing to:")
    print("  http://localhost:8080/")
    print("  http://localhost:8080/created")
    print("  http://localhost:8080/redirect")
    print("  http://localhost:8080/bad")
    print("  http://localhost:8080/secret")
    print("  http://localhost:8080/crash")
    print("  http://localhost:8080/does_not_exist")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()
