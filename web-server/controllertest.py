from flask import Flask, request, make_response, send_file, send_from_directory, url_for
from controller import WebServer;
from services.scene_service import ClientService;
from models.scene import SceneManager
from services.queue_service import RabbitMQService
import argparse
import pytest

app = Flask(__name__)

def testAddRoutes():

    check = False

    response = app.test_client().get('/video/publish')
    if (response.status != 200):
        check = True
    
    assert(check == True)

    check = False

    response = app.test_client().get('/video')
    if (response.status != 200):
        check = True

    assert(check == True)

    check = False

    response = app.test_client().get('/video/<vidid>')
    if (response.status != 200):
        check = True

    assert(check == True)

    check = False

    response = app.test_client().get('/nerfvideo/<vidid>')
    if (response.status != 200):
        check = True

    assert(check == True)

    return "Test Completed!"

print(testAddRoutes())
