import json

# 1. A Raw ASGI Application
# This is what FastAPI looks like under the hood! No framework involved.

async def simple_app(scope, receive, send):
    """
    A simple ASGI application that echoes back the request path and method.
    """
    # 1. Check the connection type (ASGI supports 'http', 'websocket', and 'lifespan')
    if scope['type'] != 'http':
        # If it's not HTTP, we just return (ignore it).
        return

    # 2. Read basic info from the scope
    method = scope['method']
    path = scope['path']
    
    # 3. Create a JSON response
    response_data = {
        "message": "Hello from raw ASGI!",
        "method": method,
        "path": path
    }
    
    # JSON strings must be encoded to bytes before sending
    body_bytes = json.dumps(response_data).encode('utf-8')
    
    # 4. Send the HTTP Headers
    # We must send an 'http.response.start' event first
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'application/json'),
            (b'content-length', str(len(body_bytes)).encode('utf-8'))
        ]
    })
    
    # 5. Send the HTTP Body
    # Then we send an 'http.response.body' event
    await send({
        'type': 'http.response.body',
        'body': body_bytes,
        # 'more_body': False is implied if omitted, meaning this is the end of the response.
    })

# 2. An ASGI Middleware
# Middleware is just an ASGI app that wraps another ASGI app!

class TimingMiddleware:
    """
    Middleware that measures how long a request takes and adds a custom header.
    """
    def __init__(self, app):
        # Store the wrapped application
        self.app = app
        
    async def __call__(self, scope, receive, send):
        import time
        start_time = time.time()
        
        # We need to intercept the `send` function so we can inject our header 
        # before the `http.response.start` event goes out to the server.
        async def custom_send(message):
            if message['type'] == 'http.response.start':
                elapsed = time.time() - start_time
                header_val = f"{elapsed:.4f}s".encode('utf-8')
                
                # Append our custom header
                message['headers'].append((b'x-process-time', header_val))
                
            # Call the original send function
            await send(message)
            
        # Call the underlying application, passing our modified send function
        await self.app(scope, receive, custom_send)

# Wrap our simple_app in the middleware
wrapped_app = TimingMiddleware(simple_app)

# To run this file:
# pip install uvicorn
# uvicorn raw_asgi:wrapped_app --reload
