#!/usr/bin/env python3
"""
This file loads the environment variables from the .env file.
Afterwards, the Web Server is started.
"""

from argparser import create_arguments
from webserver import WebServer

if __name__ == "__main__":
    parser = create_arguments()
    args = parser.parse_args()

    server = WebServer(args)
    server.run()
