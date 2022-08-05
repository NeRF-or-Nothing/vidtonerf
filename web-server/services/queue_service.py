
import pika, os, logging
import asyncio

def rabbit_read_out(callback, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=intake_func)
    channel.start_consuming()
    

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
        
        
    def post_video(self, send_str):
        self.channel.basic_publish(exchange='', routing_key='sfm-in', body=send_str)
        
        
    def post_sfm(self, send_str):
        self.channel.basic_publish(exchange='', routing_key='sfm-in', body=uuid)
        
