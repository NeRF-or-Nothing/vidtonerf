import os
import requests
import json
from models.scene import SceneManager, Video
from services.queue_service import RabbitMQService, rabbit_read_out
from uuid import uuid4, UUID
from werkzeug.utils import secure_filename

def read_sfm(client, jsonstr):
    try:
        obj = json.loads(jsonstr)
    except ValueError:
        return
    # load into mongodb and download files from server
    for link, filename in zip(obj["filelinks"], obj["filenames"]):
        data = requests.get(link)
        # TODO: This is literally just saving files that are being arbitrarily served up.
        # Needs to be more secure.
        path = os.path.join(os.getcwd(), "data/sfm/" + filename)
        with open(path, 'wb') as f:
            f.write(data.content)
        
def read_nerf(client, json):
    try:
        obj = json.loads(jsonstr)
    except ValueError:
        return
    # load into mongodb and download files from server
    

class SceneService:
    def __init__(self, queue: RabbitMQService):
        self.manager = SceneManager(MongoClient(host="localhost",port=27017))
        self.queue = queue
        
        # Needs to be set as soon as webserver is started
        self.base_url = None
     
    def send_nerf_json(self, uuid):
        pass
        
    def add_video(self, uuid):
        vidjson = {}
        vidjson["filelinks"] = []
        vidjson["filelinks"].append(self.base_url + "/video/" + uuid)
        # Currently, filenames are associated with filelinks only by order.
        # We may want to change this.
        vidjson["filenames"] = []
        # TODO: Should depend on actual file name
        vidjson["filenames"].append(uuid + ".mp4")
        
        send_str = json.dumps(vidjson)
        self.queue.post_video(send_str)
        # TODO: set up new scene in Mongo and add the uuid and the filename
    
    def add_sfm(self, uuid):
        pass
        
    def get_nerf(self, uuid):
        pass

from pymongo import MongoClient
class ClientService:
    def __init__(self):
        mongoclient = MongoClient(host="localhost",port=27017)
        self.manager = SceneManager(mongoclient)
        #self.queue = queue

    def handle_incoming_video(self, video_file):

        # receive video and check for validity
        file_name = secure_filename(video_file.filename)
        if file_name == '':
            print("ERROR: file not received")
            return None

        file_ext = os.path.splitext(file_name)[1]
        if file_ext != ".mp4":
            print("ERROR: improper file extension uploaded")
            return None

        # generate new id and save to file with db record
        uuid = str(uuid4())
        video_name = uuid + ".mp4"
        videos_folder = "data/raw/videos"
        video_file_path = os.path.join(videos_folder,video_name)
        
        video_file.save(video_file_path)

        video = Video(video_file_path)
        self.manager.set_video(uuid, video)

        # create rabbitmq job for sfm
        #TODO

        return uuid





