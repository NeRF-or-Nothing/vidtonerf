"""
This file loads the environment variables from the .env file.
Afterwards, the Web Server is started.
"""

from argparser import create_arguments
from controller import WebServer
import threading
from models.scene import SceneManager
from services.queue_service import RabbitMQService, digest_finished_sfms, digest_finished_nerfs
from services.scene_service import ClientService
from services.clean_service import cleanup
from pymongo import MongoClient


def main():
    print("Starting web-app...")
    
    parser = create_arguments()
    args = parser.parse_args()
    
    # Shared Database manager <from models>
    # SceneManager shared across threads since it is thread safe
    scene_man = SceneManager()

    # Rabbitmq service to post new jobs to the workers <from services>
    rmq_service = RabbitMQService()

    # Starting async operations to pull finished jobs from rabbitmq <from services>
    sfm_output_thread = threading.Thread(target=digest_finished_sfms, args=(scene_man,))
    nerf_output_thread = threading.Thread(target=digest_finished_nerfs, args=(scene_man,))
    sfm_output_thread.start()
    nerf_output_thread.start()

    # TODO: async worker to clean up old data
    
    # service to handle all incoming client requests from the controller <from services>
    c_service = ClientService(scene_man, rmq_service)

    # start listening to incoming requests on the controller <from controllers>
    server = WebServer(args, c_service)
    server.run()

if __name__ == "__main__":
    main()
    
