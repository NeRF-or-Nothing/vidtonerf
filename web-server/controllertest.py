from flask import Flask, request, make_response, send_file, send_from_directory, url_for
from controller import WebServer, app
from services.scene_service import ClientService
from models.scene import SceneManager
from services.queue_service import RabbitMQService
from argparser import create_arguments
import argparse
import pytest
from controller import WebServer
import unittest

app = Flask(__name__)

app.run(host='0.0.0.0', port=3000)

parser = create_arguments()
args = parser.parse_args()
app.testing = True


class ControllerTest(unittest.TestCase):
    def setUp(self):
        app = app.test_client()
        response = app.get('/test')
        self.assertEqual(response, "hello")

    def test_pubVideo(self):
        response = app.post('/video/publish', data={'uuid': 'testuuid'})
        self.assertEqual(response.status_code, 200)

    def test_recvVideo(self):
        response = app.post('/video', data={'uuid': 'testuuid'})
        self.assertEqual(response.status_code, 200)

    def test_sendVideo(self):
        response = app.test_client().get('/video/video1')
        self.assertEqual(response.status_code, 200)

    def test_sendNerfVideo(self):
        response = app.test_client().get('/nerfvideo/video1')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
