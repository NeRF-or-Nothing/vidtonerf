from flask import Flask, send_from_directory
from pathlib import Path
from log import nerf_worker_gaussian_logger
from opt import config_parser
from dotenv import load_dotenv
from utils import nerf_utils

import multiprocessing as mp

import requests
import pika
import json
import time
import shutil
import os
import functools
import threading
import logging
import torch
import train

# Globals
app = Flask(__name__)
base_url = "http://nerf-worker:5200/"


@app.route("/data/nerf_data/<path:path>")
def send_video(path):
    """
    Handles incoming get requests for trained nerf data in form of video

    Args:
        path (_type_): Requested URI

    Returns:
        _type_: Video data from the requested URI
    """
    return send_from_directory("data/nerf_data/", path)


@app.route("/data/nerf_data/point_cloud/<path:path>")
def send_point_cloud(path):
    """
    Handles incoming get requests for trained nerf data in form of point cloud

    Args:
        path (_type_): Requested URI

    Returns:
        _type_: Point cloud data from the requested URI
    """
    return send_from_directory("data/nerf_data/point_cloud/", path)


@app.route("data/nerf_data/splat/<path:path>")
def send_splats(path):
    """
    Handles incoming get requests for trained nerf data that
    has been converted to .splat notation for front end rendering

    Args:
        path (_type_): Requested URI

    Returns:
        _type_: Splat data from the requested URI
    """
    return send_from_directory("data/nerf_data/splat/", path)


def start_flask():
    """
    Starts the flask server for the nerf-worker to communicate with the web-server
    """
    global app
    app.run(host="0.0.0.0", port=5200, debug=False)


def ack_publish_message(channel, delivery_tag, body):
    """
    Threadsafe function to publish a message to the rabbitmq server and
    acknowledge job as completed

    Args:
        channel (_type_): channel object from pika
        delivery_tag (_type_): delivery_tag object from pika
        body (_type_): job completion data for web-server
    """
    logger = logging.getLogger('nerf-worker-gaussian')
    logger.info("Publishing message")

    if body:
        channel.basic_publish(exchange='', routing_key='nerf-out', body=body)
    channel.basic_ack(delivery_tag=delivery_tag)


def on_message(channel, method, header, body, args):
    """
    Handles nerf-in messages received from rabbitmq server.
    Starts a new thread to process the nerf job.

    Args:
        channel (_type_): channel object from pika
        method (_type_): method object from pika
        header (_type_): header object from pika
        body (_type_): body object from pika
        args (_type_): global running thread list
    """
    logger = logging.getLogger('nerf-worker-gaussian')
    logger.info("Received message")
    thrds = args
    delivery_tag = method.delivery_tag

    t = threading.Thread(target=run_nerf_job, args=(
        channel, method, delivery_tag, body))
    t.start()
    thrds.append(t)


def run_nerf_job(channel, method, properties, body):
    """
    Handles the running of the nerf job. Trains the nerf model and sends the
    output to the web-server.

    Args:
        channel (_type_): Pika channel object
        method (_type_): Pika method object
        properties (_type_): Pika properties object
        body (_type_): Contains job details for training the nerf model
    """

    logger = logging.getLogger('nerf-worker-gaussian')

    # Read the nerf data from the message and convert it to gaussian format
    job_data = json.loads(body.decode())
    job_data_converted = nerf_utils.convert_transforms_to_gaussian(job_data)
    id = job_data_converted["id"]

    # Create input directory for the nerf data
    input_dir: Path = Path("data/sfm_data") / id
    output_dir: Path = Path("data/nerf_data") / id
    os.makedirs(input_dir, exist_ok=True)
    os.makerdirs(output_dir, exist_ok=True)

    # Receive images from web-server
    for i, fr in enumerate(job_data_converted["frames"]):
        url = fr["file_path"]
        img = requests.get(url)
        fr["file_path"] = f"{i}.png"
        img_file_path = input_dir / fr["file_path"]
        img_file_path.write_bytes(img.content)

    # Save the sfm transform data to a file
    input_train = input_dir / "transforms_train.json"
    input_train.write_text(json.dumps(job_data_converted, indent=4))

    logger.info(f"Running nerf job for {id}")
    logger.info(f"Input directory: {input_dir}")

    # Run the nerf job
    # TODO: Allow user defined snapshot save frequency (default 7000, 30000 iters)
    # TODO: Allow user to request available snapshots mid training for frontend render
    # TODO: Log training and model saving
    args = [
        "-s", input_dir,
        "-m", output_dir,
        "--save_iterations", "10000", "20000", "30000",
        "--iterations", "30000"
    ]

    # Run gaussian splatting model training
    # TODO: Log training and model saving
    logger.info(f'Running nerf training with args: {args}')
    train.main(args)
    logger.info(f"Finished training for {id}")
    # TODO: Post the nerf data to the web-server

    CONVERT_TO_SPLAT = True
    SPLAT_ITERATION = 30000
    # TODO: User defined
    # TODO: Convert all splats to .splat format, not just 30000th iteration
    if CONVERT_TO_SPLAT:
        # Convert the nerf data to splat format for the frontend
        logger.info(f"Converting {id} iteration 
                    {SPLAT_ITERATION}.ply to .splat format")
        
        splat_dir = Path("data/nerf_data/splat") / id /
        os.makedirs(splat_dir, exist_ok=True)
        splat_data = nerf_utils.convert_to_splat(output_dir, splat_dir)
        with open(splat_dir / "{SPLAT_ITERATION}.splat", "rb") as f:
            f.write(splat_data)
             
        logger.info(f"Finished converting {id} iteration 
                    {SPLAT_ITERATION}.ply to .splat format")

    nerf_output_object = {
        "id": id,
        "training_mode": "gaussian",
        "splat_path": Path(base_url) / f"{output_dir}/splat/{SPLAT_ITERATION}.splat",
    }

    callback = functools.partial(
        ack_publish_message,
        channel,
        method.delivery_tag,
        json.dumps(nerf_output_object))

    channel.connection.add_callback_threadsafe(callback)


def init_nerf_worker(i, *args):
    """
    Handles the initialization of the nerf worker gaussian process.
    Creates a connection to the rabbitmq server and listens for incoming messages.
    Each message will be processed in a separate thread.

    Args:
        i (_type_): Torch multiprocessing index

    Raises:
        Exception: If the nerf worker takes too long to connect to the rabbitmq server
    """

    # Load env and initialize logger
    load_dotenv()
    logger = nerf_worker_gaussian_logger('nerf-worker-gaussian')

    # Cuda device information
    logger.info("~NERF WORKER GAUSSIAN~")
    logger.info(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info(f"Available CUDA devices: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            logger.info(f"CUDA Device {i}: {torch.cuda.get_device_name(i)}")

    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    rabbitmq_domain = "rabbitmq"
    credentials = pika.PlainCredentials(
        str(os.getenv("RABBITMQ_DEFAULT_USER")), str(os.getenv("RABBITMQ_DEFAULT_PASS")))
    parameters = pika.ConnectionParameters(
        rabbitmq_domain, 5672, '/', credentials, heartbeat=300
    )

    # retries connection until connects or 2 minutes pass
    timeout = time.time() + 60 * 2
    while True:
        if time.time() > timeout:
            logger.critical("nerf_worker took too long to connect to rabbitmq")
            raise Exception(
                "nerf_worker took too long to connect to rabbitmq")
        try:
            threads = []
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='nerf-in')
            channel.queue_declare(queue='nerf-out')

            # Will block until it creates a separate thread for each message
            # This is to prevent the main thread from blocking
            channel.basic_qos(prefetch_count=1)
            on_message_callback = functools.partial(on_message, args=(threads))
            channel.basic_consume(
                queue='nerf-in', on_message_callback=on_message_callback, auto_ack=False)
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                for thread in threads:
                    thread.join()

        except pika.exceptions.AMQPConnectionError:
            continue


if __name__ == "__main__":
    # IMPORTANT: FOR CUDA DEVICE USAGE
    # flask must run in a normally FORKED python.multiprocessing process
    # training and pika must run in a SPAWNED torch.multiprocessing process
    # else you will have issues with redeclaring cuda devices
    # if flask is not in forked process, web-server cannot send get requests,
    # but nerf-worker will be able to send get requests to web-server

    # additional note: spawn does not inherit memory, so need to reinitialize
    # the logger in the spawned process. This creates issues with both file
    # descriptors pointing to the same file, so the __main__ logger will not
    # be able to write to the file for now I have moved the logger to the
    # nerf_worker process as the flask process never used the logger

    flaskProcess = mp.Process(target=start_flask, args=())
    flaskProcess.start()
    nerfProcess = torch.multiprocessing.spawn(fn=init_nerf_worker, args=())
    nerfProcess.start()
    flaskProcess.join()
    nerfProcess.join()
