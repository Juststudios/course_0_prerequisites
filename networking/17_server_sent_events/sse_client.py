import httpx
import time
import json
from dataclasses import dataclass

@dataclass
class ServerSentEvent:
    event: str
    data: str
    id: str
    retry: int

def parse_sse_line(line: str, current_event: ServerSentEvent) -> bool:
    """
    Parses a single line of an SSE stream and updates the current_event object.
    Returns True if the event is complete (empty line received), False otherwise.
    """
    if not line:
        # An empty line indicates the end of an event
        return True
        
    if line.startswith(':'):
        # Lines starting with a colon are comments, ignore them
        return False
        
    if ':' in line:
        field, value = line.split(':', 1)
        # The spec says to strip a single leading space if present
        if value.startswith(' '):
            value = value[1:]
            
        if field == 'event':
            current_event.event = value
        elif field == 'data':
            # Data can be multiple lines, so we append with a newline if data already exists
            if current_event.data:
                current_event.data += '\n' + value
            else:
                current_event.data = value
        elif field == 'id':
            current_event.id = value
        elif field == 'retry':
            try:
                current_event.retry = int(value)
            except ValueError:
                pass
                
    return False

def consume_sse(url: str):
    """
    Connects to an SSE endpoint and yields parsed ServerSentEvent objects.
    """
    headers = {
        'Accept': 'text/event-stream',
        'Cache-Control': 'no-cache',
    }
    
    print(f"Connecting to SSE endpoint: {url}")
    
    # We use httpx stream to read the response line by line
    with httpx.Client() as client:
        with client.stream("GET", url, headers=headers) as response:
            response.raise_for_status()
            
            # Initialize an empty event
            current_event = ServerSentEvent(event="message", data="", id="", retry=0)
            
            for line in response.iter_lines():
                # parse_sse_line returns True when it hits an empty line (\n\n)
                is_complete = parse_sse_line(line, current_event)
                
                if is_complete and current_event.data:
                    # Yield the completed event
                    yield current_event
                    # Reset for the next event
                    current_event = ServerSentEvent(event="message", data="", id="", retry=0)

if __name__ == "__main__":
    # We will use a public testing endpoint for SSE.
    # Wikimedia provides a public SSE stream of all recent edits across Wikipedia!
    url = "https://stream.wikimedia.org/v2/stream/recentchange"
    
    print("Listening for Wikipedia edits (showing first 5)...")
    try:
        count = 0
        for event in consume_sse(url):
            # Parse the JSON data payload
            try:
                data = json.loads(event.data)
                user = data.get('user', 'Unknown')
                title = data.get('title', 'Unknown')
                wiki = data.get('wiki', 'Unknown')
                print(f"[{wiki}] {user} edited: {title}")
            except json.JSONDecodeError:
                print(f"Raw data: {event.data[:100]}...")
                
            count += 1
            if count >= 5:
                break
    except KeyboardInterrupt:
        print("\nStopped.")
