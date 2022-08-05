import os
import requests
import json
from models.scene import SceneManager
from services.queue_service import RabbitMQService, rabbit_read_out

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
        with open(path, 'w') as f:
            f.write(data)
        
        
    
def read_nerf(client, json):
    try:
        obj = json.loads(jsonstr)
    except ValueError:
        return
    # load into mongodb and download files from server
    

class SceneService:
    def __init__(self, queue: RabbitMQService):
        self.manager = SceneManager()
        self.queue = queue
        
        # Needs to be set as soon as webserver is started
        self.base_url = None
     
    def send_nerf_json(self, uuid):
        pass
        
    def add_video(self, uuid):
        vidjson = {}
        vidjson["filelinks"] = []
        vidjson["filelinks"].append(self.base_url + "/videos/" + uuid)
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
