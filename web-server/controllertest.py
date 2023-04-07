from flask import Flask, request, make_response, send_file, send_from_directory, url_for
from controller import WebServer,app;
from services.scene_service import ClientService;
from models.scene import SceneManager
from services.queue_service import RabbitMQService
from argparser import create_arguments
import argparse
import pytest
from controller import WebServer

parser = create_arguments()
args = parser.parse_args()
w = WebServer(args, ClientService)
app.testing = True

def testAddRoutes():
    response = app.test_client().post('/video/publish', data={'uuid': 'testuuid'})
    #assert(response.status_code==200)
    print(app.test_client())
    #note, do not need if statements, test assert response.status_code == 200
    print(response.status_code)

    response = app.test_client().post('/video', data={'uuid': 'testuuid'})
    #assert(response.status_code == 200)
    print(app.test_client())
    print(response.status_code)

    response = app.test_client().get('/video/<vidid>')
    #assert(response.status_code == 200)
    print(app.test_client())
    print(response.status_code)

    response = app.test_client().get('/nerfvideo/<vidid>')
    #assert(response.status_code == 200)
    print(app.test_client())
    print(response.status_code)

    return "Test Completed!"

print(testAddRoutes())
