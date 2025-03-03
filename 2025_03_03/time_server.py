from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import time

class DynamicRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/uhrzeit.html":
            # "programmierte" Seite senden
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(
                """
                <!DOCTYPE html>
                <html>
                <head>
                <title>Mein Python Web-Server</title>
                </head>""", "utf-8"))
            self.wfile.write(bytes(
                """
                <body>
                <h1>Request: """ + self.path + """</h1>
				<p>""" + time.ctime() + """</p>
				</body>
				</html>
				""", "utf-8"))
        else:
            # Weiterleitung an die Oberklasse
            SimpleHTTPRequestHandler.do_GET(self)

TCPServer.allow_reuse_address = True
with TCPServer(("", 8000), DynamicRequestHandler) as httpd:
    httpd.serve_forever()
