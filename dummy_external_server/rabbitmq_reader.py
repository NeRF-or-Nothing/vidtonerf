import pika, os, logging

def callback(ch, method, properties, body):
    print( " [x] recieved %r" % body )

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sfm-in')

channel.basic_consume(queue='sfm-in', auto_ack=True, on_message_callback=callback)
print("waiting for messages")
channel.start_consuming()
connection.close()
