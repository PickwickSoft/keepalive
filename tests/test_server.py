import os
import subprocess
import time
from http import HTTPStatus
from unittest import TestCase

import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return


class ServerTester(TestCase):
    port = "5000"
    base_url = "http://localhost:{}".format(port)
    proc: subprocess.Popen = None
    test_server: subprocess.Popen = None
    base_dir = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.Popen(["uvicorn", "main:app", "--port", cls.port], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, cwd=f"{cls.base_dir}/../src")

        cls.test_server = subprocess.Popen(["uvicorn", "test_server:app", "--port", "1212"], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, cwd=cls.base_dir)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.proc.kill()
        cls.proc.wait()
        cls.test_server.kill()
        cls.test_server.wait()

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
        response = requests.post(f"{self.base_url}/alive/", json={"url": "http://127.0.0.1:1212"})
        self.assertEqual('200', response.text)
        self.assertEqual(HTTPStatus.OK, response.status_code)
