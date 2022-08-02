import pika, os, logging

class RabbitMQService:
    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='sfm-in')
        self.channel.queue_declare(queue='sfm-out')
        self.channel.queue_declare(queue='nerf-in')
        self.channel.queue_declare(queue='nerf-out')
        
    def __del__(self):
        self.connection.close();
        
    def post_video(self, uuid):
        self.channel.basic_publish(exchange='', routing_key='sfm-in', body=uuid)
        
    def get_sfm(self):
        pass
        
    def post_sfm(self, uuid):
        self.channel.basic_publish(exchange='', routing_key='nerf-in', body=uuid)
        
    def get_nerf(self):
        pass

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print("sent")
connection.close()
