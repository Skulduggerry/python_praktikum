from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from random import random

trials = 0  # number of trials already used
target = 0  # secret number to be guessed


def get_site(content):
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
	    <meta charset="utf-8" />
	    <title>Zahlen raten</title>
	    <style>
        	body {{ padding: 10vh 10vw; background: #def; text-align: center; font-size: 400%; }}
	    input {{ font-size: 100%; padding: 10px 20px; width: 30%; }}
	    </style>
        </head>
        <body>
        {content}
        </body>
        </html>"""


class DynamicRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/start":
            global target
            global trials
            target = 1 + int(100 * random())
            trials = 0
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            site = get_site(
                """
                <h1>Willkommen</h1>
                <p>beim Zahlen-Raten!</p>
                <p><a href="/guess">zum Spiel</a></p>
                """)
            self.wfile.write(bytes(site, "utf-8"))
        elif self.path == "/guess":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            site = get_site(
                f"""
                <p>Bisherige Versuche: {trials}</p>
                <p><form method="POST" action="/result">
                <input type="number" name="guess" min="1" max="100" step="1"/>
                <input type="submit" value="Raten"/>
                </form></p>
                """)
            self.wfile.write(bytes(site, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        from urllib.parse import parse_qs
        fields = {}
        for key, value in parse_qs(self.rfile.read(int(self.headers['content-length']))).items():
            fields[key.decode("utf-8")] = value[0].decode("utf-8")

        if self.path == "/result":
            global trials
            trials += 1
            number = int(fields["guess"])
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if number == target:
                site = get_site(
                    f"""
                            <h1>Richtig!</h1>
                            <p>Du hast das Rätsel nach {trials} Versuchen gelöst!</p>
                            <p><a href="/start">noch einmal spielen</a></p>
                            """)
                self.wfile.write(bytes(site, "utf-8"))
            else:
                site = get_site(
                    f"""
                            <h1>Falsch!</h1>
                            <p>Die richtige Zahl ist {'größer' if target > number else 'kleiner'} als {number}.</p>
                            <p><a href="/guess">weiter raten</a></p>
                            """)
                self.wfile.write(bytes(site, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

TCPServer.allow_reuse_address = True
with TCPServer(("", 8000), DynamicRequestHandler) as httpd:
    httpd.serve_forever()
