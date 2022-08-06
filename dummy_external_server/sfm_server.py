import argparse
import os
import magic

from flask import Flask, make_response, send_file

class SfmServer:
    def __init__(self, args: argparse.Namespace) -> None:
        self.app = Flask(__name__)
        self.args = args

    def run(self) -> None:
        self.app.logger.setLevel(
            int(self.args.log)
        ) if self.args.log.isdecimal() else self.app.logger.setLevel(self.args.log)

        self.add_routes()

        self.app.run(port=self.args.port)

    def add_routes(self) -> None:

        @self.app.route("/<path>", methods=["GET"])
        def send_video(path: str):
            try:
                path = os.path.join(os.getcwd(), "data/" + path)
                response = make_response(send_file(path))
            except Exception as e:
                response = make_response("Error: does not exist")
            return response
