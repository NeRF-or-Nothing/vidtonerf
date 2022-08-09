import argparse
import os
import magic
from uuid import uuid4, UUID

from flask import Flask, request, make_response, send_file

from services.scene_service import ClientService, SceneService

def is_valid_uuid(value):
    try:
        UUID(str(value))
        return True
    except ValueError:
        return False

class WebServer:
    def __init__(self, args: argparse.Namespace, cserv: ClientService) -> None:
        self.app = Flask(__name__)
        self.args = args
        self.cservice = cserv

    def run(self) -> None:
        self.app.logger.setLevel(
            int(self.args.log)
        ) if self.args.log.isdecimal() else self.app.logger.setLevel(self.args.log)

        self.add_routes()
        
        # TODO: Change this to work based on where Flask server starts. Also, use the actual ip address
        ### self.sserv.base_url = request.remote_addr

        self.app.run(port=self.args.port)

    def add_routes(self) -> None:
        @self.app.route("/")
        def hello_world():
            return "Do not access"

        @self.app.route("/video", methods=["POST", "PUT"])
        def recv_video():
            """
            Must decide if we want to hang here until video is done,
            or return a 20x received and let the front-end query an endpoint
            given a cookie to see if the video is done periodically
            """
            video_file = request.files.get("file")
            print("VIDEO FILE", video_file)
            # TODO: UUID4 is cryptographically secure on CPython, but this is not guaranteed in the specifications.
            # Might want to change this.
            # TODO: Don't assume videos are in mp4 format
            uuid = self.cservice.handle_incoming_video(video_file)
            if(uuid is None):
                response = make_response("ERROR")
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            
            # TODO: now pass to nerf/tensorf/colmap/sfm, and decide if synchronous or asynchronous
            # will we use a db for cookies/ids?
                
            response = make_response(uuid)
            response.headers['Access-Control-Allow-Origin'] = '*'

            return response

        @self.app.route("/video/<vidid>", methods=["GET"])
        def send_video(vidid: str):
            try:
                if(is_valid_uuid(vidid)):
                    path = os.path.join(os.getcwd(), "data/raw/videos/" + vidid + ".mp4")
                    response = make_response(send_file(path, as_attachment=True))
                else:
                    response = make_response("Error: invalid UUID")
            except Exception as e:
                print(e)
                response = make_response("Error: does not exist")
            
            # TODO: Remove only after website uses final NeRF data
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
            
