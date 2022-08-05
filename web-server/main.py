"""
This file loads the environment variables from the .env file.
Afterwards, the Web Server is started.
"""

from argparser import create_arguments
from webserver import WebServer
import threading

from services.queue_service import RabbitMQService, rabbit_read_out
from services.scene_service import SceneService, read_sfm, read_nerf


def main():
    client = None
    parser = create_arguments()
    args = parser.parse_args()
    rmqservice = RabbitMQService()
    # Starting async operations
    sfm_thread = threading.Thread(target=rabbit_read_out,\
        args=(lambda ch, method, properties, body : read_sfm(client, body), 'sfm-out'))
    nerf_thread = threading.Thread(target=rabbit_read_out,\
        args=(lambda ch, method, properties, body : read_nerf(client, body), 'nerf-out'))
    sfm_thread.start()
    nerf_thread.start()
    
    sservice = SceneService(rmqservice)

    server = WebServer(args, sservice)
    server.run()

if __name__ == "__main__":
    main()
    
