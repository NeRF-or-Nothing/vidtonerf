from flask import Flask, request, make_response, send_file, send_from_directory, url_for
#from controller import WebServer, app
from emptytest import app
from services.scene_service import ClientService
from models.scene import SceneManager
from services.queue_service import RabbitMQService
from argparser import create_arguments
import argparse
import pytest
from controller import WebServer
import unittest

class ControllerTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        response = self.client.get('/test')
        self.assertEqual(response.data, b"hello")
    
    def test_pubVideo(self):
        response = self.client.post('/video/publish', data={'uuid': 'testuuid'})
        self.assertEqual(response.status_code, 200)

    def test_recvVideo(self):
        response = self.client.post('/video', data={'uuid': 'testuuid'})
        self.assertEqual(response.status_code, 200)

    def test_sendVideo(self):
        response = self.client.get('/video/video1')
        self.assertEqual(response.status_code, 200)

    def test_sendNerfVideo(self):
        response = self.client.get('/nerfvideo/video1')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

