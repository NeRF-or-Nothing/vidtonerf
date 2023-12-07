import unittest
from emptytest import app

class TestWebServer(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_webServer(self):
        response = self.client.get('/test')
        print(response)
        self.assertEqual(response.data, b'hello')

if __name__ == '__main__':
    unittest.main()