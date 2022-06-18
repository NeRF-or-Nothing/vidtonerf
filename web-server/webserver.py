from flask import Flask


class WebServer:
    def __init__(self, port: int = 5000):
        self.app = Flask(__name__)
        self.port = port

    def run(self):
        self.add_routes()

        self.app.run(port=self.port)

    def add_routes(self):
        @self.app.route("/")
        def hello_world():
            return "Hello World"

        @self.app.route("/<name>")
        def hello_name(name: str):
            return f"Hello {name}"
