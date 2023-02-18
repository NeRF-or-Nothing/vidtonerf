import argparse
import os
from pickle import TRUE
#import magic
from uuid import uuid4, UUID

from flask import Flask, request, make_response, send_file, send_from_directory, url_for

from services.scene_service import ClientService

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

        self.app.run(host='0.0.0.0',port=self.args.port)

    def add_routes(self) -> None:

        #TODO: Write error handling so the whole server doesn't crash when the user sends incorrect data.
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
            # TODO: Change routing to serve rendered videos
            try:
                if(is_valid_uuid(vidid)):
                    path = os.path.join(os.getcwd(), "data/raw/videos/" + vidid + ".mp4")
                    response = make_response(send_file(path, as_attachment=True))
                else:
                    response = make_response("Error: invalid UUID")
            except Exception as e:
                print(e)
                response = make_response("Error: does not exist")
           
            return response
            
        @self.app.route("/nerfvideo/<vidid>", methods=["GET"])
        def send_nerf_video(vidid: str):
            ospath = None
            status_str = "Processing"
            if is_valid_uuid(vidid):
                ospath = self.cservice.get_nerf_video_path(vidid)
            # Could change this to return both
            if ospath == None or not os.path.exists(ospath):
                response = make_response(status_str)
            else:
                status_str = "Video ready"
                response = make_response(send_file(ospath, as_attachment=True))
                
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        @self.app.route("/worker-data/<path:path>")
        def send_worker_data(path):
            # serves data directory for workers to pull any local data
            # TODO make this access secure
            return send_from_directory('data',path[5:])
            
        
