from flask import Flask
from flask import send_from_directory
from pathlib import Path
import requests
import pika
import json
import time
import shutil
from multiprocessing import Process, connection
import os
from dataLoader import sfm2nerf
from opt import config_parser
from worker import train_tensorf, render_novel_view
from dotenv import load_dotenv

import logging
from log import nerf_worker_logger

app = Flask(__name__)
base_url = "http://nerf-worker:5200/"
#base_url = "0.0.0.0:5200/"


@app.route("/data/nerf_data/<path:path>")
def send_video(path):
    return send_from_directory("data/nerf_data/", path)


def start_flask():
    global app
    app.run(host="0.0.0.0", port=5200, debug=True)


def nerf_worker():
    logger = logging.getLogger('nerf-worker')
    logger.info("Starting nerf-worker!")

    def process_nerf_job(ch, method, properties, body):
        logger.info("Starting New Job")
        args = config_parser("--config configs/localworkerconfig_testsimon.txt")

        nerf_data = json.loads(body.decode())
        id = nerf_data["id"]  
        width = nerf_data["vid_width"]
        height = nerf_data["vid_height"]
        intrinsic_matrix = nerf_data["intrinsic_matrix"]
        frames = nerf_data["frames"]

        logger.info(f"Running New Job With ID: {id}")
        
        input_dir = Path(f"data/sfm_data/{id}")
        os.makedirs(input_dir, exist_ok=True)
        
        for i, fr_ in enumerate(frames):
            # Save copy of motion data
            url = fr_["file_path"]
            img = requests.get(url)
            fr_["file_path"] = f"{i}.png"
            img_file_path = input_dir / fr_["file_path"]
            img_file_path.write_bytes(img.content)

        # Save copy of transform data
        input_train = input_dir / f"transforms_train.json"
        input_render = input_dir / f"transforms_render.json"
        input_train.write_text(json.dumps(nerf_data, indent=4))
        input_render.write_text(json.dumps(nerf_data, indent=4))

        logger.info("Saved motion and transform data.")
        
        # Run TensoRF algorithm, creates sfm2nerf datatype for training
        args.datadir += f"/{id}"
        args.expname = id
        logfolder, tensorf_model = train_tensorf(args)
        local_video_path = render_novel_view(args, logfolder, tensorf_model)

        # Save model and video to nerf_data for retrieval
        out_model_path = Path(f"data/nerf_data/{id}/model.th")
        out_video_path = Path(f"data/nerf_data/{id}/video.mp4")
        os.makedirs(f"data/nerf_data/{id}", exist_ok=True)
        shutil.copy(f"{logfolder}/imgs_render_all/video.mp4", out_video_path)
        shutil.copy(f"{logfolder}/{id}.th", out_model_path)
        
        out_model_path = base_url + str(out_model_path)
        out_video_path = base_url + str(out_video_path)
        
        nerf_output_object = {
          "id" : id,
          "model_filepath" : out_model_path, 
          "rendered_video_path" : out_video_path
        }
        combined_output = json.dumps(nerf_output_object)
        
        channel.basic_publish(exchange='', routing_key='nerf-out', body= combined_output)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Nerf job {} completed!".format(id))
    
    
    # TODO: Communicate with rabbitmq server on port defined in web-server arguments
    load_dotenv()
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
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='nerf-in')
            channel.queue_declare(queue='nerf-out')

            # Will block and call process_nerf_job repeatedly
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='nerf-in', on_message_callback=process_nerf_job, auto_ack=False)
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                break
        except pika.exceptions.AMQPConnectionError:
            continue
    

if __name__ == "__main__":
    # DEFINE LOGGER
    logger = nerf_worker_logger('nerf-worker')
    logger.info("~NERF WORKER~")

    nerfProcess = Process(target=nerf_worker, args=())
    flaskProcess = Process(target=start_flask, args=())
    flaskProcess.start()
    nerfProcess.start()
    flaskProcess.join()
    nerfProcess.join()

        