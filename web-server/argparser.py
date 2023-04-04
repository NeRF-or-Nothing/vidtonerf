import argparse
from typing import Union


def create_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Web Server", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # consult LOGLEVELS.md for possible values
    parser.add_argument(
        "-l",
        "--log",
        help="set log level",
        choices=["10", "20", "30", "40", "50", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],

        default="ERROR",
    )

    parser.add_argument(
        "-p", "--port", help="set port to listen on", type=int, default=5000
    )

    parser.add_argument(
        "--configip", type=str, default="configs/docker_out.json"
    )
    
    return parser
