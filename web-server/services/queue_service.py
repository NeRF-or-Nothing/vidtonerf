
import pika, os, logging
from models.scene import Video, Sfm, Nerf, SceneManager
import json
from urllib.parse import urlparse
import requests
from flask import url_for
import time

#TODO: make rabbitmq resistent to failed worker jobs

class RabbitMQService:
    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    def __init__(self):
        rabbitmq_domain = "rabbitmq"
        credentials = pika.PlainCredentials('admin', 'password123')
        parameters = pika.ConnectionParameters(rabbitmq_domain, 5672, '/', credentials, heartbeat=300)
        
        #2 minute timer
        timeout = time.time() + 60 * 2

        #retries connection until conencts or 2 minutes pass
        while True:
            if time.time() > timeout:
                raise Exception("RabbitMQService, _init_, took too long to connect to rabbitmq")
            try:
                self.connection = pika.BlockingConnection(parameters)  
                self.channel = self.connection.channel() 
                self.channel.queue_declare(queue='sfm-in')
                self.channel.queue_declare(queue='nerf-in')
                break
            except pika.exceptions.AMQPConnectionError:
                continue

        #TODO: make this dynamic from config file
        self.base_url = "http://localhost:5000/"
        # for docker
        self.base_url = "http://host.docker.internal:5000/"

    def to_url(self,file_path):
        return self.base_url+"/worker-data/"+file_path

    #
    def publish_sfm_job(self, id: str, vid: Video ):
        """
            publish_sfm_job publishes a new job to the sfm-in que hosted on RabbitMQ
        """
        job = {
            "id": id,
            "file_path": self.to_url(vid.file_path)
        }
        json_job = json.dumps(job)
        self.channel.basic_publish(exchange='', routing_key='sfm-in', body=json_job)
           
    def publish_nerf_job(self, id: str, vid: Video, sfm: Sfm):
        """
            publish_nerf_job publishes a new job to the nerf-in que hosted on RabbitMQ
            image sets are converted to links to be downloaded by the nerf worker
        """
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



def digest_finished_sfms(scene_manager: SceneManager):

    def process_sfm_job(ch,method,properties,body):
        #load queue object
        sfm_data = json.loads(body.decode())
        id = sfm_data['id']

        #convert each url to filepath
        #store png 
        for i,fr_ in enumerate(sfm_data['frames']):
            # TODO: This code trusts the file extensions from the worker
            # TODO: handle files not found
            url = fr_['file_path']
            img = requests.get(url)
            url_path = urlparse(fr_['file_path']).path
            filename = url_path.split("/")[-1]
            file_path =  "data/sfm/" + id 
            os.makedirs(file_path, exist_ok=True) 
            file_path += "/" + filename
            open(file_path,"wb").write(img.content)

            path = os.path.join(os.getcwd(), file_path)
            sfm_data['frames'][i]["file_path"] = file_path


        #call SceneManager to store to database
        vid = Video.from_dict(sfm_data)
        sfm = Sfm.from_dict(sfm_data)
        scene_manager.set_sfm(id,sfm)
        scene_manager.set_video(id,vid)

        print("saved finished sfm job")
        new_data = json.dumps(sfm_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # create unique connection to rabbitmq since pika is NOT thread safe
    rabbitmq_domain = "rabbitmq"
    credentials = pika.PlainCredentials('admin', 'password123')
    parameters = pika.ConnectionParameters(rabbitmq_domain, 5672, '/', credentials, heartbeat=300)

    #2 minute timer
    timeout = time.time() + 60 * 2

    #retries connection until connects or 2 minutes pass
    while True:
        if time.time() > timeout:
            raise Exception("digest_finished_sfms took too long to connect to rabbitmq")
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='sfm-out')

            # Will block and call process_sfm_job repeatedly
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='sfm-out', on_message_callback=process_sfm_job)
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                break
        except pika.exceptions.AMQPConnectionError:
            continue


def digest_finished_nerfs(scene_manager: SceneManager):

    def process_nerf_job(ch,method,properties,body):
        nerf_data = json.loads(body.decode())
        video = requests.get(nerf_data['rendered_video_path'])
        filepath = "data/nerf/" 
        os.mkdir(filepath, exist_ok=True)
        filepath = os.path.join(filepath,+f"{id}.mp4" )
        open(filepath,"wb").write(video.content)

        nerf_data['rendered_video_path'] = filepath
        id = nerf_data['id']
        nerf = Nerf()
        nerf.from_dict(nerf_data)
        scene_manager.set_nerf(id, nerf)
        #ch.basic_ack(delivery_tag=method.delivery_tag)
    
    # create unique connection to rabbitmq since pika is NOT thread safe
    rabbitmq_domain = "rabbitmq"
    credentials = pika.PlainCredentials('admin', 'password123')
    parameters = pika.ConnectionParameters(rabbitmq_domain, 5672, '/', credentials,heartbeat=300)

    #2 minute timer
    timeout = time.time() + 60 * 2

    #retries connection until connects or 2 minutes pass
    while True:
        if time.time() > timeout:
            raise Exception("digest_finished_nerfs took too long to connect to rabbitmq")
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='nerf-out')

            # Will block and call process_nerf_job repeatedly
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='nerf-out', on_message_callback=process_nerf_job)
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                break
        except pika.exceptions.AMQPConnectionError:
            continue
        
