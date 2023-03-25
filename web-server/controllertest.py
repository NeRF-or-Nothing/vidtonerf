from flask import Flask, request, make_response, send_file, send_from_directory, url_for
from controller import WebServer;
from services.scene_service import ClientService;
from models.scene import SceneManager
from services.queue_service import RabbitMQService
import argparse

app = Flask(__name__)

@app.route("/")
def index():
    return "this is an html string!"

SM = SceneManager()
RQ = RabbitMQService()

CS = ClientService(SM,RQ)

test = WebServer(argparse.Namespace, CS)
test.run()

app.run(host="0.0.0.0", port = 4000)
