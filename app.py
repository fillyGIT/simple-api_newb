from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"simple-api is running\n")

        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"healthy\n")

        elif self.path == "/version":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"service": "simple-api", "version": "1.1"}')
        
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "running"}')
    
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found\n")


server = HTTPServer(("0.0.0.0", 8000), Handler)

print("simple-api listening on port 8000")
server.serve_forever()

