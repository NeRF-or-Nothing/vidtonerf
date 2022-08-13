
import pika, os, logging
from models.scene import Video, Sfm, Nerf, SceneManager
import json
from urllib.parse import urlparse
import requests

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
            file_url = self.to_url(file_path)
            sfm_data["frames"][i]["file_path"] = file_url
        
        combined_job = {**job, **sfm_data}
        json_job = json.dumps(combined_job)
        self.channel.basic_publish(exchange='', routing_key='nerf-in', body=json_job)


    #call
    #each sfm_out object would be in the form
        # "id" = id
        # "vid_width": int vid.width,
        # "vid_height": int vid.height
        # "intrinsic_matrix": float[]
        # "frames" = array of urls and extrinsic_matrix[float]
    #   channel.basic.consume(on_message_callback = callback_sfm_job, queue = sfm_out)

    def callback_sfm_job(self, ch,method,properties,body):
        #load queue object
        sfm_data = json.load(body)
        id = sfm_data['id']

        #convert each url to filepath
        #store png 
        for i,fr_ in enumerate(sfm_data['frames']):
            # TODO: This code trusts the file extensions from the worker
            url = fr_['filepath']
            png = requests.get(url)
            url_path = urlparse(fr_['file_path']).path
            filename = url_path.split("/")[-1]
            filepath =  "data/sfm/" + id + "/" + filename
            path = os.path.join(os.getcwd(), filepath)
            png.save(path)
            sfm_data['frames'][i] = filepath


        new_data = json.dumps(sfm_data)

        #call SceneManager to store to database
        sfm = Sfm()
        sfm.from_dict(new_data)
        sManager = SceneManager()
        sManager.set_sfm(id,sfm)

        # depends if you want autoack = True
        #   ch.basic_ack(delivery_tag = method.delivery_tag)
        #publish_nerf_job(id, vid: Video, sfm: Sfm)



    def return_nerf_job(self, ch,method,properties,body):
    
        nerf_data = json.load(body)
        video = requests.get(nerf_data['model_file_path'])
        filepath = "data/nerf/" + id
        path = os.path.join(os.getcwd(), filepath)
        video.save(path)
        id = nerf_data['id']
        nerf = Nerf()
        nerf.from_dict(nerf_data)
        sManager = SceneManager()
        sManager.set_nerf(id, nerf)
        
