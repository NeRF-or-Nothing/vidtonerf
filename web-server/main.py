"""
This file loads the environment variables from the .env file.
Afterwards, the Web Server is started.
"""

from argparser import create_arguments
from webserver import WebServer
import threading

from services.queue_service import RabbitMQService, rabbit_read_out
from services.scene_service import SceneService, ClientService, read_sfm, read_nerf
from services.clean_service import cleanup
from pymongo import MongoClient


def main():
    # MongoDB client, I don't know how to set this up
    client = MongoClient(host="localhost",port=27017,username="admin",password="password123")
    parser = create_arguments()
    args = parser.parse_args()
    rmqservice = RabbitMQService()
    # Starting async operations
    # This starts consuming messages from the queue, a blocking call, and when one comes in it
    # provides the body to read_sfm through the callback argument
    #sfm_thread = threading.Thread(target=rabbit_read_out,\
    #    args=(lambda ch, method, properties, body : read_sfm(client, body), 'sfm-out'))
    #nerf_thread = threading.Thread(target=rabbit_read_out,\
    #    args=(lambda ch, method, properties, body : read_nerf(client, body), 'nerf-out'))
    #sfm_thread.start()
    #nerf_thread.start()
    
    #cleanup_thread = threading.Thread(target=cleanup, args=(client))
    #cleanup_thread.start()
    
    cservice = ClientService(client, rmqservice)

    server = WebServer(args, cservice)
    server.run()

if __name__ == "__main__":
    main()
    
