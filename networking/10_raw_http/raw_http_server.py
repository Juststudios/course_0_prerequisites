import socket

def run_raw_http_server(host='127.0.0.1', port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening for HTTP requests on http://{host}:{port}")

    try:
        while True:
            client, addr = server.accept()
            with client:
                request_data = client.recv(1024).decode('utf-8')
                if not request_data:
                    continue
                
                # Print the raw request
                print("--- Incoming Request ---")
                print(request_data)
                
                # Parse the request line
                lines = request_data.split('\r\n')
                request_line = lines[0]
                method, path, protocol = request_line.split(' ')
                
                # Prepare response body
                if path == "/":
                    body = "<h1>Welcome to the Raw HTTP Server!</h1>"
                elif path == "/api":
                    body = '{"status": "success", "message": "API endpoint reached"}'
                else:
                    body = "<h1>404 Not Found</h1>"
                
                # Prepare headers
                status_line = "HTTP/1.1 200 OK\r\n" if path in ["/", "/api"] else "HTTP/1.1 404 Not Found\r\n"
                content_type = "Content-Type: text/html\r\n" if path != "/api" else "Content-Type: application/json\r\n"
                content_length = f"Content-Length: {len(body)}\r\n"
                
                # Construct the full raw HTTP response
                # Remember the \r\n to separate headers from body!
                response = status_line + content_type + content_length + "\r\n" + body
                
                # Send the response
                client.sendall(response.encode('utf-8'))
                
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server.close()

if __name__ == "__main__":
    run_raw_http_server()
