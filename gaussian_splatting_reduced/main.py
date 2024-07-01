from flask import Flask, send_from_directory
from pathlib import Path
from log import nerf_worker_logger
from opt import config_parser
from dotenv import load_dotenv
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
import multiprocessing as mp
from utils import nerf_utils
import train

app = Flask(__name__)
base_url = "http://nerf-worker:5200/"

@app.route("/data/nerf_data/<path:path>")
def send_video(path):
    return send_from_directory("data/nerf_data/", path)

def start_flask():
    global app
    app.run(host="0.0.0.0", port=5200, debug=False)

def on_message(channel, method, header, body, args):
    logger = logging.getLogger('nerf-worker')
    logger.info("Received message")
    thrds = args
    delivery_tag = method.delivery_tag
    
    t = threading.Thread(target = run_nerf_job, args=(channel, method, delivery_tag, body))
    t.start()
    thrds.append(t)

def run_nerf_job(channel, method, properties, body):
    logger = logging.getLogger('nerf-worker')

    # Read the nerf data from the message and convert it to gaussian format
    job_data = json.loads(body.decode())
    job_data_converted = nerf_utils.convert_transforms_to_gaussian(job_data)
    
    # Create input directory for the nerf data
    id = job_data_converted["id"]
    input_dir = Path("data/sfm_data") / id
    os.makedirs(input_dir, exist_ok=True)

    # Receive images from web-server
    for i, fr in enumerate(job_data_converted["frames"]):
        url = fr["file_path"]
        img = requests.get(url)
        fr["file_path"] = f"{i}.png" 
        img_file_path = input_dir / fr["file_path"]
        img_file_path.write_bytes(img.content)

    # Save the sfm data to a file
    input_train = input_dir / "transforms_train.json"
    input_train.write_text(json.dumps(job_data_converted, indent=4))

    logger.info(f"Running nerf job for {id}")
    logger.info(f"Input directory: {input_dir}")

    # Run the nerf job
    # TODO: Allow user defined snapshot frequency (default 7000, 30000 iters)
    # TODO: Allow user to request available snapshots mid training for frontend render
    args = f"-s {input_dir}".split()
    logger.info(f'Running nerf training with args: {args}')

    train.main(args)
    logger.info(f"Finished training for {id}")




def init_nerf_worker(i, *args):
    load_dotenv()
    logger = nerf_worker_logger('nerf-worker')
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

    # additional note: spawn does not inherent memory, so need to reinitialize
    # the logger in the spawned process. This creates issues with both file descriptors
    # pointing to the same file, so the __main__ logger will not be able to write to the file
    # for now I have moved the logger to the nerf_worker process as the flask process never used
    # the logger

    flaskProcess = mp.Process(target=start_flask, args=())
    flaskProcess.start()
    nerfProcess = torch.multiprocessing.spawn(fn=init_nerf_worker, args=())
    nerfProcess.start()
    flaskProcess.join()
    nerfProcess.join()
