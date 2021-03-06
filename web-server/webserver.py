import argparse
import os
import magic
from flask import Flask, request
from werkzeug import secure_filename


class WebServer:
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
        @self.app.route("/")
        def hello_world():
            return "You shouldn't be here"

        @self.app.route("/<name>")
        # remove later
        def hello_name(name: str):
            return f"Hello {name}"

        @self.app.route("/video", methods=["POST"])
        def recv_video():
            """
            Must decide if we want to hang here until video is done,
            or return a 20x received and let the front-end query an endpoint
            given a cookie to see if the video is done periodically
            """
            video = request.files.get("file")
            video_name = "videos/" + secure_filename(video.filename)
            video.save(os.path.join(os.getcwd(), video_name))

            try:
                vid_type = magic.from_file(video_name, mime=True)
                self.app.logger.info("video type: %s", vid_type)
            except Exception as e:
                return "Error: couldn't figure out file type " + repr(e)

            # now pass to nerf/tensorf/colmap/sfm, and decide if synchronous or asynchronous
            # will we use a db for cookies/ids?

            return "Video Received"

        @self.app.route("/video", methods=["GET"])
        def send_video():
            """
            Placeholder for if/when the frontend queries this periodically to see if it's done
            """

            # pseudocode
            # video = db.get_video(user_id/session_id)
            # if video.done:
            #     return video.get_video_data()
            # else:
            #     return "Video not done"

    # Eric moment
    def write_to_colmap(self, video_fp: str):
        pass

    def write_to_nerf(self, video_fp: str):
        pass

    def write_to_tensorf(self, video_fp: str):
        pass
