import subprocess
import time
from http import HTTPStatus
from unittest import TestCase

import requests


class ServerTester(TestCase):
    port = "5000"
    base_url = "http://localhost:{}".format(port)
    proc = None

    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.Popen(["uvicorn", "main:app", "--port", cls.port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.proc.kill()
        cls.proc.wait()

    def test_root(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_alive_not_exist(self):
        # Call the alive endpoint with a URL that doesn't exist
        response = requests.post(f"{self.base_url}/alive/", json={"url": "http://does-not.exist/"})
        self.assertEqual('400', response.text)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_alive_does_exist(self):
        # Call the alive endpoint with a URL that exists
        response = requests.post(f"{self.base_url}/alive/", json={"url": "https://www.github.com/"})
        self.assertEqual('200', response.text)
        self.assertEqual(HTTPStatus.OK, response.status_code)
