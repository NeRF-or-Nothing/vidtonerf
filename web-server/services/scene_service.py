import os
import requests
import json
from models.scene import SceneManager, Video
from services.queue_service import RabbitMQService
from uuid import uuid4, UUID
from werkzeug.utils import secure_filename

from pymongo import MongoClient

import logging

class ClientService:
    def __init__(self, manager: SceneManager, rmqservice: RabbitMQService):
        self.logger = logging.getLogger('web-server')
        self.manager = manager
        self.rmqservice = rmqservice
        
    def handle_incoming_video(self, video_file):
        # receive video and check for validity
        file_name = secure_filename(video_file.filename)
        if file_name == '':
            self.logger.error("ERROR: file not received")
            return None

        file_ext = os.path.splitext(file_name)[1]
        if file_ext != ".mp4":
            self.logger.error("ERROR: improper file extension uploaded")
            return None

        # generate new id and save to file with db record
        uuid = str(uuid4())
        video_name = uuid + ".mp4"
        videos_folder = "data/raw/videos"
        current_directory = os.getcwd()

        #video_file_path = os.path.join(current_directory, videos_folder)
        video_file_path = videos_folder
        
        if not os.path.exists(video_file_path):
            # If the path does not exist, create it
            os.makedirs(video_file_path)
        video_file_path = os.path.join(video_file_path, video_name)
        video_file.save(video_file_path)

        video = Video(video_file_path)
        self.manager.set_video(uuid, video)

        # create rabbitmq job for sfm
        #TODO
        self.rmqservice.publish_sfm_job(uuid, video)

        return uuid

    # Returns a string describing the status of the video in the database
    # along with a path to the final video, if available
    def get_nerf_video_path(self, uuid):
        # TODO: depend on mongodb to load file path
        # return None if not found
        nerf = self.manager.get_nerf(uuid)
        if nerf:
            return nerf.rendered_video_path
            #return ("Video ready", nerf.rendered_video_path)
        return None
    
    # Returns an integer describing the status of the video in the database.
    # Normal videos will have a value of 0 and this is unncessary, but other values
    # encode information on the COLMAP error that went wrong(e.g. 4 is a blurry video)
    def     get_nerf_flag(self, uuid):
        nerf = self.manager.get_nerf(uuid)
        if nerf:
            return nerf.flag
        return 0
        