"""
This file loads the environment variables from the .env file.
Afterwards, the Web Server is started.
"""

from argparser import create_arguments
from sfm_server import SfmServer
from time import sleep
import threading
import pika
import json
import requests
import os
    

def process_sfm(jsonstr):
    print('got string %s', jsonstr)
    try:
        obj = json.loads(jsonstr)
    except ValueError:
        return
    # download files from webserver
    for link, filename in zip(obj["filelinks"], obj["filenames"]):
        data = requests.get(link)
        # TODO: This is literally just saving files that are being arbitrarily served up.
        # Needs to be more secure.
        path = os.path.join(os.getcwd(), "data/" + filename)
        with open(path, 'wb') as f:
            f.write(data.content)
    # 'process'
    print('processing')
    sleep(10)
    
    # make new json
    sfmjson = {}
    sfmjson["filelinks"] = []
    sfmjson["filelinks"].append("http://localhost:5555/" + filename)
    # Currently, filenames are associated with filelinks only by order.
    # We may want to change this.
    sfmjson["filenames"] = []
    # TODO: Should depend on actual file name
    sfmjson["filenames"].append(filename)
    
    # send to rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sfm-out')
    channel.basic_publish(exchange='', routing_key='sfm-in', body=json.dumps(sfmjson))
            
def rabbit_read_out(callback, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)
    print('starting to consume')
    channel.start_consuming()

def main():
    parser = create_arguments()
    args = parser.parse_args()
    data_thread = threading.Thread(target=rabbit_read_out,\
        args=(lambda ch, method, properties, body : process_sfm(body), 'sfm-in'))
    data_thread.start()

    server = SfmServer(args)
    server.run()

if __name__ == "__main__":
    main()
    
