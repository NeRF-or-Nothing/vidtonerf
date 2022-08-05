
from models.scene import SceneManager
from services.queue_service import RabbitMQService

class SceneService:
    def __init__(self, queue: RabbitMQService):
        self.manager = SceneManager()
        self.queue = queue
        
    def generate_sfm_json(self, uuid):
        http_path = self.base_url + "/videos/" + uuid
        self.scenes = ToSfmData(http_path)
        send_str = json.dumps(http_path)
     
    def generate_nerf_json(self, uuid):
        pass
        
    def add_video(self, uuid):
        pass
    
    def add_sfm(self, uuid):
        pass
        
    def get_nerf(self, uuid):
        pass
