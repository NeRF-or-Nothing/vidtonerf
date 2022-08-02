import pika, os, logging

class RabbitMQService:
    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sfm-in')
        channel.queue_declare(queue='sfm-out')
        channel.queue_declare(queue='nerf-in')
        channel.queue_declare(queue='nerf-out')
        
    def post_video(self, uuid):
        channel.basic_publish(exchange='', routing_key='sfm-in', body=uuid)
        
    def get_sfm(self):
        pass
        
    def post_sfm(self):
        channel.basic_publish(exchange='', routing_key='sfm-in', body=uuid)
        
    def get_nerf(self):
        pass

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print("sent")
connection.close()
