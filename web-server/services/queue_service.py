import pika, os, logging
import json

class RabbitMQService:
    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    def __init__(self):
        # Change this ->
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='sfm-in')
        self.channel.queue_declare(queue='sfm-out')
        self.channel.queue_declare(queue='nerf-in')
        self.channel.queue_declare(queue='nerf-out')
        
        # Needs to be set as soon as webserver is started
        self.base_url = None
        
        
    def post_video(self, send_str):
        self.channel.basic_publish(exchange='', routing_key='sfm-in', body=send_str)
        
    def get_sfm(self):
        pass
        
    def post_sfm(self, send_str):
        self.channel.basic_publish(exchange='', routing_key='sfm-in', body=uuid)
        
    def get_nerf(self):
        pass
