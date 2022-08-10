
import pika, os, logging
from models.scene import Video, Sfm, Nerf
import json

def rabbit_read_out(callback, queue):
    # TODO: Add security
    credentials = pika.PlainCredentials('admin', 'password123')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)
    channel.start_consuming()
    

class RabbitMQService:
    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    def __init__(self):
        credentials = pika.PlainCredentials('admin', 'password123')
        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        # Change this ->
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='sfm-in')
        self.channel.queue_declare(queue='sfm-out')
        self.channel.queue_declare(queue='nerf-in')
        self.channel.queue_declare(queue='nerf-out')

        #TODO: make this dynamic from config file
        self.base_url = "http://localhost:5000/"
        

    def to_url(self,file_path):
        return self.base_url+"/worker-data/"+file_path

        
    def publish_sfm_job(self, id: str, vid: Video ):
        job = {
            "id": id,
            "file_path": self.to_url(vid.file_path)
        }
        json_job = json.dumps(job)
        self.channel.basic_publish(exchange='', routing_key='sfm-in', body=json_job)
        
        
    def publish_nerf_job(self, id: str, vid: Video, sfm: Sfm):
        job = {
            "id": id,
            "vid_width": vid.width,
            "vid_height": vid.height
        }

        # replace relative filepaths with URLS
        sfm_data = sfm.to_dict()
        for i,frame in enumerate(sfm_data["frames"]):
            file_path = frame["file_path"]
            file_url = to_url(file_path)
            sfm_data["frames"][i] = file_url
        
        combined_job = {**job, **sfm_data}
        json_job = json.dumps(combined_job)
        self.channel.basic_publish(exchange='', routing_key='nerf-in', body=json_job)
        
