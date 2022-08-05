import pika, os, logging
import json


def callback(ch, method, properties, body):
    print( " [x] recieved %r" % body )
    try:
        obj = json.loads(body)
    except ValueError:
        print("loading failed")
    

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sfm-in')
channel.queue_declare(queue='nerf-in')

channel.basic_consume(queue='sfm-in', auto_ack=True, on_message_callback=callback)
channel.basic_consume(queue='nerf-in', auto_ack=True, on_message_callback=callback)
print("waiting for messages")
channel.start_consuming()
connection.close()
