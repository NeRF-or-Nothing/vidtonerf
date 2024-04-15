from flask import Flask, send_from_directory
from pathlib import Path
from log import nerf_worker_logger
from opt import config_parser
from worker import train_tensorf, render_novel_view
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

def ack_publish_message(channel, delivery_tag, body):
    logger = logging.getLogger('nerf-worker')
    logger.info("Publishing message")
    
    if body:
        channel.basic_publish(exchange='', routing_key='nerf-out', body=body)
    channel.basic_ack(delivery_tag=delivery_tag)
    
def run_nerf_job(channel, method, properties, body):
    logger = logging.getLogger('nerf-worker')
    
    args = config_parser(
        "--config configs/localworkerconfig_testsimon.txt")

    nerf_data = json.loads(body.decode())
    id = nerf_data["id"]
    width = nerf_data["vid_width"]
    height = nerf_data["vid_height"]
    intrinsic_matrix = nerf_data["intrinsic_matrix"]
    frames = nerf_data["frames"]
    
    logger.info(f"Running nerf job for {id}")

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

    logger.info("Saved motion and transorm data")
    
    # Run TensoRF algorithm, creates sfm2nerf datatype for training
    args.datadir += f"/{id}"
    args.expname = id
    logfolder, tensorf_model = train_tensorf(args)
    local_video_path = render_novel_view(args, logfolder, tensorf_model)
    
    # Clear from RAM/VRAM to prevent detached thread leak (can be >20GB)
    torch.cuda.empty_cache()
    del tensorf_model

    # Save model and video to nerf_data for retrieval
    out_model_path = Path(f"data/nerf_data/{id}/model.th")
    out_video_path = Path(f"data/nerf_data/{id}/video.mp4")
    os.makedirs(f"data/nerf_data/{id}", exist_ok=True)
    shutil.copy(f"{logfolder}/imgs_render_all/video.mp4", out_video_path)
    shutil.copy(f"{logfolder}/{id}.th", out_model_path)

    out_model_path = base_url + str(out_model_path)
    out_video_path = base_url + str(out_video_path)

    nerf_output_object = {
        "id": id,
        "model_filepath": out_model_path,
        "rendered_video_path": out_video_path
    }

    # Use threadsafe callback to ack message and publish nerf_output_object 
    callback = functools.partial(
        ack_publish_message, 
        channel, 
        method.delivery_tag, 
        json.dumps(nerf_output_object))
    
    channel.connection.add_callback_threadsafe(callback)


def nerf_worker(i, *args):
    logger = nerf_worker_logger('nerf-worker')
    logger.info("~NERF WORKER~")
    logger.info(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info(f"Available CUDA devices: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            logger.info(f"CUDA Device {i}: {torch.cuda.get_device_name(i)}")
    
        
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
            threads = []
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='nerf-in')
            channel.queue_declare(queue='nerf-out')

            # Will block until it creates a separate thread for each message
            # This is to prevent the main thread from blocking
            channel.basic_qos(prefetch_count=1)
            on_message_callback = functools.partial(on_message, args = (threads))
            channel.basic_consume(queue='nerf-in', on_message_callback=on_message_callback, auto_ack=False)
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
    nerfProcess = torch.multiprocessing.spawn(fn=nerf_worker, args=())
    nerfProcess.start()
    flaskProcess.join()
    nerfProcess.join()

        