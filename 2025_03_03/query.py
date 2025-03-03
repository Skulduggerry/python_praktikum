from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer


class Query:
    def __init__(self, title: str, options: list):
        self.title = title
        self.options = options
        self.user_choices = {}


current_query: Query | None = None

class DynamicRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/create.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(
                """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8" />
                    <title>Abfrage Erstellen</title>
                    <style>
                    body { padding: 10vh 10vw; background: #eee; color: #444; font-family: sans; font-size: 12pt; }
                    table { width: 100%; background: #fff; border: 1px solid #aaa; margin: 10px 0; }
                    td { width: 10vw; padding: 10px; }
                    th { width: 10vw; padding: 10px; background: #ccd; }
                    input[type=text] { padding: 5px 10px; font-size: 12pt; width: 80%; height: 30px; background: #eef; }
                    input[type=submit] { padding: 10px 20px; font-size: 16pt; }
                    </style>
                </head>
                <body>
                    <form action="/create.html" method="POST">
                    <h1>Neue Abfrage erstellen</h1>
                    <table>
                        <tr>
                            <th>Titel</th>
                            <th>Option 1</th>
                            <th>Option 2</th>
                            <th>Option 3</th>
                            <th>Option 4</th>
                            <th>Option 5</th>
                        </tr>
                        <tr>
                            <td><input type="text" name="title" placeholder="Titel der Abfrage" autofocus/></td>
                            <td><input type="text" name="option0" placeholder="Was? Wann? Wo?"/></td>
                            <td><input type="text" name="option1" placeholder="Was? Wann? Wo?"/></td>
                            <td><input type="text" name="option2" placeholder="Was? Wann? Wo?"/></td>
                            <td><input type="text" name="option3" placeholder="Was? Wann? Wo?"/></td>
                            <td><input type="text" name="option4" placeholder="Was? Wann? Wo?"/></td>
                        </tr>
                    </table>
                    <input type="submit" value="erstellen"/>
                    </form>
                </body>
                </html>
                """, "utf-8"
            ))
        elif self.path == "/participate.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            option_row = ""
            for option in current_query.options:
                option_row += f"<th>{option}</th>\n"

            participant_rows = ""
            for participant, choices in current_query.user_choices.items():
                row = f"""
                <tr>
                <td>{participant}</td>
                """
                for choice in choices:
                    row += f"<td class={'ja' if choice else 'nein'}></td>\n"
                row += "</tr>\n"
                participant_rows += row

            user_option_row = '<td><input type="text"     name="name" placeholder="Dein Name" autofocus/></td>'
            for i in range(len(current_query.options)):
                user_option_row += f'<td><input type="checkbox" name="answer{i}" value="ja"/></td>'

            self.wfile.write(bytes(
                f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8" />
                    <title>{current_query.title}</title>
                    <style>
                    body {{ padding: 10vh 10vw; background: #eee; color: #444; font-family: sans; font-size: 12pt; }}
                    table {{ width: 100%; background: #fff; border: 1px solid #aaa; margin: 10px 0; border-collapse: collapse; }}
                    td {{ width: 10vw; padding: 10px; border: 1px solid #666; }}
                    th {{ width: 10vw; padding: 10px; border: 1px solid #666; background: #ccd; }}
                    input[type=text] {{ padding: 5px 10px; font-size: 12pt; width: 80%; height: 30px; background: #eef; }}
                    input[type=checkbox] {{ margin: 5px auto; width: 100%; height: 30px; }}
                    input[type=submit] {{ padding: 10px 20px; font-size: 16pt; }}
                    .ja {{ background: #8f8; text-align: center; }}
                    .nein {{ background: #f88; text-align: center; }}
                    .ja::before {{ content: "ja" }}
                    .nein::before {{ content: "nein" }}
                    </style>
                </head>
                <body>
                    <form action="/participate.html" method="POST">
                    <h1>{current_query.title}</h1>
                    <table>
                        <tr>
                            <th>Name</th>
                            {option_row}
                        </tr>
                        {participant_rows}
                        <tr>
                            {user_option_row}
                        </tr>
                    </table>
                    <input type="submit" value="eintragen"/>
                    </form>
                </body>
                </html>
                """, "utf-8"
            ))

    def do_POST(self):
        from urllib.parse import parse_qs
        fields = {}
        for key, value in parse_qs(self.rfile.read(int(self.headers['content-length']))).items():
            fields[key.decode("utf-8")] = value[0].decode("utf-8")

        if self.path == "/create.html":
            title = fields["title"]
            options = []
            for idx in range(5):
                if f"option{idx}" in fields:
                    options.append(fields[f"option{idx}"])
            global current_query
            current_query = Query(title, options)

        if self.path == "/participate.html":
            name = fields["name"]
            choices = []
            for idx in range(len(current_query.options)):
                choices.append(f"answer{idx}" in fields)
            current_query.user_choices[name] = choices

        self.send_response(302)
        self.send_header("Location", "/participate.html")
        self.end_headers()


TCPServer.allow_reuse_address = True
with TCPServer(("", 8000), DynamicRequestHandler) as httpd:
    httpd.serve_forever()
