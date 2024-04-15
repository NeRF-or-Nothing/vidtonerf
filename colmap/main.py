from flask import Flask
from flask import send_from_directory
from pathlib import Path
from video_to_images import split_video_into_frames
from colmap_runner import run_colmap
from matrix import get_json_matrices
from image_position_extractor import extract_position_data
from opt import config_parser
import requests
import pika
import json
import time
from multiprocessing import Process
import os
import argparse
import sys

import logging
from log import sfm_worker_logger

from dotenv import load_dotenv

app = Flask(__name__)
# base_url = "http://host.docker.internal:5000/"
base_url = "http://sfm-worker:5100/"


@app.route("/data/outputs/<path:path>")
def send_video(path):
    logger.info(f"Sending video: {path}")
    return send_from_directory("data/outputs/", path)


def start_flask():
    global app
    app.run(host="0.0.0.0", port=5100, debug=True)


def to_url(local_file_path: str):
    return base_url + local_file_path


def run_full_sfm_pipeline(id, video_file_path, input_data_dir, output_data_dir):
    # run colmap and save data to custom directory
    # Create output directory under data/output_data_dir/id
    # TODO: use library to fix filepath joining
    if not output_data_dir.endswith(("\\", "/")) and not id.startswith(("\\", "/")):
        output_data_dir = output_data_dir + "/"
    output_path = output_data_dir + id
    Path(f"{output_path}").mkdir(parents=True, exist_ok=True)

    # Get logger
    logger = logging.getLogger('sfm-worker')

    # (1) vid_to_images.py
    imgs_folder = os.path.join(output_path, "imgs")
    logger.info("Video file path:{}".format(video_file_path))

    split_status = split_video_into_frames(video_file_path, imgs_folder, 100)
    # Catches flag for blurriness
    if split_status == 4:
        logger.error("Video is too blurry.")
        # motion_data flag option determines the status of the job
        # flag = 4 means the video was too blurry
        motion_data = {"flag":4,"id":id}
        return motion_data, None

    # imgs are now in output_data_dir/id

    # (2) colmap_runner.py
    colmap_path = "/usr/local/bin/colmap"
    status = run_colmap(colmap_path, imgs_folder, output_path)
    if status == 0:
        logger.info("COLMAP ran successfully.")
    elif status == 1:
        logger.error("ERROR: There was an unknown error running COLMAP")

    # (3) matrix.py
    initial_motion_path = os.path.join(output_path, "images.txt")
    camera_stats_path = os.path.join(output_path, "cameras.txt")
    parsed_motion_path = os.path.join(output_path, "parsed_data.csv")

    extract_position_data(initial_motion_path, parsed_motion_path)
    motion_data = get_json_matrices(camera_stats_path, parsed_motion_path)
    motion_data["id"] = id
    motion_data["flag"] = 0

    # Save copy of motion data
    with open(os.path.join(output_path, "transforms_data.json"), "w") as outfile:
        outfile.write(json.dumps(motion_data, indent=4))

    return motion_data, imgs_folder


def colmap_worker():
    load_dotenv()
    input_data_dir = "data/inputs/"
    output_data_dir = "data/outputs/"
    Path(f"{input_data_dir}").mkdir(parents=True, exist_ok=True)
    Path(f"{output_data_dir}").mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger('sfm-worker')

    def process_colmap_job(ch, method, properties, body):
        logger.info("Starting New Job")
        logger.info(body.decode())
        job_data = json.loads(body.decode())
        id = job_data["id"]
        
        logger.info(f"Running New Job With ID: {id}")

        # TODO: Handle exceptions and enable steaming to make safer
        video = requests.get(job_data["file_path"], timeout=10)
        logger.info("Web server pinged")
        video_file_path = f"{input_data_dir}{id}.mp4"
        logger.info("Saving video to: {video_file_path}")
        open(video_file_path, "wb").write(video.content)
       
        logger.info("Video downloaded")

        # RUNS COLMAP AND CONVERSION CODE
        motion_data, imgs_folder = run_full_sfm_pipeline(
            id, video_file_path, input_data_dir, output_data_dir
        )
        # Catch incomplete videos by flag != 1 and return here
        if motion_data["flag"] != 0:
            logger.error("An error was found. Ending process.")
            channel.basic_publish(
            exchange="", routing_key="sfm-out", body=json.dumps(motion_data)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # create links to local data to serve
        for i, frame in enumerate(motion_data["frames"]):
            file_name = frame["file_path"]
            file_path = os.path.join(imgs_folder, file_name)
            file_url = to_url(file_path)
            motion_data["frames"][i]["file_path"] = file_url

        json_motion_data = json.dumps(motion_data)
        channel.basic_publish(
            exchange="", routing_key="sfm-out", body=json_motion_data
        )

        # confirm to rabbitmq job is done
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Job complete")


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
            raise Exception(
                "nerf_worker took too long to connect to rabbitmq")
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='sfm-in')
            channel.queue_declare(queue='sfm-out')

            # Will block and call process_nerf_job repeatedly
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue='sfm-in', on_message_callback=process_colmap_job, auto_ack=False)
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                break
        except pika.exceptions.AMQPConnectionError:
            continue
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="sfm-in", on_message_callback=process_colmap_job)
    channel.start_consuming()
    logger.critical("Should not get here: After consumption of RabbitMQ.")

if __name__ == "__main__":  
    input_data_dir = "data/inputs/"
    output_data_dir = "data/outputs/"
    Path(f"{input_data_dir}").mkdir(parents=True, exist_ok=True)
    Path(f"{output_data_dir}").mkdir(parents=True, exist_ok=True)

    """
     STARTING LOGGER
    """
    logger = sfm_worker_logger('sfm-worker')
    logger.info("~SFM WORKER~")

    # Load args from config file
    args = config_parser()

    # Local run behavior
    if args.local_run == True:
        motion_data, imgs_folder = run_full_sfm_pipeline(
            "Local_Test", args.input_data_path, input_data_dir, output_data_dir
        )
        logger.info("MOTION DATA: {}".format(motion_data))
        json_motion_data = json.dumps(motion_data)

    # Standard webserver run behavior
    else:
        sfmProcess = Process(target=colmap_worker, args=())
        flaskProcess = Process(target=start_flask, args=())
        flaskProcess.start()
        sfmProcess.start()
        flaskProcess.join()
        sfmProcess.join()
