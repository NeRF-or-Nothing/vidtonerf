
import pika, os, logging
from models.scene import Video, Sfm, Nerf, SceneManager, QueueListManager
import json
from urllib.parse import urlparse
import requests
from flask import url_for
import time
import os
from dotenv import load_dotenv
import numpy as np
import math
import random
import sklearn.cluster


import logging
# Load environment variables from .env file at the root of the project
load_dotenv()

#TODO: make rabbitmq resistent to failed worker jobs

class RabbitMQService:
    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    def __init__(self, rabbitip, manager):
        self.logger = logging.getLogger('web-server')

        rabbitmq_domain = rabbitip
        credentials = pika.PlainCredentials(str(os.getenv("RABBITMQ_DEFAULT_USER")), str(os.getenv("RABBITMQ_DEFAULT_PASS")))
        parameters = pika.ConnectionParameters(rabbitmq_domain, 5672, '/', credentials, heartbeat=300)
        self.queue_manager = manager
        
        #2 minute timer
        timeout = time.time() + 60 * 2

        #retries connection until conencts or 2 minutes pass
        while True:
            if time.time() > timeout:
                self.logger.critical("RabbitMQService, _init_, took too long to connect to rabbitmq")
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
        # for queue list positions

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
        # add to sfm_list and queue_list (first received, goes into overarching queue) queue manager
        self.queue_manager.append_queue("sfm_list",id)
        self.queue_manager.append_queue("queue_list",id)
        
        self.logger.info("SFM Job Published with ID {}".format(id))
           
    def publish_nerf_job(self, id: str, vid: Video, sfm: Sfm):
        """
            publish_nerf_job publishes a new job to the nerf-in que hosted on RabbitMQ
            image sets are converted to links to be downloaded by the nerf worker
        """
        job = {
            "id": id,
            "vid_width": vid.width if vid.width else 0,
            "vid_height": vid.height if vid.height else 0,
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
        # add to nerf_list queue manager
        self.queue_manager.append_queue("nerf_list",id)

        self.logger.info("NERF Job Published with ID {}".format(id))

    #call
    #each sfm_out object would be in the form
        # "id" = id
        # "vid_width": int vid.width,
        # "vid_height": int vid.height
        # "intrinsic_matrix": float[]
        # "frames" = array of urls and extrinsic_matrix[float]
    #   channel.basic.consume(on_message_callback = callback_sfm_job, queue = sfm_out)

def find_elbow_point(data, max_k=35):
    # Within-Cluster Sum of Squares (WCSS)
    wcss = []

    # Set a maximum limit for computational efficiency
    max_k = min(len(data), max_k)  

    # Check if max_k is very large
    max_k = max(max_k, math.floor(math.sqrt(len(data))))

    # Calculate WCSS for different values of k
    for k in range(1, max_k + 1):
        kmeans = sklearn.cluster.KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)

    # Fill in x values for elbow function 
    x = range(1, len(wcss)+1)

    # Determine Elbow point of graph
    #TODO: fix this
    #elbow = kneed.KneeLocator(x, wcss, curve = 'convex', direction='decreasing')
    
    # Returns elbow point (along with x and y values for graph testing)
    #return elbow.knee, x, wcss

def k_mean_sampling(frames, size=100):
    logger = logging.getLogger('web-server')

    #TODO Make this input passed in, with default value 100
    CLUSTERS = size

    extrins = []
    angles = []
    for f in frames["frames"]:
        extrinsic = np.array(f["extrinsic_matrix"])
        extrins+=[ extrinsic ]
    for i,e in enumerate(extrins):

        # t == rectangular coordinates
        t = e[0:3,3]

        # s == spherical coordinates

        # r = sqrt(x^2 + y^2 + z^2)
        r = math.sqrt((t[0]*t[0])+(t[1]*t[1])+(t[2]*t[2]))
        theta = math.acos(t[2]/r)
        phi = math.atan(t[1]/t[0])

        #convert radian to degrees

        theta = (theta * 180) / math.pi
        phi = (phi * 180) / math.pi

        s = [theta,phi]

        angles.append(s)

    #elbow_point, _, _ = find_elbow_point(angles)
    elbow_point = 10
    km = sklearn.cluster.Kmeans(n_clusters=elbow_point, n_init=10)
    km.fit(angles)

    labels = km.labels
    if (len(set(labels)) != elbow_point):
        logger.error("Error with clustering.")

    cluster_array = [ [] for _ in range(elbow_point) ]

    for i in range(len(angles)):
        cluster_array[labels[i]].append(i)

    centroids = km.cluster_centers_
    closest_frames = []

    # Find the frame closest to each centroid in each cluster
    for idx, cluster_indices in enumerate(cluster_array):

        # Extract data points belonging to the current cluster
        cluster_data = np.array([angles[i] for i in cluster_indices])
        
        # Calculate the centroid of the current cluster
        centroid = centroids[idx]

        # Calculate the distances between each data point and the centroid
        distances = np.linalg.norm(cluster_data - centroid, axis=1)

        # Find the index of the closest frame within the current cluster
        closest_frame_index = cluster_indices[np.argmin(distances)]
        
        # Append the index of the closest frame to the list
        closest_frames.append(closest_frame_index)

    return closest_frames


def digest_finished_sfms(rabbitip, rmqservice: RabbitMQService, scene_manager: SceneManager, queue_manager: QueueListManager):
    logger = logging.getLogger('web-server')

    def process_sfm_job(ch,method,properties,body):
        #load queue object
        sfm_data = json.loads(body.decode())
        flag = sfm_data['flag']
        id = sfm_data['id']
        logger.info("SFM TASK RETURNED WITH FLAG {}".format(flag))
        # Process frames only if video is valid (== 0)
        if(flag == 0):
        #convert each url to filepath
        #store png 
            for i,fr_ in enumerate(sfm_data['frames']):
                # TODO: This code trusts the file extensions from the worker
                # TODO: handle files not found
                url = fr_['file_path']
                logger.log(logging.INFO, f"Downloading image from {url}")
                img = requests.get(url)
                url_path = urlparse(fr_['file_path']).path
                filename = url_path.split("/")[-1]
                file_path =  "data/sfm/" + id 
                os.makedirs(file_path, exist_ok=True) 
                file_path += "/" + filename
                open(file_path,"wb").write(img.content)

                path = os.path.join(os.getcwd(), file_path)
                sfm_data['frames'][i]["file_path"] = file_path
        
        # Get indexes of k mean grouped frames
        #k_sampled = k_mean_sampling(sfm_data)

        # Use those frames to revise list of frames used in sfm generation
        #sfm_data['frames'] = [sfm_data['frames'][i] for i in k_sampled]

            del sfm_data['flag']
            #call SceneManager to store to database
            vid = Video.from_dict(sfm_data)
            sfm = Sfm.from_dict(sfm_data)
            scene_manager.set_sfm(id,sfm)
            scene_manager.set_video(id,vid)

        #remove video from sfm_list queue manager
        queue_manager.pop_queue("sfm_list",id)

        logger.info("Saved finished SFM job")
        new_data = json.dumps(sfm_data)
        
        # Publish new job to nerf-in only if good status (flag of 0)
        if(flag == 0):
            rmqservice.publish_nerf_job(id, vid, sfm)
        else:
            queue_manager.pop_queue("queue_list",id)
            # Set a specific flag to the failed flag (normal is 0)
            nerf = Nerf().from_dict({"flag":flag})
            # Set this to the final output
            scene_manager.set_nerf(id, nerf)


        ch.basic_ack(delivery_tag=method.delivery_tag)
        

    # create unique connection to rabbitmq since pika is NOT thread safe
    rabbitmq_domain = rabbitip
    credentials = pika.PlainCredentials(str(os.getenv("RABBITMQ_DEFAULT_USER")), str(os.getenv("RABBITMQ_DEFAULT_PASS")))
    parameters = pika.ConnectionParameters(rabbitmq_domain, 5672, '/', credentials, heartbeat=300)

    #2 minute timer
    timeout = time.time() + 60 * 2

    #retries connection until connects or 2 minutes pass
    while True:
        if time.time() > timeout:
            logger.critical("digest_finished_sfms took too long to connect to rabbitmq")
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


def digest_finished_nerfs(rabbitip, rmqservice: RabbitMQService, scene_manager: SceneManager, queue_manager: QueueListManager):
    logger = logging.getLogger('web-server')

    def process_nerf_job(ch,method,properties,body):
        
        nerf_data = json.loads(body.decode())
        video = requests.get(nerf_data['rendered_video_path'])
        id = nerf_data['id']
        
        filepath = "data/nerf/" 
        os.makedirs(filepath, exist_ok=True)
        filepath = os.path.join(filepath+f"{id}.mp4")
        
        open(filepath,"wb").write(video.content)

        nerf_data["flag"] = 0
        nerf_data['rendered_video_path'] = filepath
        id = nerf_data['id']
        
        # Static method to create Nerf object from dictionary
        nerf = Nerf().from_dict(nerf_data)
        scene_manager.set_nerf(id, nerf)

        #remove video from nerf_list and queue_list (end of full process) queue manager
        queue_manager.pop_queue("nerf_list",id)
        queue_manager.pop_queue("queue_list",id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    # create unique connection to rabbitmq since pika is NOT thread safe
    rabbitmq_domain = rabbitip
    credentials = pika.PlainCredentials(str(os.getenv("RABBITMQ_DEFAULT_USER")), str(os.getenv("RABBITMQ_DEFAULT_PASS")))
    parameters = pika.ConnectionParameters(rabbitmq_domain, 5672, '/', credentials,heartbeat=300)

    #2 minute timer
    timeout = time.time() + 60 * 2

    #retries connection until connects or 2 minutes pass
    while True:
        if time.time() > timeout:
            logger.critical("digest_finished_nerfs took too long to connect to rabbitmq")
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
        
