"""
This file loads the environment variables from the .env file.
Afterwards, the Web Server is started.
"""

from argparser import create_arguments
from webserver import WebServer

from services.queue_service import RabbitMQService
from services.scene_service import SceneService

def main():
    parser = create_arguments()
    args = parser.parse_args()
    rmqservice = RabbitMQService()
    
    sservice = SceneService(rmqservice)

    server = WebServer(args, sservice)
    server.run()

if __name__ == "__main__":
    main()
    
