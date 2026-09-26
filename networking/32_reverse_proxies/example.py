import http.server
import socketserver
import urllib.request

# A VERY simple Python reverse proxy demonstrating the concept
class ReverseProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # We forward the request to an upstream server (e.g., httpbin.org)
        upstream_url = "http://httpbin.org" + self.path
        
        req = urllib.request.Request(upstream_url)
        # Pass along important headers
        req.add_header('X-Forwarded-For', self.client_address[0])
        
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read()
                
                # Send back to client
                self.send_response(response.status)
                for key, val in response.getheaders():
                    self.send_header(key, val)
                self.end_headers()
                self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReverseProxyHandler) as httpd:
        print(f"Simple Python Reverse Proxy running on port {PORT}")
        httpd.serve_forever()
