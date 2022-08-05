
import json
from models.scene import SceneManager
from services.queue_service import RabbitMQService

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
        vidjson["http_path"] = self.base_url + "/videos/" + uuid
        send_str = json.dumps(vidjson)
        self.queue.post_video(send_str)
        # TODO: set up new scene in Mongo and add the uuid and the filename
    
    def add_sfm(self, uuid):
        pass
        
    def get_nerf(self, uuid):
        pass
