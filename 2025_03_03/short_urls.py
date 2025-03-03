from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

url_map = {}
curr_index = 0

class DynamicRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if len(self.path) < 6:
            id = int(self.path.replace("/", ""))
            if not id in url_map:
                self.send_response(404)
                self.end_headers()
                return
            self.send_response(302)
            self.send_header("Location", url_map[id])
            self.end_headers()
        elif self.path == "/create.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(
                """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8" />
                    <title>Kurze URLs</title>
                    <style>
                        body { padding: 10vh 10vw; background: #eee; color: #444; font-family: sans; font-size: 12pt; }
                        input[type=text] { padding: 5px 10px; font-size: 12pt; width: 80%; height: 30px; background: #eef; }
                        input[type=submit] { padding: 10px 20px; font-size: 16pt; }
                    </style>
                </head>
                <body>
                <form action="/create.html" method="POST">
                    <h1>Kurze URL Erstellen</h1>
                    <input type="text" name="long" placeholder="lange URL"/>
                    <input type="submit" value="erstellen"/>
                </form>
                </body>
                </html>
                """, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global curr_index
        from urllib.parse import parse_qs
        fields = {}
        for key, value in parse_qs(self.rfile.read(int(self.headers['content-length']))).items():
            fields[key.decode("utf-8")] = value[0].decode("utf-8")

        if self.path == "/create.html":
            id = curr_index
            curr_index += 1
            long_url = fields["long"]
            url_map[id] = long_url

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(
                """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8" />
                    <title>Kurze URLs</title>
                    <style>
                        body { padding: 10vh 10vw; background: #eee; color: #444; font-family: sans; font-size: 12pt; }
                    </style>
                </head>
                <body>
                <h1>Kurze URL erstellt</h1>
                <p>http://localhost:8000/""" + str(id) + """</p>
                <p>""" + long_url + """</p>
                </body>
                </html>
                """, "utf-8"))


TCPServer.allow_reuse_address = True
with TCPServer(("", 8000), DynamicRequestHandler) as httpd:
    httpd.serve_forever()
