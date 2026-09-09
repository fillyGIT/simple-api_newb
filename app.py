from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import psycopg
import json

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
            self.wfile.write(b'{"service": "simple-api", "version": "1.2"}')
        
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "running"}')
    
        elif self.path == "/items":
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM items;")
                rows = cur.fetchall()

            items = []

            for row in rows:
                items.append({
                    "id": row[0],
                    "name": row[1]
                })

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(items).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found\n")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = json.loads(body)
        name = data["name"]

        with conn.cursor() as cur:
            cur.execute(
               "INSERT INTO items (name) VALUES (%s);",
               (name,)
            )


        conn.commit()
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"name": name}).encode())

db_host = os.getenv("DB_HOST")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

conn = psycopg.connect(
    host=db_host,
    dbname=db_name,
    user=db_user,
    password=db_password
)

port = int(os.getenv("PORT", "8000"))
server = HTTPServer(("0.0.0.0", port), Handler)

print(f"simple-api listening on port{port}")
server.serve_forever()

