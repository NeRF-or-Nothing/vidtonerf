from uuid import uuid4, UUID
import json
from flask import Flask, request, make_response, send_file, send_from_directory, url_for

app = Flask(__name__)

@app.route('/test')
def get_webServer():
    return 'hello'

@app.route("/video/publish", methods=["POST", "PUT"])
def pub_video():
    video_file = request.files.get("file")
    print("VIDEO_FILE", video_file)
    # TODO: set uuid equal to a "handle_outcoming_video", aka if the video is already done rendering.
    # uuid = self.cservice.get_nerf_video_path(video_file)
    f = open("publish_video.txt", "x")
    data = json.load(f)
    data["uuid"] = uuid
    if (uuid is None):
        response = make_response("ERROR", 404)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    response = make_response(uuid, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/video", methods=["POST", "PUT"])
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
    f = open("publish_video.txt", "x")
    data = json.load(f)
    data["uuid"] = "testuuid"
    if(uuid is None):
        response = make_response("ERROR", 404)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route("/video/<vidid>", methods=["GET"])
def send_video(vidid: str):
    # TODO: Change routing to serve rendered videos
    try:
        if(is_valid_uuid(vidid)):
            path = os.path.join(
                os.getcwd(), "data/raw/videos/" + vidid + ".mp4")
            response = make_response(
                send_file(path, as_attachment=True), 200)
        else:
            response = make_response("Error: invalid UUID", 404)
    except Exception as e:
        print(e)
        response = make_response("Error: does not exist", 403)

    return response

@app.route("/nerfvideo/<vidid>", methods=["GET"])
def send_nerf_video(vidid: str):
    ospath = None
    status_str = "Processing"
    if is_valid_uuid(vidid):
        ospath = self.cservice.get_nerf_video_path(vidid)
    # Could change this to return both
    if ospath == None or not os.path.exists(ospath):
        response = make_response(status_str, 404)
    else:
        status_str = "Video ready"
        response = make_response(
            send_file(ospath, as_attachment=True), 200)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run()