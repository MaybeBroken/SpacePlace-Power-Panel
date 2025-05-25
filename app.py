import os
from subprocess import run
import websockets as ws
import asyncio
import http.server


# Logic for WS server here






PORT = 4443
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path in ('/', '/index.htm', '/index.html'):
            self.path = '/index.htm'
        return super().do_GET()

def http_server():
    httpd = http.server.ThreadingHTTPServer(('localhost', PORT), Handler)

    print(f"Serving HTTP on http://localhost:{PORT}/")
    try:
        import socket
        with socket.create_connection(("localhost", PORT), timeout=2):
            print(f"Local connectivity check: OK (http://localhost:{PORT}/)")
    except Exception as e:
        print(f"Warning: Could not connect to http://localhost:{PORT}/ from localhost. Error: {e}")
    httpd.serve_forever()

def websocket_server():
    async def handler(websocket):
        print(f"WebSocket connection established from {websocket.remote_address}")
        try:
            while True:
                message = await websocket.recv()
                await websocket.send(f"Echo: {message}")
        except ws.ConnectionClosed:
            print("WebSocket connection closed")

    async def start():
        server = await ws.serve(handler, "localhost", 8765)
        print("WebSocket server started on ws://localhost:8765/")
        try:
            await server.wait_closed()
        except KeyboardInterrupt:
            print("WebSocket server stopped")

    asyncio.run(start())

if __name__ == "__main__":
    print("Starting HTTP and WebSocket servers...")

    # Start HTTP server in a separate thread
    import threading
    http_thread = threading.Thread(target=http_server, daemon=True)
    http_thread.start()

    # Start WebSocket server
    websocket_server()