"""
This file loads the environment variables from the .env file.
Afterwards, the Web Server is started.
"""

from argparser import create_arguments
from webserver import WebServer

from services.queue_service import RabbitMQService

def main():
    parser = create_arguments()
    args = parser.parse_args()
    rmqservice = RabbitMQService()

    server = WebServer(args, rmqservice)
    server.run()
    

if __name__ == "__main__":
